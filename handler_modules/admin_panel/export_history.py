import json
import csv
import os
from telegram import Update
from telegram.ext import CallbackContext, CallbackQueryHandler

from utils import fixed_keyboards
from utils.strings import (
	EXPORT_HISTORY_ERROR,
)
from utils.utilities import (
	admin_required,
	get_categories_for_user,
	get_chat_id,
	handle_telegram_errors,
)
from utils.config import Config


@admin_required
@handle_telegram_errors
async def export_history(update: Update, context: CallbackContext):
	"""
	Handler to export user history to CSV and send it to the admin.

	Reads user history from JSON file, converts it to CSV format with user details
	and their associated categories, then sends the CSV file to the admin via Telegram.

	Args:
	    update (Update): The Telegram update object
	    context (CallbackContext): The callback context object

	Returns:
	    None
	"""
	try:
		# Get chat ID for the current admin user
		chat_id = get_chat_id(update)

		# Define file paths
		history_file = 'data/user_history.json'
		csv_path = 'data/user_history.csv'

		# Read user history from JSON
		with open(history_file, 'r', encoding='utf-8') as f:
			user_history = json.load(f)

		user_history = user_history[Config.get_locale().value]

		# Define CSV structure and write data
		fieldnames = [
			'user_id',
			'first_name',
			'last_name',
			'language',
			'username',
			'start_time',
			'categories',
		]

		# Get all possible categories from all users
		all_categories = set()
		for entry in user_history:
			categories = get_categories_for_user(entry.get('user_id', ''))
			all_categories.update(categories)

		# Update fieldnames to include individual category columns
		base_fields = [
			'user_id',
			'first_name',
			'last_name',
			'language',
			'username',
			'start_time',
		]
		fieldnames = base_fields + sorted(list(all_categories))

		with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			writer.writeheader()

			# Process each user entry
			for entry in user_history:
				# Get categories for current user
				categories_containing_user = get_categories_for_user(
					entry.get('user_id', '')
				)

				# Create row dict with base user data
				row = {
					'user_id': entry.get('user_id', ''),
					'first_name': entry.get('first_name', ''),
					'last_name': entry.get('last_name', ''),
					'language': entry.get('language', ''),
					'username': entry.get('username', ''),
					'start_time': entry.get('start_time', ''),
				}

				# Add category columns with 1/0 values
				for category in all_categories:
					row[category] = 1 if category in categories_containing_user else 0

				writer.writerow(row)

		# Send CSV file to admin
		with open(csv_path, 'rb') as file:
			await context.bot.send_document(
				chat_id=chat_id, document=file, filename='user_history.csv'
			)

		# Send success confirmation
		await context.bot.send_message(
			chat_id=chat_id,
			text='✅ User history has been successfully exported to CSV!',
			reply_markup=fixed_keyboards.ADMIN_RETURN_TO_MAIN_MENU,
		)

		# Cleanup temporary CSV file
		os.remove(csv_path)

		# Acknowledge the callback query
		await update.callback_query.answer()

	except Exception as e:
		# Handle any errors during export process
		await update.callback_query.message.reply_text(
			EXPORT_HISTORY_ERROR.format(error=str(e)),
			reply_markup=fixed_keyboards.ADMIN_RETURN_TO_MAIN_MENU,
		)
		await update.callback_query.answer()


export_history_handler = CallbackQueryHandler(
	callback=export_history, pattern='EXPORT_HISTORY'
)
