from telegram import error, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, ConversationHandler

from admin_panel.basic_handlers import cancel_operation
from admin_panel.utilities import admin_required, get_category_id_list, get_category_label_by_id, get_users_by_category_id


@admin_required
async def get_message(update: Update, context: CallbackContext):
    """Send a message to all users in a category."""

    try:
        # If the command is used in reply to a previous message, that message will be forwarded to the recipients without the sender data.
        if update.message.reply_to_message:
            # Get a list of all the available categories in the form of a tuple of (id, label)
            categories_with_ids = get_category_id_list()
            categories_keyboard = InlineKeyboardMarkup(
                [[InlineKeyboardButton(user_category_label, callback_data=user_category_id)] for user_category_id, user_category_label in
                 categories_with_ids]
            )

            # Relay message
            await update.message.reply_text(f'📧 Message selected for bulk sending. Now select the category you wish the message to be sent to.',
                                            reply_markup=categories_keyboard)
            context.user_data['message_id'] = update.message.reply_to_message.message_id
            context.user_data['from_chat_id'] = update.effective_chat.id

            return 'GET_CATEGORY_ID'

        else:
            # Confirmation message
            await update.message.reply_text(
                f'⚠️ Error: Bulk sending can only be used in reply to a message. Please make sure you reply to a message with the command '
                f'and try again.')

            context.user_data.clear()

            return ConversationHandler.END

    except error.BadRequest as e:
        await context.bot.send_message(update.effective_chat.id, '⚠️ Error: User ID might be invalid or bot has no permission: {str(e)}')

    except Exception as e:
        await context.bot.send_message(update.effective_chat.id, f'🚨 An error occurred: {str(e)}')

    context.user_data.clear()

    return ConversationHandler.END


async def get_category_id(update: Update, context: CallbackContext):
    try:
        # Get the category id from the callback query and the message id from the user_data object
        category_id = update.callback_query.data
        context.user_data['category_id'] = category_id

        await update.callback_query.answer()

        confirmation_keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton('Yes', callback_data='CONFIRM_SET_CATEGORY'), InlineKeyboardButton('Cancel', callback_data='CANCEL_OPERATION')]]
        )

        await update.callback_query.answer()

        # Edit the last message sent by the bot to indicate the success and to not show the keyboard
        await update.callback_query.edit_message_text(
            f'❓ Category {get_category_label_by_id(category_id)} selected successfully. Are you sure you want to send the message to all'
            f' {len(get_users_by_category_id(category_id))} users in this category?',
            reply_markup=confirmation_keyboard)

        return 'CONFIRM_BULK_SEND'

    except error.BadRequest as e:
        await context.bot.send_message(update.effective_chat.id, f'⚠️ Error: User ID might be invalid or bot has no permission: {str(e)}')

    except Exception as e:
        await context.bot.send_message(update.effective_chat.id, f'🚨 An error occurred: {str(e)}')

    context.user_data.clear()

    return ConversationHandler.END


async def confirm(update: Update, context: CallbackContext):
    try:
        if update.callback_query.data == 'CANCEL_OPERATION':
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
            f'✅ Message sent to all users in category {get_category_label_by_id(category_id)} successfully!')

        context.user_data.clear()

        return ConversationHandler.END

    except error.BadRequest as e:
        await context.bot.send_message(update.effective_chat.id, f'⚠️ Error: User ID might be invalid or bot has no permission: {str(e)}')

    except Exception as e:
        await context.bot.send_message(update.effective_chat.id, f'🚨 An error occurred: {str(e)}')

    context.user_data.clear()

    return ConversationHandler.END
