from datetime import datetime
import json
from functools import wraps
import logging
from dotenv import dotenv_values
from telegram import error, Update
from telegram.ext import ConversationHandler, CallbackContext
import os
from utils.config import Config

locale = Config.get_locale().value


def get_bot_token() -> str:
	"""
	Get the appropriate bot token based on the current locale.

	Returns:
	    str: The bot token for the current locale

	Raises:
	    ValueError: If the token for the current locale is not found
	"""
	# Load environment variables
	env_vars = dotenv_values('.env.secret')

	token_key = f'BOT_TOKEN_{locale}'
	if token_key not in env_vars:
		raise ValueError(f'Bot token for locale {locale} not found in .env.secret')

	return env_vars[token_key]


def get_localized_message_id(message_name: str) -> int:
	"""
	Get a message ID based on the current locale and message name.

	Args:
		message_name: The name of the message to get the ID for

	Returns:
		The message ID for the current locale

	Raises:
		KeyError: If the message name doesn't exist for the current locale
	"""
	message_ids_file = 'data/user_panel_message_ids.json'

	with open(message_ids_file, 'r', encoding='utf-8') as f:
		message_ids = json.load(f)

	return message_ids[locale][message_name]


def register_user_start(start_message):
	"""
	Register a new user in the history JSON file in the correct locale when they first start using the bot.

	Args:
	    start_message: The message object containing user information from the /start command

	The function creates a history file if it doesn't exist, extracts user information like name,
	language, ID etc. and adds it to the history if the user isn't already registered.
	"""
	history_file = 'data/user_history.json'

	# Create the history file if it doesn't exist
	if not os.path.exists(history_file):
		with open(history_file, 'w', encoding='utf-8') as f:
			json.dump({'EN': [], 'TR': []}, f, indent=4, ensure_ascii=False)

	# Extract user information from the message
	user_first_name = start_message.from_user.first_name
	user_last_name = start_message.from_user.last_name
	user_language = start_message.from_user.language_code
	user_id = start_message.from_user.id
	user_username = start_message.from_user.username
	start_date = start_message.date.isoformat()

	# Create a new user entry with extracted information
	new_user = {
		'user_id': str(user_id),
		'first_name': user_first_name if user_first_name else '',
		'last_name': user_last_name if user_last_name else '',
		'language': user_language,
		'username': user_username if user_username else '',
		'start_time': start_date,
	}

	# Load existing history or create empty dict if file doesn't exist
	history = {'EN': [], 'TR': []}
	if os.path.exists(history_file):
		with open(history_file, 'r', encoding='utf-8') as f:
			history = json.load(f)

	# Add new user if not already present in either locale
	if len(history[locale]) == 0 or not any(
		entry['user_id'] == str(user_id) for entry in history[locale]
	):
		# Add to the appropriate locale
		history[locale].append(new_user)

		# Write updated history back to file
		with open(history_file, 'w', encoding='utf-8') as f:
			json.dump(history, f, indent=4, ensure_ascii=False)


def get_user_lists():
	"""
	Load and return the full user lists from the JSON file.

	Returns:
	    dict: Dictionary containing all user lists and their metadata for the current locale
	"""
	with open('data/user_lists.json', 'r') as f:
		user_lists = json.load(f)

	return user_lists[locale]


def get_category_id_list():
	"""
	Get a list of tuples containing category IDs and their labels.

	Returns:
	    list: List of tuples (category_id, label) for all categories
	"""
	user_lists = get_user_lists()
	return [
		(category_id, user_lists[category_id]['label'])
		for category_id in user_lists.keys()
	]


def get_categories_for_user(user_id):
	"""
	Get all categories that a user belongs to.

	Args:
	    user_id: The ID of the user to check

	Returns:
	    list: List of category labels the user belongs to
	"""
	user_lists = get_user_lists()
	return [
		category['label']
		for category in user_lists.values()
		if user_id in category['users']
	]


def add_user_to_category(user_id, category_id):
	"""
	Add a user to a specific category if they're not already in it.

	Args:
	    user_id: The ID of the user to add
	    category_id: The ID of the category to add the user to
	"""
	with open('data/user_lists.json', 'r') as f:
		user_lists = json.load(f)

	# Only add if user isn't already in the category
	if user_id not in user_lists[locale][category_id]['users']:
		user_lists[locale][category_id]['users'].append(user_id)

		with open('data/user_lists.json', 'w') as f:
			json.dump(user_lists, f, indent=4)


def remove_user_from_category(user_id, category_id):
	"""
	Remove a user from a specific category if they're in it.

	Args:
	    user_id: The ID of the user to remove
	    category_id: The ID of the category to remove the user from
	"""
	with open('data/user_lists.json', 'r') as f:
		user_lists = json.load(f)

	# Only remove if user is in the category
	if user_id in user_lists[locale][category_id]['users']:
		user_lists[locale][category_id]['users'].remove(user_id)

		with open('data/user_lists.json', 'w') as f:
			json.dump(user_lists, f, indent=4)


def get_category_label_by_id(category_id):
	"""
	Get the label of a category by its ID.

	Args:
	    category_id: The ID of the category

	Returns:
	    str: The label of the category
	"""
	user_lists = get_user_lists()
	return user_lists[category_id]['label']


def get_users_by_category_id(category_id):
	"""
	Get all users in a specific category.

	Args:
	    category_id: The ID of the category

	Returns:
	    list: List of user IDs in the category
	"""
	user_lists = get_user_lists()
	return user_lists[category_id]['users']


