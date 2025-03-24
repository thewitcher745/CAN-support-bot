from telegram.ext import CallbackContext, ConversationHandler
from telegram import Update
from telegram.error import BadRequest

from utils import fixed_keyboards
from utils.strings import (
	ADMIN_WELCOME,
	ADMIN_WELCOME_BACK,
	USER_WELCOME,
	USER_WELCOME_BACK,
	ADMIN_HELP,
	USER_HELP,
	OPERATION_CANCELED,
)
from utils.utilities import (
	add_user_to_category,
	is_user_admin,
	get_chat_id,
	get_update_type,
	handle_telegram_errors,
	register_user_start,
)


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
				USER_WELCOME.format(name=update.message.from_user.first_name),
				reply_markup=fixed_keyboards.USER_PANEL_MAIN,
			)
		else:
			# Handle callback query for returning users
			await update.callback_query.answer()

			# If the edit fails, that means the message probably is a media message with a caption. Remove the media.
			try:
				await update.callback_query.edit_message_text(
					USER_WELCOME_BACK, reply_markup=fixed_keyboards.USER_PANEL_MAIN
				)
			except BadRequest:
				await update.callback_query.answer()
				await context.bot.send_message(
					chat_id=chat_id,
					text=USER_WELCOME_BACK,
					reply_markup=fixed_keyboards.USER_PANEL_MAIN,
				)
				await update.callback_query.delete_message()

		# Add user to interested category
		add_user_to_category(str(chat_id), '0')

	# Handle admin users
	else:
		if update_type == 'MESSAGE':
			await update.message.reply_text(
				ADMIN_WELCOME.format(name=update.message.from_user.first_name),
				reply_markup=fixed_keyboards.ADMIN_PANEL_MAIN,
			)
		else:
			await update.callback_query.answer()
			await update.callback_query.edit_message_text(
				ADMIN_WELCOME_BACK, reply_markup=fixed_keyboards.ADMIN_PANEL_MAIN
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

	help_message = ADMIN_HELP if is_user_admin(chat_id) else USER_HELP

	if update_type == 'MESSAGE':
		await update.message.reply_text(
			help_message, reply_markup=fixed_keyboards.RETURN_TO_MAIN_MENU
		)
	else:
		await update.callback_query.answer()
		await update.callback_query.edit_message_text(
			help_message, reply_markup=fixed_keyboards.RETURN_TO_MAIN_MENU
		)


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
			OPERATION_CANCELED,
			reply_markup=fixed_keyboards.RETURN_TO_MAIN_MENU,
		)
	except (BadRequest, AttributeError):
		# Handle as callback query if message update fails
		await update.callback_query.edit_message_text(
			OPERATION_CANCELED, reply_markup=fixed_keyboards.RETURN_TO_MAIN_MENU
		)

	# Clear user data and end conversation
	context.user_data.clear()
	return ConversationHandler.END
