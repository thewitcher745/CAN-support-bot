from telegram.ext import CallbackContext, ConversationHandler
from telegram import Update, error, InlineKeyboardMarkup, InlineKeyboardButton

from admin_panel.utilities import add_user_to_category, is_user_admin


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

/addtocategory: This command adds a list of ID's to the selected category. After replying to the user list with this command, select which category you would like to add the users to. 📈

/bulksend <user id>: This command sends a message to all users in a category, selected in a dialog after the command is used. 📈
"""
    else:
        help_message = """
📝 This bot is used to contact users. Select your desired option after using the /start command."""

    await update.message.reply_text(help_message)


async def cancel_operation(update: Update, context: CallbackContext):
    try:
        await context.bot.send_message(update.message.chat_id, "❌ Operation canceled by the user.")
    except:
        # If the try block fails, that means the update was a callback query. In that case the effective chat id is the chat id of the user.
        await update.callback_query.edit_message_text("❌ Operation canceled by the user.")

    # Clear the user_data object
    context.user_data.clear()
    return ConversationHandler.END
