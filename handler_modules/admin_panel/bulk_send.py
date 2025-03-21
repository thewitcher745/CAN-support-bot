"""
Bulk Send Module

This module handles sending messages to all users in a specified category.
Messages can be selected either by:
1. Replying to another message with a command
2. Sending/forwarding a message to the bot after selecting the Bulk Send option from the main menu
"""

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
    BULK_SEND_MESSAGE_SELECTED,
    BULK_SEND_ERROR_REPLY,
    BULK_SEND_PROMPT,
    BULK_SEND_CATEGORY_SELECTED,
    BULK_SEND_ERROR_USER,
    BULK_SEND_SUCCESS,
)
from handler_modules.basic_handlers import cancel_operation
from utils.utilities import (
    admin_required,
    get_category_label_by_id,
    get_users_by_category_id,
    handle_telegram_errors,
)


@admin_required
@handle_telegram_errors
async def get_message_from_reply(update: Update, context: CallbackContext):
    """
    Handler for getting a message from a reply to forward to multiple users.

    Stores the message_id and from_chat_id in user_data for later use in the bulk send process.

    Args:
        update (Update): The Telegram update object
        context (CallbackContext): The callback context object

    Returns:
        str: The next conversation state 'GET_CATEGORY_ID' if successful
        int: ConversationHandler.END if an error occurs
    """

    # If the command is used in reply to a previous message, that message will be forwarded to the recipients without the sender data.
    if update.message.reply_to_message:
        await update.message.reply_text(
            BULK_SEND_MESSAGE_SELECTED, reply_markup=fixed_keyboards.CATEGORIES
        )

        context.user_data["message_id"] = update.message.reply_to_message.message_id
        context.user_data["from_chat_id"] = update.effective_chat.id

        return "GET_CATEGORY_ID"

    else:
        # Confirmation message
        await update.message.reply_text(BULK_SEND_ERROR_REPLY)

        context.user_data.clear()

        return ConversationHandler.END


@admin_required
@handle_telegram_errors
async def get_message_from_user_update(update: Update, context: CallbackContext):
    """
    Handler for initiating the bulk send process from a callback query (menu button).

    Prompts the user to send a message that will be forwarded to multiple users.

    Args:
        update (Update): The Telegram update object
        context (CallbackContext): The callback context object

    Returns:
        str: The next conversation state 'SET_MESSAGE_ID' if successful
        int: ConversationHandler.END if an error occurs
    """
    await update.callback_query.edit_message_text(
        BULK_SEND_PROMPT, reply_markup=fixed_keyboards.CANCEL_OPERATION
    )
    return "SET_MESSAGE_ID"


@handle_telegram_errors
async def set_message_id(update: Update, context: CallbackContext):
    """
    Handler for storing the message ID and chat ID after the user sends a message to forward.

    Stores the message details and prompts the user to select a category.

    Args:
        update (Update): The Telegram update object
        context (CallbackContext): The callback context object

    Returns:
        str: The next conversation state 'GET_CATEGORY_ID'
    """
    # Store the message details for later forwarding
    context.user_data["message_id"] = update.message.message_id
    context.user_data["from_chat_id"] = update.effective_chat.id

    await update.message.reply_text(
        BULK_SEND_MESSAGE_SELECTED, reply_markup=fixed_keyboards.CATEGORIES
    )

    return "GET_CATEGORY_ID"


@handle_telegram_errors
async def get_category_id(update: Update, context: CallbackContext):
    """
    Handler for processing the selected category for bulk message sending.

    Gets the category ID from the callback query and prompts for confirmation.

    Args:
        update (Update): The Telegram update object
        context (CallbackContext): The callback context object

    Returns:
        str: The next conversation state 'CONFIRM_BULK_SEND' if successful
        int: ConversationHandler.END if an error occurs or operation is canceled
    """

    if update.callback_query.data == "CANCEL":
        await update.callback_query.answer()
        context.user_data.clear()
        return await cancel_operation(update, context)

    # Get the category id from the callback query
    category_id = update.callback_query.data
    context.user_data["category_id"] = category_id

    # Get user count for confirmation message
    user_count = len(get_users_by_category_id(category_id))
    category_label = get_category_label_by_id(category_id)

    await update.callback_query.answer()

    # Prompt for confirmation before sending to multiple users
    await update.callback_query.edit_message_text(
        BULK_SEND_CATEGORY_SELECTED.format(category=category_label, count=user_count),
        reply_markup=fixed_keyboards.CONFIRMATION,
    )

    return "CONFIRM_BULK_SEND"


@handle_telegram_errors
async def confirm(update: Update, context: CallbackContext):
    """
    Handler for processing the confirmation of bulk message sending.

    If confirmed, sends the message to all users in the selected category.

    Args:
        update (Update): The Telegram update object
        context (CallbackContext): The callback context object

    Returns:
        int: ConversationHandler.END in all cases, ending the conversation
    """

    # Check if user confirmed the operation
    if not update.callback_query.data == "CONFIRM":
        await update.callback_query.answer()
        context.user_data.clear()
        return await cancel_operation(update, context)

    # Retrieve stored data needed for message forwarding
    category_id = context.user_data["category_id"]
    message_id = context.user_data["message_id"]
    from_chat_id = context.user_data["from_chat_id"]

    # Get all users in the selected category
    users_in_category = get_users_by_category_id(category_id)
    category_label = get_category_label_by_id(category_id)

    # Send the message to every user in the category
    # We continue even if some sends fail to ensure all users are attempted
    for chat_id in users_in_category:
        try:
            await context.bot.copy_message(
                chat_id=chat_id, from_chat_id=from_chat_id, message_id=message_id
            )
        except Exception as e:
            # Log the error but continue with other users
            await context.bot.send_message(
                update.effective_chat.id,
                BULK_SEND_ERROR_USER.format(user_id=chat_id, error=str(e)),
            )

    await update.callback_query.answer()

    # Show success message and return to main menu
    await update.callback_query.edit_message_text(
        BULK_SEND_SUCCESS.format(category=category_label),
        reply_markup=fixed_keyboards.RETURN_TO_MAIN_MENU,
    )

    context.user_data.clear()
    return ConversationHandler.END


bulk_send_handler = ConversationHandler(
    entry_points=[
        CommandHandler("bulksend", get_message_from_reply),
        CallbackQueryHandler(
            callback=get_message_from_user_update, pattern="START_BULK_SEND"
        ),
    ],
    states={
        "SET_MESSAGE_ID": [
            MessageHandler(filters=~filters.COMMAND, callback=set_message_id)
        ],
        "GET_CATEGORY_ID": [CallbackQueryHandler(get_category_id)],
        "CONFIRM_BULK_SEND": [CallbackQueryHandler(confirm)],
    },
    fallbacks=[
        CommandHandler("cancel", cancel_operation),
        CallbackQueryHandler(cancel_operation, pattern="CANCEL"),
    ],
)
