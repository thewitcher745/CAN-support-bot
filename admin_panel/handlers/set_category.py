from telegram import error, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, ConversationHandler

from admin_panel.handlers import cancel_operation
from admin_panel.utilities import admin_required, get_category_id_list, get_category_label_by_id, set_category_user_list


@admin_required
async def get_user_list_to_set(update: Update, context: CallbackContext):
    """Sets a category's user list to the list of ID's given in a replied message."""

    try:
        if not update.message.reply_to_message:
            # If the command wasn't used in reply to a message, show an error message
            await update.message.reply_text('⚠️ You have to use this command in reply to a list of user ID\'s.')
            return

        # Parse the list of user ID's in the replied message.
        user_ids = update.message.reply_to_message.text.split()
        user_ids = [user_id for user_id in user_ids]

        context.user_data['user_list_to_set'] = user_ids

        # Create a keyboard of categories that the user is not currently in.
        categories_with_ids = get_category_id_list()
        categories_keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton(user_category_label, callback_data=user_category_id)] for user_category_id, user_category_label in
             categories_with_ids]
        )

        # Get the category the user should be in
        await update.message.reply_text('📈 Please select a category to set the user list for:', reply_markup=categories_keyboard)

        return 'GET_CATEGORY_ID_TO_SET'

    except error.BadRequest as e:
        await context.bot.send_message(update.effective_chat.id, f'⚠️ Error: User ID might be invalid or bot has no permission: {str(e)}')

    except Exception as e:
        await context.bot.send_message(update.effective_chat.id, f'🚨 An error occurred: {str(e)}')

    return ConversationHandler.END


async def get_category_id_to_set(update: Update, context: CallbackContext):
    # Take the category_id through the callback query and the target_user_id through the user_data object
    try:
        category_id = update.callback_query.data
        context.user_data['category_id_to_set'] = category_id
        print(f'get_category_id_to_set SETTING CATEGORY WITH ID TO LIST {context.user_data['user_list_to_set']}', category_id)

        confirmation_keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton('Yes', callback_data='CONFIRM_SET_CATEGORY'), InlineKeyboardButton('Cancel', callback_data='CANCEL_OPERATION')]]
        )

        await update.callback_query.answer()

        # Edit the last message sent by the bot to indicate the success and to not show the keyboard
        await update.callback_query.edit_message_text(
            f'❓ Are you sure you want to set the user list for category {get_category_label_by_id(category_id)}?',
            reply_markup=confirmation_keyboard)

        return 'CONFIRM_SET_CATEGORY'

    except error.BadRequest as e:
        await context.bot.send_message(update.effective_chat.id, f'⚠️ Error: User ID might be invalid or bot has no permission: {str(e)}')

    # except Exception as e:
    #     await context.bot.send_message(update.effective_chat.id, f'🚨 An error occurred: {str(e)}')


async def confirm_set_category(update: Update, context: CallbackContext):
    try:
        if update.callback_query.data == 'CANCEL_OPERATION':
            await update.callback_query.answer()

            context.user_data.clear()
            return await cancel_operation(update, context)

        # Get the category id from the callback query and the message id from the user_data object
        category_id = context.user_data['category_id_to_set']
        user_list = context.user_data['user_list_to_set']
        print(f'confirm_set_category SETTING CATEGORY WITH ID TO LIST {context.user_data['user_list_to_set']}', category_id)

        # Set the user list for the category
        set_category_user_list(category_id, user_list)

        await update.callback_query.answer()

        # Edit the last message sent by the bot to indicate the success and to not show the keyboard
        await update.callback_query.edit_message_text(f'✅ Category {get_category_label_by_id(category_id)} set successfully!')

        context.user_data.clear()

        return ConversationHandler.END

    except error.BadRequest as e:
        await context.bot.send_message(update.effective_chat.id, f'⚠️ Error: User ID might be invalid or bot has no permission: {str(e)}')

    # except Exception as e:
    #     await context.bot.send_message(update.effective_chat.id, f'🚨 An error occurred: {str(e)}')

    context.user_data.clear()

    return ConversationHandler.END
