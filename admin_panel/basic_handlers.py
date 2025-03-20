from telegram.ext import CallbackContext, ConversationHandler
from telegram import Update

from admin_panel import fixed_keyboards
from admin_panel.utilities import (
    add_user_to_category,
    is_user_admin,
    get_chat_id,
    get_update_type,
    handle_telegram_errors,
    register_user_start
)


@handle_telegram_errors
async def start(update: Update, context: CallbackContext):
    """
    Handle the /start command for both regular users and admins.
    
    For regular users:
    - Sends a welcome message
    - Registers their start in user history
    - Adds them to the INTERESTED category
    
    For admins:
    - Shows admin panel welcome message with main menu

    Args:
        update (Update): The Telegram update object
        context (CallbackContext): The callback context object

    Returns:
        None
    """
    chat_id = get_chat_id(update)
    update_type = get_update_type(update)
    is_admin = is_user_admin(chat_id)

    # Handle regular users
    if not is_admin:
        if update_type == 'MESSAGE':
            # Register new user start and send welcome
            register_user_start(update.message)
                
            await update.message.reply_text(
                f'🤖 Hello, {update.message.from_user.first_name}! '
                'I\'m a bot that helps you contact CAN support. Use /help to see what I can do.'
            )
        else:
            # Handle callback query for returning users
            await update.callback_query.answer()
            await update.callback_query.edit_message_text(
                '🤖 Welcome back! I\'m a bot that helps you contact CAN support. '
                'Use /help to see what I can do.'
            )

        # Add user to interested category
        add_user_to_category(str(chat_id), '0')

    # Handle admin users
    else:
        if update_type == 'MESSAGE':
            await update.message.reply_text(
                f'🔰 Welcome to the admin panel, {update.message.from_user.first_name}! '
                'Use /help to see what I can do, or use the "Show help" button below.',
                reply_markup=fixed_keyboards.ADMIN_PANEL_MAIN
            )
        else:
            await update.callback_query.answer()
            await update.callback_query.edit_message_text(
                '🔰 Welcome back to the admin panel! Use /help to see what I can do, '
                'or use the "Show help" button below.',
                reply_markup=fixed_keyboards.ADMIN_PANEL_MAIN
            )


@handle_telegram_errors
async def show_help(update: Update, context: CallbackContext):
    """
    Show help message appropriate for the user's role (admin or regular user).

    The help message contains:
    - For admins: List of available commands and their usage
    - For regular users: Basic usage instructions

    Args:
        update (Update): The Telegram update object
        context (CallbackContext): The callback context object

    Returns:
        None
    """
    chat_id = get_chat_id(update)
    update_type = get_update_type(update)

    # Define help messages for different user roles
    if is_user_admin(chat_id):
        help_message = """
📝 This bot is used to contact users. Currently it supports the following commands and functionalities:

/send <user id>: This command forwards a message to a single user given the user's ID. To select what message to forward, reply to the desired message with this command. If no user ID is given, the message is reflected back to the sender. If no message is replied to, a test message is sent instead. 📱

/setcategory: This command assigns a list of user ID's to the selected category. After replying to the user list with this command, select which category you would like to add the users to. This overwrites the existing list. 📈

/addtocategory: This command adds a list of ID's to the selected category. After replying to the user list with this command, select which category you would like to add the users to. 📈

/removefromcategory: This command removes a list of ID's from the selected category. After replying to the user list with this command, select which category you would like to remove the users from. 📈

/bulksend <user id>: This command sends a message to all users in a category, selected in a dialog after the command is used. 📈
"""
    else:
        help_message = """
📝 This bot is used to contact users. Select your desired option after using the /start command."""

    # Send help message based on update type
    if update_type == 'MESSAGE':
        await update.message.reply_text(
            help_message,
            reply_markup=fixed_keyboards.RETURN_TO_MAIN_MENU
        )
    else:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            help_message,
            reply_markup=fixed_keyboards.RETURN_TO_MAIN_MENU
        )


@handle_telegram_errors
async def cancel_operation(update: Update, context: CallbackContext):
    """
    Cancel the current operation and return to main menu.

    Handles both message and callback query updates, clears user data
    and returns conversation end state.

    Args:
        update (Update): The Telegram update object
        context (CallbackContext): The callback context object

    Returns:
        int: ConversationHandler.END to end the conversation
    """
    try:
        # Try handling as message update
        await context.bot.send_message(
            update.message.chat_id,
            "❌ Operation canceled by the user.",
            reply_markup=fixed_keyboards.RETURN_TO_MAIN_MENU
        )
    except:
        # Handle as callback query if message update fails
        await update.callback_query.edit_message_text(
            "❌ Operation canceled by the user.",
            reply_markup=fixed_keyboards.RETURN_TO_MAIN_MENU
        )

    # Clear user data and end conversation
    context.user_data.clear()
    return ConversationHandler.END
