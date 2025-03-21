from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from utils import fixed_keyboards
from admin_panel.basic_handlers import cancel_operation
from utils.utilities import admin_required, get_category_label_by_id, handle_telegram_errors, remove_user_list_from_category


@admin_required
@handle_telegram_errors
async def get_user_list_from_reply(update: Update, context: CallbackContext):
    """
    Handler for getting a list of user IDs from a replied message to remove from a category.

    Args:
        update (Update): The Telegram update object
        context (CallbackContext): The callback context object

    Returns:
        str: The next conversation state 'GET_CATEGORY_ID_TO_REMOVE'
        None: If no message was replied to
    """
    if not update.message.reply_to_message:
        # If the command wasn't used in reply to a message, show an error message
        await update.message.reply_text('⚠️ You have to use this command in reply to a list of user ID\'s.')
        return

    # Parse the list of user ID's in the replied message
    user_ids = update.message.reply_to_message.text.split()
    context.user_data['user_list_to_remove'] = user_ids

    # Prompt user to select a category
    await update.message.reply_text(
        '📈 Please select a category to remove the user list from:',
        reply_markup=fixed_keyboards.CATEGORIES
    )

    return 'GET_CATEGORY_ID_TO_REMOVE'


@admin_required
@handle_telegram_errors
async def get_user_list_from_user_update(update: Update, context: CallbackContext):
    """
    Handler for getting a list of user IDs directly from user input after clicking menu button.

    Args:
        update (Update): The Telegram update object
        context (CallbackContext): The callback context object

    Returns:
        str: The next conversation state 'SET_USER_LIST'
    """
    await update.callback_query.edit_message_text(
        '📋 Send the list of user IDs you want to remove from a category.',
        reply_markup=fixed_keyboards.CANCEL_OPERATION
    )
    return 'SET_USER_LIST'


@handle_telegram_errors
async def set_user_list(update: Update, context: CallbackContext):
    """
    Handler for processing user-provided list of IDs and prompting for category selection.

    Args:
        update (Update): The Telegram update object
        context (CallbackContext): The callback context object

    Returns:
        str: The next conversation state 'GET_CATEGORY_ID_TO_REMOVE'
    """
    # Parse the list of user ID's from the message
    user_ids = update.message.text.split()
    context.user_data['user_list_to_remove'] = user_ids

    # Prompt user to select a category
    await update.message.reply_text(
        '📈 Please select a category to remove the user list from:',
        reply_markup=fixed_keyboards.CATEGORIES
    )
    return 'GET_CATEGORY_ID_TO_REMOVE'


@handle_telegram_errors
async def get_category_id(update: Update, context: CallbackContext):
    """
    Handler for processing the selected category and asking for confirmation.

    Args:
        update (Update): The Telegram update object
        context (CallbackContext): The callback context object

    Returns:
        str: The next conversation state 'CONFIRM_REMOVE_CATEGORY'
    """
    # Get the category_id from the callback query
    category_id = update.callback_query.data
    context.user_data['category_id_to_remove'] = category_id

    await update.callback_query.answer()

    # Show confirmation prompt with category name
    await update.callback_query.edit_message_text(
        f'❓ Are you sure you want to remove the user list from category {get_category_label_by_id(category_id)}?',
        reply_markup=fixed_keyboards.CONFIRMATION
    )

    return 'CONFIRM_REMOVE_CATEGORY'


@handle_telegram_errors
async def confirm(update: Update, context: CallbackContext):
    """
    Handler for processing confirmation and removing users from selected category.

    Args:
        update (Update): The Telegram update object
        context (CallbackContext): The callback context object

    Returns:
        int: ConversationHandler.END on success
        Any: Result of cancel_operation() if not confirmed
    """
    # Handle cancellation
    if not update.callback_query.data == 'CONFIRM':
        await update.callback_query.answer()
        context.user_data.clear()
        return await cancel_operation(update, context)

    # Get stored category ID and user list
    category_id = context.user_data['category_id_to_remove']
    user_list = context.user_data['user_list_to_remove']

    # Remove the user list from the category
    remove_user_list_from_category(category_id, user_list)

    await update.callback_query.answer()

    # Show success message
    await update.callback_query.edit_message_text(
        f'✅ Selected list removed from category {get_category_label_by_id(category_id)} successfully!',
        reply_markup=fixed_keyboards.RETURN_TO_MAIN_MENU
    )

    # Clean up user data
    context.user_data.clear()

    return ConversationHandler.END
