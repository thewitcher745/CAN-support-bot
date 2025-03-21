from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, CallbackQueryHandler, MessageHandler, filters

from utils import fixed_keyboards
from utils.strings import (
    SEND_MESSAGE_PROMPT,
    SEND_MESSAGE_SUCCESS,
    SEND_MESSAGE_ERROR
)
from admin_panel.basic_handlers import cancel_operation
from utils.utilities import admin_required, handle_telegram_errors


@admin_required
@handle_telegram_errors
async def get_message_from_reply(update: Update, context: CallbackContext):
    """
    Handler for getting a message from a reply to forward to a user.

    Args:
        update (Update): The Telegram update object
        context (CallbackContext): The callback context object

    Returns:
        str: The next conversation state 'SET_MESSAGE_ID' if successful
        int: ConversationHandler.END if an error occurs
    """
    if update.message.reply_to_message:
        # Get the target user ID from command arguments
        args = context.args
        if not args:
            # If no user ID provided, send back to sender
            target_user_id = update.effective_chat.id
        else:
            target_user_id = args[0]

        context.user_data['target_user_id'] = target_user_id
        context.user_data['message_id'] = update.message.reply_to_message.message_id
        context.user_data['from_chat_id'] = update.effective_chat.id

        try:
            await context.bot.copy_message(chat_id=target_user_id,
                                           from_chat_id=update.effective_chat.id,
                                           message_id=update.message.reply_to_message.message_id
                                           )
            await update.message.reply_text(SEND_MESSAGE_SUCCESS.format(user_id=target_user_id),
                                            reply_markup=fixed_keyboards.RETURN_TO_MAIN_MENU
                                            )
        except Exception as e:
            await update.message.reply_text(SEND_MESSAGE_ERROR.format(error=str(e)),
                                            reply_markup=fixed_keyboards.RETURN_TO_MAIN_MENU
                                            )

        return ConversationHandler.END

    else:
        await update.message.reply_text(SEND_MESSAGE_PROMPT)
        return 'SET_MESSAGE_ID'


@admin_required
@handle_telegram_errors
async def get_message_from_user_update(update: Update, context: CallbackContext):
    """
    Handler for initiating the send message process from a callback query (menu button).

    Args:
        update (Update): The Telegram update object
        context (CallbackContext): The callback context object

    Returns:
        str: The next conversation state 'SET_MESSAGE_ID'
    """
    await update.callback_query.edit_message_text(SEND_MESSAGE_PROMPT,
                                                  reply_markup=fixed_keyboards.CANCEL_OPERATION)
    return 'SET_MESSAGE_ID'


@handle_telegram_errors
async def set_message_id(update: Update, context: CallbackContext):
    """
    Handler for storing the message ID and chat ID after the user sends a message to forward.

    Args:
        update (Update): The Telegram update object
        context (CallbackContext): The callback context object

    Returns:
        int: ConversationHandler.END
    """
    # Store the message details for later forwarding
    context.user_data['message_id'] = update.message.message_id
    context.user_data['from_chat_id'] = update.effective_chat.id

    # Get the target user ID from command arguments
    args = context.args
    if not args:
        # If no user ID provided, send back to sender
        target_user_id = update.effective_chat.id
    else:
        target_user_id = args[0]

    try:
        await context.bot.copy_message(
            chat_id=target_user_id,
            from_chat_id=update.effective_chat.id,
            message_id=update.message.message_id
        )
        await update.message.reply_text(
            SEND_MESSAGE_SUCCESS.format(user_id=target_user_id),
            reply_markup=fixed_keyboards.RETURN_TO_MAIN_MENU
        )
    except Exception as e:
        await update.message.reply_text(
            SEND_MESSAGE_ERROR.format(error=str(e)),
            reply_markup=fixed_keyboards.RETURN_TO_MAIN_MENU
        )

    return ConversationHandler.END


send_message_handler = ConversationHandler(
    entry_points=[
        CommandHandler('send', get_message_from_reply),
        CallbackQueryHandler(
            callback=get_message_from_user_update, pattern='START_SEND_MESSAGE')
    ],
    states={
        'SET_MESSAGE_ID': [MessageHandler(filters=~filters.COMMAND, callback=set_message_id)]
    },
    fallbacks=[
        CommandHandler('cancel', cancel_operation),
        CallbackQueryHandler(cancel_operation, pattern='CANCEL')
    ]
)
