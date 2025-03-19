"""
Sends a message to all users in a category. The message can be selected by replying to another message with a command, or sent/forwarded to the bot
after selecting the Bulk Send option from the main menu using a user update (Callback query).
"""

from telegram import error, Update
from telegram.ext import CallbackContext, ConversationHandler

from admin_panel import fixed_keyboards
from admin_panel.basic_handlers import cancel_operation
from admin_panel.utilities import admin_required, get_category_label_by_id, get_users_by_category_id, handle_telegram_errors


@admin_required
@handle_telegram_errors
async def get_message_from_reply(update: Update, context: CallbackContext):
    """
    Get the message from the reply.
    Sets the values for message_id and from_chat_id fields of the user_data dict to be used later.
    """

    try:
        # If the command is used in reply to a previous message, that message will be forwarded to the recipients without the sender data.
        if update.message.reply_to_message:
            await update.message.reply_text(f'📧 Message selected for bulk sending. Now select the category you wish the message to be sent to.',
                                            reply_markup=fixed_keyboards.CATEGORIES)

            context.user_data['message_id'] = update.message.reply_to_message.message_id
            context.user_data['from_chat_id'] = update.effective_chat.id

            return 'GET_CATEGORY_ID'

        else:
            # Confirmation message
            await update.message.reply_text(
                f'⚠️ Error: The command /bulksend can only be used in reply to a message. Please make sure you reply to a message with the command '
                f'and try again.')

            context.user_data.clear()

            return ConversationHandler.END

    except error.BadRequest as e:
        await context.bot.send_message(update.effective_chat.id, f'⚠️ Error: User ID might be invalid or bot has no permission: {str(e)}')

    except Exception as e:
        await context.bot.send_message(update.effective_chat.id, f'🚨 An error occurred: {str(e)}')

    context.user_data.clear()

    return ConversationHandler.END


@admin_required
@handle_telegram_errors
async def get_message_from_user_update(update: Update, context: CallbackContext):
    """
    Get the message from a message sent by the user.
    Sets the values for message_id and from_chat_id fields of the user_data dict to be used later.
    """

    try:
        await update.callback_query.edit_message_text('📨 Send the message you wish to be sent to users in a category.',
                                                      reply_markup=fixed_keyboards.CANCEL_OPERATION)

        return 'SET_MESSAGE_ID'

    except error.BadRequest as e:
        await context.bot.send_message(update.effective_chat.id, f'⚠️ Error: User ID might be invalid or bot has no permission: {str(e)}')

    except Exception as e:
        await context.bot.send_message(update.effective_chat.id, f'🚨 An error occurred: {str(e)}')

    context.user_data.clear()

    return ConversationHandler.END


@handle_telegram_errors
async def set_message_id(update: Update, context: CallbackContext):
    # Sets the message ID and the from_chat ID from the message sent by the user
    context.user_data['message_id'] = update.message.message_id
    context.user_data['from_chat_id'] = update.effective_chat.id

    await update.message.reply_text(f'📧 Message selected for bulk sending. Now select the category you wish the message to be sent to.',
                                    reply_markup=fixed_keyboards.CATEGORIES)

    return 'GET_CATEGORY_ID'


@handle_telegram_errors
async def get_category_id(update: Update, context: CallbackContext):
    try:
        if update.callback_query.data == 'CANCEL':
            await update.callback_query.answer()

            context.user_data.clear()
            return await cancel_operation(update, context)

        # Get the category id from the callback query and the message id from the user_data object
        category_id = update.callback_query.data
        context.user_data['category_id'] = category_id

        await update.callback_query.answer()

        # Edit the last message sent by the bot to indicate the success and to not show the keyboard
        await update.callback_query.edit_message_text(
            f'❓ Category {get_category_label_by_id(category_id)} selected successfully. Are you sure you want to send the provided message to all'
            f' {len(get_users_by_category_id(category_id))} users in this category?',
            reply_markup=fixed_keyboards.CONFIRMATION)

        return 'CONFIRM_BULK_SEND'

    except error.BadRequest as e:
        await context.bot.send_message(update.effective_chat.id, f'⚠️ Error: User ID might be invalid or bot has no permission: {str(e)}')

    except Exception as e:
        await context.bot.send_message(update.effective_chat.id, f'🚨 An error occurred: {str(e)}')

    context.user_data.clear()

    return ConversationHandler.END


@handle_telegram_errors
async def confirm(update: Update, context: CallbackContext):
    try:
        if not update.callback_query.data == 'CONFIRM':
            await update.callback_query.answer()

            context.user_data.clear()
            return await cancel_operation(update, context)

        category_id = context.user_data['category_id']
        message_id = context.user_data['message_id']
        from_chat_id = context.user_data['from_chat_id']

        # Send the message to every user in the category
        users_in_category = get_users_by_category_id(category_id)

        for chat_id in users_in_category:
            try:
                await context.bot.copy_message(chat_id=chat_id, from_chat_id=from_chat_id, message_id=message_id)

            except Exception as e:
                await context.bot.send_message(update.effective_chat.id, f'⚠️ Error: Message sending failed for user ID {chat_id}: {str(e)}')

        await update.callback_query.answer()

        await update.callback_query.edit_message_text(
            f'✅ Message sent to all users in category {get_category_label_by_id(category_id)} successfully!',
            reply_markup=fixed_keyboards.RETURN_TO_MAIN_MENU)

        context.user_data.clear()

        return ConversationHandler.END

    except error.BadRequest as e:
        await context.bot.send_message(update.effective_chat.id, f'⚠️ Error: User ID might be invalid or bot has no permission: {str(e)}')

    except Exception as e:
        await context.bot.send_message(update.effective_chat.id, f'🚨 An error occurred: {str(e)}')

    context.user_data.clear()

    return ConversationHandler.END
