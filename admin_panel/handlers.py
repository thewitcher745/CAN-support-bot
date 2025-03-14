from telegram.ext import CallbackContext, ConversationHandler
from telegram import Update, error, InlineKeyboardMarkup, InlineKeyboardButton

from admin_panel.utilities import get_categories_for_user, get_category_id_list, add_user_to_category, get_category_label_by_id, \
    remove_user_from_category


# Define command handlers

async def show_help(update, context):
    """Send a welcome message when the command /start is issued."""
    help_message = """
📝 This bot is used to contact users. Currently it supports the following commands and functionalities:

/send <user id>: This command forwards a message to a single user given the user's ID. To select what message to forward, reply to the desired message with this command. If no user ID is given, the message is reflected back to the sender. If no message is replied to, a test message is sent instead. 📱

/setcategory <user id>: This command puts a user with a given user ID into a category. After using this command, select which category you would like to put the user in. 📈

/unsetcategory <user id>: This command removes a user with a given user ID from a category. After using this command, select which category you would like to remove the user from. 📈
"""
    await update.message.reply_text(help_message)


async def send_message(update: Update, context: CallbackContext):
    """Send a message to the target user ID."""
    try:
        # Get the target user ID from the sender
        try:
            target_user_id = update.message.text.split(' ')[1]

        except IndexError:
            await update.message.reply_text('⚠️ No target user specified, reflecting message back to sender...')
            target_user_id = update.message.from_user.id

        # If the command is used in reply to a previous message, that message will be forwarded to the recipient without the sender data.
        if update.message.reply_to_message:
            # Confirmation message
            await update.message.reply_text(f'📧 Forwarding message to user {target_user_id}...')

            await context.bot.copy_message(chat_id=target_user_id, from_chat_id=update.effective_chat.id,
                                           message_id=update.message.reply_to_message.message_id)

        # If the command isn't used in a reply, just send the dev message...
        else:
            # Confirmation message
            await update.message.reply_text(f'📨 Sending message to user {target_user_id}...')

            # Send the message to the target user
            await context.bot.send_message(target_user_id, f'This is a test message sent to user {target_user_id}')

    except error.BadRequest as e:
        await update.message.reply_text(f'⚠️ Error: User ID might be invalid or bot has no permission: {str(e)}')

    except Exception as e:
        await update.message.reply_text(f'🚨 An error occurred: {str(e)}')

    return


async def set_category(update: Update, context: CallbackContext):
    """Adds a user to a category."""
    try:
        # Get the target user ID from the sender
        try:
            target_user_id = update.message.text.split(' ')[1]
            context.user_data['target_user_id'] = target_user_id

        except IndexError:
            await update.message.reply_text('⚠️ You have to specify a target user ID for this command.')

            return

        # Show what lists the user is currently in
        user_categories = get_categories_for_user(target_user_id)
        message_text = f'📊 User {target_user_id} is currently in the following categories:\n\n'
        for category in user_categories:
            message_text += f'💠 {category}\n'

        await update.message.reply_text(message_text)

        # Create a keyboard of categories that the user is not currently in.
        categories_with_ids = get_category_id_list()
        categories_keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton(user_category_label, callback_data=user_category_id)] for user_category_id, user_category_label in
             categories_with_ids if user_category_label not in user_categories]
        )

        # Get the category the user should be in
        await update.message.reply_text('📈 Please select a category to put the user in:', reply_markup=categories_keyboard)

        return "FINALIZE_SET_CATEGORY"

    except error.BadRequest as e:
        await update.message.reply_text(f'⚠️ Error: User ID might be invalid or bot has no permission: {str(e)}')

    except Exception as e:
        await update.message.reply_text(f'🚨 An error occurred: {str(e)}')

    return ConversationHandler.END


async def finalize_set_category(update: Update, context: CallbackContext):
    # Take the category_id through the callback query and the target_user_id through the user_data object
    try:
        category_id = update.callback_query.data
        target_user_id = context.user_data['target_user_id']

        # Add the user to the category
        add_user_to_category(target_user_id, category_id)

        await update.callback_query.answer(f'✅ User {target_user_id} added to category {get_category_label_by_id(category_id)} successfully!')

        # Edit the last message sent by the bot to indicate the success and to not show the keyboard
        await update.callback_query.edit_message_text(
            f'✅ User {target_user_id} added to category {get_category_label_by_id(category_id)} successfully!')

    except error.BadRequest as e:
        await update.message.reply_text(f'⚠️ Error: User ID might be invalid or bot has no permission: {str(e)}')

    except Exception as e:
        await update.message.reply_text(f'🚨 An error occurred: {str(e)}')

    # Clear the user_data object
    context.user_data.clear()

    return ConversationHandler.END


async def unset_category(update: Update, context: CallbackContext):
    """Removes a user from a category."""
    try:
        # Get the target user ID from the sender
        try:
            target_user_id = update.message.text.split(' ')[1]
            context.user_data['target_user_id'] = target_user_id

        except IndexError:
            await update.message.reply_text('⚠️ You have to specify a target user ID for this command.')

            return

        # Show what lists the user is currently in
        user_categories = get_categories_for_user(target_user_id)

        # Create a keyboard of categories that the user is currently in.
        categories_with_ids = get_category_id_list()
        categories_keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton(user_category_label, callback_data=user_category_id)] for user_category_id, user_category_label in
             categories_with_ids if user_category_label in user_categories]
        )

        # Get the category the user should be removed from
        await update.message.reply_text('📈 Please select a category to remove the user from:', reply_markup=categories_keyboard)

        return "FINALIZE_UNSET_CATEGORY"

    except error.BadRequest as e:
        await update.message.reply_text(f'⚠️ Error: User ID might be invalid or bot has no permission: {str(e)}')

    except Exception as e:
        await update.message.reply_text(f'🚨 An error occurred: {str(e)}')

    return ConversationHandler.END


async def finalize_unset_category(update: Update, context: CallbackContext):
    # Take the category_id through the callback query and the target_user_id through the user_data object
    try:
        category_id = update.callback_query.data
        target_user_id = context.user_data['target_user_id']

        # Remove the user from the category
        remove_user_from_category(target_user_id, category_id)

        await update.callback_query.answer(f'✅ User {target_user_id} removed from category {get_category_label_by_id(category_id)} successfully!')

        # Edit the last message sent by the bot to indicate the success and to not show the keyboard
        await update.callback_query.edit_message_text(
            f'✅ User {target_user_id} removed from category {get_category_label_by_id(category_id)} successfully!')

    except error.BadRequest as e:
        await update.message.reply_text(f'⚠️ Error: User ID might be invalid or bot has no permission: {str(e)}')

    except Exception as e:
        await update.message.reply_text(f'🚨 An error occurred: {str(e)}')

    # Clear the user_data object
    context.user_data.clear()

    return ConversationHandler.END


async def cancel_operation(update: Update, context: CallbackContext):
    await context.bot.send_message(update.message.chat_id, "❌ Operation canceled by the user.")
    # Clear the user_data object
    context.user_data.clear()
    return ConversationHandler.END
