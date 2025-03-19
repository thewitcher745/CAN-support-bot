from telegram.ext import CallbackContext, ConversationHandler
from telegram import Update

from admin_panel import fixed_keyboards
from admin_panel.utilities import add_user_to_category, is_user_admin, get_chat_id, get_update_type, handle_telegram_errors


# Define command handlers
@handle_telegram_errors
async def start(update: Update, context: CallbackContext):
    """Send a welcome message when /start is used if the user isn't an admin, otherwise show a welcome message for the admin panel. If the user isn't
    an admin, add them to the INTERESTED category."""
    # Show a welcome message to normal users

    chat_id = get_chat_id(update)
    update_type = get_update_type(update)

    if not is_user_admin(chat_id):
        if update_type == 'MESSAGE':
            await update.message.reply_text(
                f'🤖 Hello, {update.message.from_user.first_name}! I\'m a bot that helps you contact CAN support. Use /help to see what I can do.')

        else:
            await update.callback_query.answer()

            await update.callback_query.edit_message_text(
                f'🤖 Welcome back! I\'m a bot that helps you contact CAN support. Use /help to see what I can do.')

        add_user_to_category(str(chat_id), '0')

    # Show admin panel welcome message to admins.
    else:
        if update_type == 'MESSAGE':
            await update.message.reply_text(
                f'🔰 Welcome to the admin panel, {update.message.from_user.first_name}! Use /help to see what I can do, or use '
                f'the "Show help" button below.',
                reply_markup=fixed_keyboards.ADMIN_PANEL_MAIN)

        else:
            await update.callback_query.answer()

            await update.callback_query.edit_message_text(
                f'🔰 Welcome back to the admin panel! Use /help to see what I can do, or use '
                f'the "Show help" button below.',
                reply_markup=fixed_keyboards.ADMIN_PANEL_MAIN)


@handle_telegram_errors
async def show_help(update: Update, context: CallbackContext):
    """Show different help messages for admins and regular users."""

    chat_id = get_chat_id(update)
    update_type = get_update_type(update)

    if is_user_admin(chat_id):
        help_message = """
📝 This bot is used to contact users. Currently it supports the following commands and functionalities:

/send <user id>: This command forwards a message to a single user given the user's ID. To select what message to forward, reply to the desired message with this command. If no user ID is given, the message is reflected back to the sender. If no message is replied to, a test message is sent instead. 📱

/setcategory: This command assigns a list of user ID's to the selected category. After replying to the user list with this command, select which category you would like to add the users to. This overwrites the existing list. 📈

/addtocategory: This command adds a list of ID's to the selected category. After replying to the user list with this command, select which category you would like to add the users to. 📈

/bulksend <user id>: This command sends a message to all users in a category, selected in a dialog after the command is used. 📈
"""
    else:
        help_message = """
📝 This bot is used to contact users. Select your desired option after using the /start command."""

    if update_type == 'MESSAGE':
        await update.message.reply_text(help_message, reply_markup=fixed_keyboards.RETURN_TO_MAIN_MENU)
    else:
        await update.callback_query.answer()

        await update.callback_query.edit_message_text(help_message, reply_markup=fixed_keyboards.RETURN_TO_MAIN_MENU)


@handle_telegram_errors
async def cancel_operation(update: Update, context: CallbackContext):
    try:
        await context.bot.send_message(update.message.chat_id, "❌ Operation canceled by the user.", reply_markup=fixed_keyboards.RETURN_TO_MAIN_MENU)
    except:
        # If the try block fails, that means the update was a callback query. In that case the effective chat id is the chat id of the user.
        await update.callback_query.edit_message_text("❌ Operation canceled by the user.", reply_markup=fixed_keyboards.RETURN_TO_MAIN_MENU)

    # Clear the user_data object
    context.user_data.clear()
    return ConversationHandler.END
