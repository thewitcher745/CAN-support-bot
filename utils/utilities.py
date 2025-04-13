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


def add_user_to_category(user_id, category_id=None, category_label=None):
	"""
	Add a user to a specific category if they're not already in it.

	If only the category_id is provided, the user is added to the category with that ID.
	If only the category_label is provided, the user is added to the category with that label.
	If the category with the given label doesn't exist, it is created.
	If the category with the given label already exists, the user is added to it.
	If the user is already in the category, no action is taken.

	If the category is not INTERESTED (category_id='0'), the user will be removed from
	the INTERESTED category.

	Args:
	    user_id (int): The ID of the user to add
	    category_id (int, optional): The ID of the category to add the user to
	    category_label (str, optional): The label of the category to add the user to

	Raises:
	    ValueError: If neither category_id nor category_label is provided
	"""
	with open('data/user_lists.json', 'r') as f:
		user_lists = json.load(f)

	# If category_id is provided, use it to find the category
	if category_id is not None:
		category = user_lists[locale].get(str(category_id))
		target_category_id = str(category_id)

	# If category_label is provided, find or create the category with that label
	elif category_label is not None:
		# Find the category with the given label
		category_id_found = None
		for cat_id, cat in user_lists[locale].items():
			if cat['label'] == category_label:
				category = cat
				category_id_found = cat_id
				break

		# If no category with the given label exists, create a new one
		if category_id_found is None:
			new_category_id = str(len(user_lists[locale]))
			user_lists[locale][new_category_id] = {'label': category_label, 'users': []}
			category = user_lists[locale][new_category_id]
			target_category_id = new_category_id
		else:
			target_category_id = category_id_found

	else:
		raise ValueError('Either category_id or category_label must be provided')

	# Only add if user isn't already in the category
	if user_id not in category['users']:
		category['users'].append(user_id)

		# If adding to a non-INTERESTED category, remove from INTERESTED
		if target_category_id != '0':
			# Remove from INTERESTED category if present
			interested_category = user_lists[locale].get('0')
			if interested_category and user_id in interested_category['users']:
				interested_category['users'].remove(user_id)

	with open('data/user_lists.json', 'w') as f:
		json.dump(user_lists, f, indent=4)


def remove_user_from_category(user_id, category_id):
	"""
	Remove a user from a specific category if they're in it.
	If after removal the user is not in any non-INTERESTED category,
	they will be added to the INTERESTED category (category_id='0').

	Args:
	    user_id: The ID of the user to remove
	    category_id: The ID of the category to remove the user from
	"""
	with open('data/user_lists.json', 'r') as f:
		user_lists = json.load(f)

	# Only remove if user is in the category
	if user_id in user_lists[locale][str(category_id)]['users']:
		user_lists[locale][str(category_id)]['users'].remove(user_id)

		# If we removed from a non-INTERESTED category, check if user should be added to INTERESTED
		if str(category_id) != '0':
			# Check if user is in any other non-INTERESTED category
			in_other_category = False
			for cat_id, cat in user_lists[locale].items():
				if cat_id != '0' and user_id in cat['users']:
					in_other_category = True
					break

			# If not in any other category, add to INTERESTED
			if not in_other_category:
				interested_category = user_lists[locale].get('0')
				if interested_category and user_id not in interested_category['users']:
					interested_category['users'].append(user_id)

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
	Add multiple users to a category, avoiding duplicates and removing them from
	INTERESTED if they were already in it.

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

		# If the user is in INTERESTED, remove them
		if user in user_lists[locale]['0']['users']:
			user_lists[locale]['0']['users'].remove(user)

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

			# If we removed from a non-INTERESTED category, check if user should be added to INTERESTED
			if category_id != '0':
				# Check if user is in any other non-INTERESTED category
				in_other_category = False
				for cat_id, cat in user_lists[locale].items():
					if cat_id != '0' and user in cat['users']:
						in_other_category = True
						break

				# If not in any other category, add to INTERESTED
				if not in_other_category:
					interested_category = user_lists[locale].get('0')
					if interested_category and user not in interested_category['users']:
						interested_category['users'].append(user)

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


