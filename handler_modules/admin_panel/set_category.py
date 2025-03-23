from telegram import Update
from telegram.ext import (
    CallbackContext,
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from utils import fixed_keyboards
from utils.strings import (
    CATEGORY_ERROR_REPLY,
    CATEGORY_SELECT_PROMPT,
    CATEGORY_USER_LIST_PROMPT,
    CATEGORY_CONFIRM_SET,
    CATEGORY_SET_SUCCESS,
)
from handler_modules.basic_handlers import cancel_operation
from utils.utilities import (
    admin_required,
    get_category_label_by_id,
    set_category_user_list,
    handle_telegram_errors,
)


@admin_required
@handle_telegram_errors
async def get_user_list_from_reply(update: Update, context: CallbackContext):
    '''
    Handler for getting a list of user IDs from a replied message to set as a category's user list.

    Args:
        update (Update): The Telegram update object
        context (CallbackContext): The callback context object

    Returns:
        str: The next conversation state 'GET_CATEGORY_ID_TO_SET'
        None: If no message was replied to
    '''
    if not update.message.reply_to_message:
        await update.message.reply_text(CATEGORY_ERROR_REPLY)
        return

    # Parse space-separated user IDs from the replied message
    user_ids = update.message.reply_to_message.text.split()
    context.user_data['user_list_to_set'] = user_ids

    # Prompt user to select category
    await update.message.reply_text(
        CATEGORY_SELECT_PROMPT, reply_markup=fixed_keyboards.CATEGORIES
    )

    return 'GET_CATEGORY_ID_TO_SET'


@admin_required
@handle_telegram_errors
async def get_user_list_from_user_update(update: Update, context: CallbackContext):
    '''
    Handler for getting a list of user IDs directly from user input after clicking menu button.

    Args:
        update (Update): The Telegram update object
        context (CallbackContext): The callback context object

    Returns:
        str: The next conversation state 'SET_USER_LIST'
    '''
    await update.callback_query.edit_message_text(
        CATEGORY_USER_LIST_PROMPT, reply_markup=fixed_keyboards.CANCEL_OPERATION
    )
    return 'SET_USER_LIST'


@handle_telegram_errors
async def set_user_list(update: Update, context: CallbackContext):
    '''
    Handler for processing user-provided list of IDs and prompting for category selection.

    Args:
        update (Update): The Telegram update object
        context (CallbackContext): The callback context object

    Returns:
        str: The next conversation state 'GET_CATEGORY_ID_TO_SET'
    '''
    # Parse space-separated user IDs from message
    user_ids = update.message.text.split()
    context.user_data['user_list_to_set'] = user_ids

    # Prompt user to select category
    await update.message.reply_text(
        CATEGORY_SELECT_PROMPT, reply_markup=fixed_keyboards.CATEGORIES
    )

    return 'GET_CATEGORY_ID_TO_SET'


@admin_required
@handle_telegram_errors
async def get_category_id(update: Update, context: CallbackContext):
    '''
    Handler for processing the selected category and asking for confirmation.

    Args:
        update (Update): The Telegram update object
        context (CallbackContext): The callback context object

    Returns:
        str: The next conversation state 'CONFIRM_SET_CATEGORY'
    '''
    # Get the category_id from callback data
    category_id = update.callback_query.data
    context.user_data['category_id_to_set'] = category_id

    await update.callback_query.answer()

    # Show confirmation prompt with category name
    await update.callback_query.edit_message_text(
        CATEGORY_CONFIRM_SET.format(category=get_category_label_by_id(category_id)),
        reply_markup=fixed_keyboards.CONFIRMATION,
    )

    return 'CONFIRM_SET_CATEGORY'


@admin_required
@handle_telegram_errors
async def confirm(update: Update, context: CallbackContext):
    '''
    Handler for processing confirmation and setting the category's user list.

    Args:
        update (Update): The Telegram update object
        context (CallbackContext): The callback context object

    Returns:
        int: ConversationHandler.END on success
        Any: Result of cancel_operation() if not confirmed
    '''
    # Handle cancellation
    if not update.callback_query.data == 'CONFIRM':
        await update.callback_query.answer()
        context.user_data.clear()
        return await cancel_operation(update, context)

    # Get stored category ID and user list
    category_id = context.user_data['category_id_to_set']
    user_list = context.user_data['user_list_to_set']

    # Set the user list for the category
    set_category_user_list(category_id, user_list)

    await update.callback_query.answer()

    # Show success message
    await update.callback_query.edit_message_text(
        CATEGORY_SET_SUCCESS.format(category=get_category_label_by_id(category_id)),
        reply_markup=fixed_keyboards.RETURN_TO_MAIN_MENU,
    )

    # Clean up user data
    context.user_data.clear()

    return ConversationHandler.END


set_category_handler = ConversationHandler(
    entry_points=[
        CommandHandler('setcategory', get_user_list_from_reply),
        CallbackQueryHandler(
            callback=get_user_list_from_user_update, pattern='START_SET_CATEGORY'
        ),
    ],
    states={
        'SET_USER_LIST': [
            MessageHandler(filters=~filters.COMMAND, callback=set_user_list)
        ],
        'GET_CATEGORY_ID_TO_SET': [CallbackQueryHandler(get_category_id)],
        'CONFIRM_SET_CATEGORY': [CallbackQueryHandler(callback=confirm)],
    },
    fallbacks=[
        CommandHandler('cancel', cancel_operation),
        CallbackQueryHandler(cancel_operation, pattern='CANCEL'),
    ],
)
