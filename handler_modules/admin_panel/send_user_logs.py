"""
Send User Logs Module

This module handles sending user panel log files for the current locale.
The logs are stored in logs/user_panel_errors_{locale}.log
"""

import os
from telegram import Update
from telegram.ext import (
	CallbackContext,
	ConversationHandler,
	CallbackQueryHandler,
)

from utils import fixed_keyboards
from utils.strings import (
	SEND_USER_LOGS_NO_FILE,
	SEND_USER_LOGS_SUCCESS,
)
from utils.utilities import (
	admin_required,
	handle_telegram_errors,
)
from utils.config import Config


@admin_required
@handle_telegram_errors
async def send_user_logs(update: Update, context: CallbackContext):
	"""
	Handler to send user panel log files.

	Sends the log file for the current locale if it exists.

	Args:
		update (Update): The Telegram update object
		context (CallbackContext): The callback context object

	Returns:
		int: ConversationHandler.END
	"""
	# Define log file path based on current locale
	log_file = f'logs/user_panel_errors_{Config.get_locale().value}.log'

	# Check if log file exists
	if not os.path.exists(log_file):
		await update.callback_query.edit_message_text(
			SEND_USER_LOGS_NO_FILE,
			reply_markup=fixed_keyboards.ADMIN_RETURN_TO_MAIN_MENU,
		)

		await update.callback_query.answer()

		return ConversationHandler.END

	# Send the log file
	with open(log_file, 'rb') as f:
		await update.callback_query.message.reply_document(
			document=f,
			filename=os.path.basename(log_file),
		)

	await context.bot.send_message(
		update.effective_chat.id,
		SEND_USER_LOGS_SUCCESS,
		reply_markup=fixed_keyboards.ADMIN_RETURN_TO_MAIN_MENU,
	)

	await update.callback_query.answer()

	return ConversationHandler.END


send_user_logs_handler = CallbackQueryHandler(
	callback=send_user_logs, pattern='SEND_USER_LOGS'
)