def set_category_user_list(category_id, user_list):
	"""
	Replace the entire user list for a category.

	Args:
	    category_id: The ID of the category to update
	    user_list: The new list of users
	"""
	with open('data/user_lists.json', 'r') as f:
		user_lists = json.load(f)

	user_lists[locale][category_id]['users'] = user_list

	with open('data/user_lists.json', 'w') as f:
		json.dump(user_lists, f, indent=4)


def add_user_list_to_category(category_id, user_list):
	"""
	Add multiple users to a category, avoiding duplicates.

	Args:
	    category_id: The ID of the category to add users to
	    user_list: List of user IDs to add
	"""
	with open('data/user_lists.json', 'r') as f:
		user_lists = json.load(f)

	# Add each user if they're not already in the category
	for user in user_list:
		if user not in user_lists[locale][category_id]['users']:
			user_lists[locale][category_id]['users'].append(user)

	with open('data/user_lists.json', 'w') as f:
		json.dump(user_lists, f, indent=4)


def remove_user_list_from_category(category_id, user_list):
	"""
	Remove multiple users from a category.

	Args:
	    category_id: The ID of the category to remove users from
	    user_list: List of user IDs to remove
	"""
	with open('data/user_lists.json', 'r') as f:
		user_lists = json.load(f)

	# Remove each user if they're in the category
	for user in user_list:
		if user in user_lists[locale][category_id]['users']:
			user_lists[locale][category_id]['users'].remove(user)

	with open('data/user_lists.json', 'w') as f:
		json.dump(user_lists, f, indent=4)


def is_user_admin(user_id):
	"""
	Check if a user has admin privileges.

	Args:
	    user_id: The ID of the user to check

	Returns:
	    bool: True if user is an admin, False otherwise
	"""
	with open('data/admins.json', 'r') as f:
		admins = json.load(f)
	return user_id in admins[locale]


def admin_required(func):
	"""
	Decorator that restricts function access to admin users only.

	Args:
	    func: The function to wrap with admin check

	Returns:
	    wrapper: The wrapped function that checks admin status
	"""

	async def wrapper(update, context):
		chat_id = get_chat_id(update)
		if not is_user_admin(chat_id):
			context.user_data.clear()
			return ConversationHandler.END
		return await func(update, context)

	return wrapper


def get_chat_id(update):
	"""
	Extract chat ID from either a message or callback query update.

	Args:
	    update: The Telegram update object

	Returns:
	    int: The chat ID
	"""
	try:
		# Try to get chat ID from message
		chat_id = update.message.chat_id
	except AttributeError:
		# If message doesn't exist, get from callback query
		chat_id = update.callback_query.from_user.id

	return chat_id


def get_user_panel_message_id(message_name):
	"""
	Get the message ID for a user panel message by name.

	Args:
	    message_name: The name of the message

	Returns:
	    int: The message ID
	"""
	with open('data/user_panel_message_ids.json', 'r') as f:
		message_ids = json.load(f)

	return message_ids[locale][message_name]


def get_update_type(update):
	"""
	Determine the type of Telegram update received.

	Args:
	    update: The Telegram update object

	Returns:
	    str: Either 'MESSAGE' or 'CALLBACK_QUERY'
	"""
	try:
		update.message.chat_id
		return 'MESSAGE'
	except AttributeError:
		return 'CALLBACK_QUERY'


def get_message_labels():
	"""
	Get the labels for all messages in the user panel.

	Returns:
	    dict: Dictionary containing all message labels
	"""
	with open('data/user_panel_message_ids.json', 'r') as f:
		message_ids = json.load(f)

	return message_ids[locale]


def handle_telegram_errors(func):
	"""
	Decorator that handles common Telegram errors and cleans up user data.

	Args:
	    func: The async function to wrap with error handling

	Returns:
	    wrapper: The wrapped function with error handling
	"""

	@wraps(func)
	async def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
		try:
			return await func(update, context, *args, **kwargs)
		except error.BadRequest as e:
			# Handle invalid user ID or permission errors
			await context.bot.send_message(
				update.effective_chat.id,
				f'⚠️ Error: User ID might be invalid or bot has no permission: {str(e)}',
			)
		except Exception as e:
			# Handle all other errors
			await context.bot.send_message(
				update.effective_chat.id, f'🚨 An error occurred: {str(e)}'
			)

		# Clean up and end conversation on error
		context.user_data.clear()
		return ConversationHandler.END

	return wrapper


def log_user_panel_errors(func):
	"""
	Decorator that logs errors occurring in user panel functions using the logger module.
	Logs are written to logs/user_panel_errors.log

	Args:
	    func: The async function to wrap with error logging

	Returns:
	    wrapper: The wrapped function with error logging
	"""
	logger = logging.getLogger(locale)
	
	# Create logs directory if it doesn't exist
	os.makedirs('logs', exist_ok=True)
	
	# Configure file handler
	file_handler = logging.FileHandler(f'logs/user_panel_errors_{locale}.log')
	file_handler.setFormatter(logging.Formatter(
		'%(asctime)s - %(levelname)s - %(message)s'
	))
	logger.addHandler(file_handler)

	@wraps(func)
	async def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
		try:
			return await func(update, context, *args, **kwargs)
		except Exception as e:
			logger.error(
				f'User panel error occurred in {func.__name__} for user {update.effective_user.id}: {str(e)}'
			)

	return wrapper
