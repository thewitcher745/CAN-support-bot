"""
Clear User Logs Module

This module handles clearing user panel log files for the current locale.
The logs are stored in logs/user_panel_errors_{locale}.log
"""

import os
from telegram import Update
from telegram.ext import (
	CallbackContext,
	ConversationHandler,
	CallbackQueryHandler,
	CommandHandler,
)

from utils import fixed_keyboards
from utils.strings import (
	CLEAR_USER_LOGS_CONFIRM,
	CLEAR_USER_LOGS_SUCCESS,
	CLEAR_USER_LOGS_NO_FILE,
)
from utils.utilities import (
	admin_required,
	handle_telegram_errors,
)
from utils.config import Config
from handler_modules.basic_handlers import cancel_operation


@admin_required
@handle_telegram_errors
async def clear_user_logs_confirm(update: Update, context: CallbackContext):
	"""
	Handler to confirm clearing user panel log files.

	Shows a confirmation message to the admin before clearing the logs.

	Args:
		update (Update): The Telegram update object
		context (CallbackContext): The callback context object

	Returns:
		str: The next conversation state 'CONFIRM_CLEAR'
	"""
	# Define log file path based on current locale
	log_file = f'logs/user_panel_errors_{Config.get_locale().value}.log'

	# Check if log file exists
	if not os.path.exists(log_file):
		await update.callback_query.edit_message_text(
			CLEAR_USER_LOGS_NO_FILE,
			reply_markup=fixed_keyboards.ADMIN_RETURN_TO_MAIN_MENU,
		)

		await update.callback_query.answer()

		return ConversationHandler.END

	# Show confirmation prompt
	await update.callback_query.edit_message_text(
		CLEAR_USER_LOGS_CONFIRM.format(locale=Config.get_locale().value),
		reply_markup=fixed_keyboards.ADMIN_CONFIRMATION,
	)

	await update.callback_query.answer()

	return 'CONFIRM_CLEAR'


@admin_required
@handle_telegram_errors
async def clear_user_logs(update: Update, context: CallbackContext):
	"""
	Handler to clear user panel log files after confirmation.

	Deletes the log file for the current locale if it exists.

	Args:
		update (Update): The Telegram update object
		context (CallbackContext): The callback context object

	Returns:
		int: ConversationHandler.END on success
		Any: Result of cancel_operation() if not confirmed
	"""
	# Check if operation was confirmed
	if update.callback_query.data != 'CONFIRM':
		await update.callback_query.edit_message_text(
			'Operation canceled.',
			reply_markup=fixed_keyboards.ADMIN_RETURN_TO_MAIN_MENU,
		)

		await update.callback_query.answer()

		context.user_data.clear()

		return await cancel_operation(update, context)

	# Define log file path based on current locale
	log_file = f'logs/user_panel_errors_{Config.get_locale().value}.log'

	# Check if log file exists
	if not os.path.exists(log_file):
		await update.callback_query.edit_message_text(
			CLEAR_USER_LOGS_NO_FILE,
			reply_markup=fixed_keyboards.ADMIN_RETURN_TO_MAIN_MENU,
		)
		await update.callback_query.answer()

		context.user_data.clear()

		return ConversationHandler.END

	# Clear the log file contents
	open(log_file, 'w').close()

	# Show success message
	await update.callback_query.edit_message_text(
		CLEAR_USER_LOGS_SUCCESS,
		reply_markup=fixed_keyboards.ADMIN_RETURN_TO_MAIN_MENU,
	)

	await update.callback_query.answer()

	# Clean up user data
	context.user_data.clear()

	return ConversationHandler.END


clear_user_logs_handler = ConversationHandler(
	entry_points=[
		CallbackQueryHandler(
			callback=clear_user_logs_confirm, pattern='CLEAR_USER_LOGS'
		),
	],
	states={
		'CONFIRM_CLEAR': [
			CallbackQueryHandler(callback=clear_user_logs, pattern='CONFIRM')
		],
	},
	fallbacks=[
		CommandHandler('cancel', cancel_operation),
		CallbackQueryHandler(cancel_operation, pattern='CANCEL'),
	],
)
