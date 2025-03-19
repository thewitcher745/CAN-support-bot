from telegram import Update, error
from telegram.ext import CallbackContext, ConversationHandler

from admin_panel import fixed_keyboards
from admin_panel.basic_handlers import cancel_operation
from admin_panel.utilities import admin_required, get_category_label_by_id, set_category_user_list


@admin_required
async def get_user_list_from_reply(update: Update, context: CallbackContext):
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

        # Get the category the user should be in
        await update.message.reply_text('📈 Please select a category to set the user list for:', reply_markup=fixed_keyboards.CATEGORIES)

        return 'GET_CATEGORY_ID_TO_SET'

    except error.BadRequest as e:
        await context.bot.send_message(update.effective_chat.id, f'⚠️ Error: User ID might be invalid or bot has no permission: {str(e)}')

    except Exception as e:
        await context.bot.send_message(update.effective_chat.id, f'🚨 An error occurred: {str(e)}')

    context.user_data.clear()

    return ConversationHandler.END


@admin_required
async def get_user_list_from_user_update(update: Update, context: CallbackContext):
    """
    Get the user list from a message sent by the user after clicking the menu button.
    """
    try:
        await update.callback_query.edit_message_text(
            '📋 Send the list of user IDs you want to set for the category.',
            reply_markup=fixed_keyboards.CANCEL_OPERATION
        )
        return 'SET_USER_LIST'

    except error.BadRequest as e:
        await context.bot.send_message(update.effective_chat.id, f'⚠️ Error: User ID might be invalid or bot has no permission: {str(e)}')
    except Exception as e:
        await context.bot.send_message(update.effective_chat.id, f'🚨 An error occurred: {str(e)}')

    context.user_data.clear()
    return ConversationHandler.END


async def set_user_list(update: Update, context: CallbackContext):
    """Process the user list message and show category selection."""
    try:
        # Parse the list of user ID's from the message
        user_ids = update.message.text.split()
        user_ids = [user_id for user_id in user_ids]
        context.user_data['user_list_to_set'] = user_ids

        await update.message.reply_text(
            '📈 Please select a category to set the user list for:',
            reply_markup=fixed_keyboards.CATEGORIES
        )
        return 'GET_CATEGORY_ID_TO_SET'

    except Exception as e:
        await context.bot.send_message(update.effective_chat.id, f'🚨 An error occurred: {str(e)}')
        context.user_data.clear()
        return ConversationHandler.END


async def get_category_id(update: Update, context: CallbackContext):
    # Take the category_id through the callback query and the target_user_id through the user_data object
    try:
        category_id = update.callback_query.data
        context.user_data['category_id_to_set'] = category_id

        await update.callback_query.answer()

        # Edit the last message sent by the bot to indicate the success and to not show the keyboard
        await update.callback_query.edit_message_text(
            f'❓ Are you sure you want to set the user list for category {get_category_label_by_id(category_id)}?',
            reply_markup=fixed_keyboards.CONFIRMATION)

        return 'CONFIRM_SET_CATEGORY'

    except error.BadRequest as e:
        await context.bot.send_message(update.effective_chat.id, f'⚠️ Error: User ID might be invalid or bot has no permission: {str(e)}')

    except Exception as e:
        await context.bot.send_message(update.effective_chat.id, f'🚨 An error occurred: {str(e)}')

    context.user_data.clear()

    return ConversationHandler.END


async def confirm(update: Update, context: CallbackContext):
    try:
        if not update.callback_query.data == 'CONFIRM':
            await update.callback_query.answer()

            context.user_data.clear()
            return await cancel_operation(update, context)

        # Get the category id from the callback query and the message id from the user_data object
        category_id = context.user_data['category_id_to_set']
        user_list = context.user_data['user_list_to_set']

        # Set the user list for the category
        set_category_user_list(category_id, user_list)

        await update.callback_query.answer()

        # Edit the last message sent by the bot to indicate the success and to not show the keyboard
        await update.callback_query.edit_message_text(f'✅ Category {get_category_label_by_id(category_id)} set successfully!',
                                                      reply_markup=fixed_keyboards.RETURN_TO_MAIN_MENU)

        context.user_data.clear()

        return ConversationHandler.END

    except error.BadRequest as e:
        await context.bot.send_message(update.effective_chat.id, f'⚠️ Error: User ID might be invalid or bot has no permission: {str(e)}')

    except Exception as e:
        await context.bot.send_message(update.effective_chat.id, f'🚨 An error occurred: {str(e)}')

    context.user_data.clear()

    return ConversationHandler.END
