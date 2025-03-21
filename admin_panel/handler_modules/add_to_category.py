from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from utils import fixed_keyboards
from admin_panel.basic_handlers import cancel_operation
from utils.utilities import admin_required, get_category_label_by_id, add_user_list_to_category, handle_telegram_errors


@admin_required
@handle_telegram_errors
async def get_user_list_from_reply(update: Update, context: CallbackContext):
    """
    Handler for getting a list of user IDs from a replied message to add to a category.
    
    Args:
        update (Update): The Telegram update object
        context (CallbackContext): The callback context object
        
    Returns:
        str: The next conversation state 'GET_CATEGORY_ID_TO_ADD'
        None: If no message was replied to
    """
    if not update.message.reply_to_message:
        await update.message.reply_text('⚠️ You have to use this command in reply to a list of user ID\'s.')
        return

    # Parse space-separated user IDs from the replied message
    user_ids = update.message.reply_to_message.text.split()
    context.user_data['user_list_to_add'] = user_ids

    # Prompt user to select category
    await update.message.reply_text(
        '📈 Please select a category to add the user list to:', 
        reply_markup=fixed_keyboards.CATEGORIES
    )

    return 'GET_CATEGORY_ID_TO_ADD'


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
        '📋 Send the list of user IDs you want to add to a category.',
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
        str: The next conversation state 'GET_CATEGORY_ID_TO_ADD'
    """
    # Parse space-separated user IDs from message
    user_ids = update.message.text.split()
    context.user_data['user_list_to_add'] = user_ids

    await update.message.reply_text(
        '📈 Please select a category to add the user list to:', 
        reply_markup=fixed_keyboards.CATEGORIES
    )
    return 'GET_CATEGORY_ID_TO_ADD'


@admin_required
@handle_telegram_errors
async def get_category_id(update: Update, context: CallbackContext):
    """
    Handler for processing selected category and asking for confirmation.
    
    Args:
        update (Update): The Telegram update object
        context (CallbackContext): The callback context object
        
    Returns:
        str: The next conversation state 'CONFIRM_ADD_CATEGORY'
    """
    # Store selected category ID from callback data
    category_id = update.callback_query.data
    context.user_data['category_id_to_add'] = category_id

    await update.callback_query.answer()

    # Show confirmation prompt
    await update.callback_query.edit_message_text(
        f'❓ Are you sure you want to add the user list to category {get_category_label_by_id(category_id)}?',
        reply_markup=fixed_keyboards.CONFIRMATION
    )

    return 'CONFIRM_ADD_CATEGORY'


@admin_required
@handle_telegram_errors
async def confirm(update: Update, context: CallbackContext):
    """
    Handler for processing confirmation and adding users to selected category.
    
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
    category_id = context.user_data['category_id_to_add']
    user_list = context.user_data['user_list_to_add']

    # Add users to category
    add_user_list_to_category(category_id, user_list)

    await update.callback_query.answer()

    # Show success message
    await update.callback_query.edit_message_text(
        f'✅ Selected list added to category {get_category_label_by_id(category_id)} successfully!',
        reply_markup=fixed_keyboards.RETURN_TO_MAIN_MENU
    )

    context.user_data.clear()
    return ConversationHandler.END