def get_user_panel_message_id(message_name, user_id=None):
	"""
	Get the message ID for a user panel message by name.

	If the message ID in the user_panel_message_ids.json file is a dictionary with a 'DEFAULT' key,
	this function will check if the user is in any of the categories specified in the dictionary
	and return the corresponding message ID. If the user is not in any of the specified categories,
	the default message ID will be returned.

	Args:
	    message_name (str): The name of the message
	    user_id (str, optional): The ID of the user requesting the message

	Returns:
	    int or dict: The message ID or album info dictionary
	"""
	with open('data/user_panel_message_ids.json', 'r') as f:
		message_ids = json.load(f)

	message_id_value = message_ids[locale][message_name]

	# If the message ID is a dictionary with a DEFAULT key and user_id is provided,
	# check if the user is in any of the categories specified in the dictionary
	if (
		isinstance(message_id_value, dict)
		and 'DEFAULT' in message_id_value
		and user_id is not None
	):
		# Check each category in the dictionary (except DEFAULT)
		for category_label, category_message_id in message_id_value.items():
			if category_label != 'DEFAULT' and is_user_in_category(
				user_id, category_label
			):
				return category_message_id

		# If the user is not in any of the specified categories, return the default message ID
		return message_id_value['DEFAULT']

	# Otherwise, return the message ID as is
	return message_id_value


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


def is_valid_promo_code(promo_code: str) -> bool:
	"""
	Check if a promo code is valid.

	Args:
	    promo_code (str): The promo code to check

	Returns:
	    bool: True if the promo code is valid, False otherwise
	"""
	try:
		with open('data/promo_codes.json', 'r') as f:
			valid_promo_codes = json.load(f)
			return promo_code in valid_promo_codes

	except FileNotFoundError:
		# If the promo codes file does not exist, return False
		return False

	except json.JSONDecodeError:
		# If the promo codes file is not valid JSON, return False
		return False


def get_sample_signals_data():
	"""
	Load and return the sample signals data from the JSON file.
	This function should be called each time the data is needed to ensure it's always up-to-date.

	Returns:
	    dict: Dictionary containing sample signals data for the current locale
	"""
	with open('data/sample_signals.json', 'r', encoding='utf-8') as f:
		sample_signals = json.load(f)

	return sample_signals[locale]


def get_signals_for_type(signal_type: str) -> list:
	"""
	Get the signals for a specific signal type.

	Args:
	    signal_type (str): The type of signal to get the signals for

	Returns:
	    list: List of signals for the specified signal type
	"""
	sample_signals = get_sample_signals_data()

	# Get the signals for the specified signal type
	signals = sample_signals.get(signal_type, [])

	return signals


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
				f'⚠️ Error during execution of function {func.__name__}: {str(e)}',
			)

			if get_update_type(update) == 'CALLBACK_QUERY':
				await update.callback_query.answer()

		except Exception as e:
			# Handle all other errors
			await context.bot.send_message(
				update.effective_chat.id,
				f'🚨 An error occurred during execution of function {func.__name__}: {str(e)}',
			)

			if get_update_type(update) == 'CALLBACK_QUERY':
				await update.callback_query.answer()

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
	file_handler.setFormatter(
		logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
	)
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


def is_user_in_category(user_id, category_label):
	"""
	Check if a user is in a category with the specified label.

	Args:
	    user_id (str): The ID of the user to check
	    category_label (str): The label of the category to check

	Returns:
	    bool: True if the user is in the category, False otherwise
	"""
	user_id = str(user_id)

	with open('data/user_lists.json', 'r') as f:
		user_lists = json.load(f)

	# Find the category with the given label
	category = next(
		(cat for cat in user_lists[locale].values() if cat['label'] == category_label),
		None,
	)

	# If the category doesn't exist, the user is not in it
	if category is None:
		return False

	# Check if the user is in the category
	return user_id in category['users']


def is_user_in_non_interested_category(user_id):
	"""
	Check if a user is in any category other than INTERESTED (category_id='0').

	Args:
	    user_id (str): The ID of the user to check

	Returns:
	    bool: True if the user is in any non-INTERESTED category, False otherwise
	"""
	with open('data/user_lists.json', 'r') as f:
		user_lists = json.load(f)

	# Check if user is in any category other than INTERESTED (category_id='0')
	for category_id, category in user_lists[locale].items():
		print(category)
		if category_id != '0' and str(user_id) in category['users']:
			print('User is in a non-INTERESTED category')
			return True
	print('User is not in a non-INTERESTED category')
	return False
