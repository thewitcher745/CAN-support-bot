from telegram.ext import CallbackContext, ConversationHandler
from telegram import Update, error, InlineKeyboardMarkup, InlineKeyboardButton

from admin_panel.utilities import get_categories_for_user, get_category_id_list, add_user_to_category, get_category_label_by_id, \
    remove_user_from_category, is_user_admin, get_users_by_category_id, admin_required


# Define command handlers
async def start(update, context):
    """Send a welcome message when /start is used if the user isn't an admin, otherwise show a welcome message for the admin panel. If the user isn't
    an admin, add them to the INTERESTED category."""
    # Show a welcome message to normal users
    if not is_user_admin(update.message.from_user.id):
        await update.message.reply_text(
            f"🤖 Hello, {update.message.from_user.first_name}! I'm a bot that helps you contact CAN support. Use /help to see what I can do.")
        add_user_to_category(str(update.message.from_user.id), '0')

    # Show admin panel welcome message to admins.
    else:
        await update.message.reply_text(
            f"🔰 Welcome to the admin panel, {update.message.from_user.first_name}! Use /help to see what I can do.")


async def show_help(update, context):
    """Show different help messages for admins and regular users."""
    if is_user_admin(update.message.from_user.id):
        help_message = """
📝 This bot is used to contact users. Currently it supports the following commands and functionalities:

/send <user id>: This command forwards a message to a single user given the user's ID. To select what message to forward, reply to the desired message with this command. If no user ID is given, the message is reflected back to the sender. If no message is replied to, a test message is sent instead. 📱

/setcategory: This command assigns a list of user ID's to the selected category. After replying to the user list with this command, select which category you would like to add the users to. This overwrites the existing list. 📈

/unsetcategory <user id>: This command removes a user with a given user ID from a category. After using this command, select which category you would like to remove the user from, or use this command in reply to a message to remove the sender from a category. 📈

/bulksend <user id>: This command sends a message to all users in a category, selected in a dialog after the command is used. 📈
"""
    else:
        help_message = """
📝 This bot is used to contact users. Select your desired option after using the /start command."""

    await update.message.reply_text(help_message)


@admin_required
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


@admin_required
async def bulk_send(update: Update, context: CallbackContext):
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
            context.user_data['bulk_send_message_id'] = update.message.reply_to_message.message_id
            context.user_data['bulk_send_from_chat_id'] = update.effective_chat.id

            return "FINALIZE_BULK_SEND"

        else:
            # Confirmation message
            await update.message.reply_text(
                f'⚠️ Error: Bulk sending can only be used in reply to a message. Please make sure you reply to a message with the command '
                f'and try again.')

            return ConversationHandler.END

    except error.BadRequest as e:
        await context.bot.send_message(update.effective_chat.id, '⚠️ Error: User ID might be invalid or bot has no permission: {str(e)}')

    except Exception as e:
        await context.bot.send_message(update.effective_chat.id, f'🚨 An error occurred: {str(e)}')

    return ConversationHandler.END


async def finalize_bulk_send(update: Update, context: CallbackContext):
    try:
        # Get the category id from the callback query and the message id from the user_data object
        category_id = update.callback_query.data
        context.user_data['bulk_send_category_id'] = category_id

        await update.callback_query.answer(f'✅ Category {get_category_label_by_id(category_id)} selected successfully!')

        # Edit the last message sent by the bot to indicate the success and to not show the keyboard
        await update.callback_query.edit_message_text(
            f'✅ Category {get_category_label_by_id(category_id)} selected successfully. Are you sure you want to send the message to all'
            f' {len(get_users_by_category_id(category_id))} users in this category? Type /yes to confirm and /cancel to cancel the operation.')

        return 'CONFIRM_BULK_SEND'

    except error.BadRequest as e:
        await context.bot.send_message(update.effective_chat.id, f'⚠️ Error: User ID might be invalid or bot has no permission: {str(e)}')

    except Exception as e:
        await context.bot.send_message(update.effective_chat.id, f'🚨 An error occurred: {str(e)}')

    return ConversationHandler.END


async def confirm_bulk_send(update: Update, context: CallbackContext):
    try:
        category_id = context.user_data['bulk_send_category_id']
        message_id = context.user_data['bulk_send_message_id']
        from_chat_id = context.user_data['bulk_send_from_chat_id']

        # Send the message to every user in the category
        users_in_category = get_users_by_category_id(category_id)
        print(users_in_category)
        for chat_id in users_in_category:
            try:
                await context.bot.copy_message(chat_id=chat_id, from_chat_id=from_chat_id, message_id=message_id)

            except Exception as e:
                await context.bot.send_message(update.effective_chat.id, f'⚠️ Error: Message sending failed for user ID {chat_id}: {str(e)}')

        await update.message.reply_text(f'✅ Message sent to all users in category {get_category_label_by_id(category_id)} successfully!')

        return ConversationHandler.END

    except error.BadRequest as e:
        await context.bot.send_message(update.effective_chat.id, f'⚠️ Error: User ID might be invalid or bot has no permission: {str(e)}')

    except Exception as e:
        await context.bot.send_message(update.effective_chat.id, f'🚨 An error occurred: {str(e)}')

    return ConversationHandler.END


@admin_required
async def unset_category(update: Update, context: CallbackContext):
    """Removes a user from a category."""

    try:
        # Get the target user ID from the sender
        try:
            target_user_id = update.message.text.split(' ')[1]
            context.user_data['target_user_id'] = target_user_id

        except IndexError:
            # If there is an IndexError, this means the user didn't specify a target user ID. Check if the command was used in reply to a message.
            if update.message.reply_to_message:
                target_user_id = str(update.message.reply_to_message.api_kwargs['forward_from']['id'])
                context.user_data['target_user_id'] = target_user_id

            else:
                # If the command wasn't used in reply to a message, show an error message
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
        await context.bot.send_message(update.effective_chat.id, f'⚠️ Error: User ID might be invalid or bot has no permission: {str(e)}')

    except Exception as e:
        await context.bot.send_message(update.effective_chat.id, f'🚨 An error occurred: {str(e)}')

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
        await context.bot.send_message(update.effective_chat.id, f'⚠️ Error: User ID might be invalid or bot has no permission: {str(e)}')

    except Exception as e:
        await context.bot.send_message(update.effective_chat.id, f'🚨 An error occurred: {str(e)}')

    # Clear the user_data object
    context.user_data.clear()

    return ConversationHandler.END


async def cancel_operation(update: Update, context: CallbackContext):
    try:
        await context.bot.send_message(update.message.chat_id, "❌ Operation canceled by the user.")
    except:
        # If the try block fails, that means the update was a callback query. In that case the effective chat id is the chat id of the user.
        await context.bot.send_message(update.callback_query.from_user.id, "❌ Operation canceled by the user.")

    # Clear the user_data object
    context.user_data.clear()
    return ConversationHandler.END
