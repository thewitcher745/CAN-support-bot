import json
from functools import wraps
from telegram import error, Update
from telegram.ext import ConversationHandler, CallbackContext
import os


def register_user_start(start_message):
    """
    Register a user's name, language, ID, and start time (current date and time) in a history json file. Create the file if it doesn't exist. Don't add the user if their
    ID is already in the history file.
    """
    history_file = 'admin_panel/data/user_history.json'

    # Create the history file if it doesn't exist
    if not os.path.exists(history_file):
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump([], f, indent=4, ensure_ascii=False)

    # Get the user's first name, last name, language, ID, and username
    user_first_name = start_message.from_user.first_name
    user_last_name = start_message.from_user.last_name
    user_language = start_message.from_user.language_code
    user_id = start_message.from_user.id
    user_username = start_message.from_user.username

    # Get the date the /start command was used
    start_date = start_message.date.isoformat()

    # Create a new user entry
    new_user = {
        'user_id': str(user_id),
        'first_name': user_first_name if user_first_name else "",
        'last_name': user_last_name if user_last_name else "",
        'language': user_language,
        'username': user_username if user_username else "",
        'start_time': start_date
    }

    # Load existing history if file exists
    if os.path.exists(history_file):
        with open(history_file, 'r', encoding='utf-8') as f:
            history = json.load(f)
    else:
        history = []

    # Add new user if not already present
    if not any(entry['user_id'] == str(user_id) for entry in history):
        history.append(new_user)

    # Write updated history back to file
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=4, ensure_ascii=False)


def get_user_lists():
    """Get the full user lists from the JSON file."""
    with open('admin_panel/data/user_lists.json', 'r') as f:
        user_lists = json.load(f)

    return user_lists


def get_category_id_list():
    """Get the names and ID's of all categories."""
    user_lists = get_user_lists()
    category_id_list = []

    for category_id in user_lists.keys():
        label = user_lists[category_id]['label']
        category_id_list.append((category_id, label))

    return category_id_list


def get_categories_for_user(user_id):
    user_lists = get_user_lists()
    categories = []

    for category in user_lists.values():
        if user_id in category['users']:
            categories.append(category['label'])

    return categories


def add_user_to_category(user_id, category_id):
    """Add the user with ID user_id to category with ID category_id, if the user already exists in that list, do nothing."""
    user_lists = get_user_lists()

    if user_id in user_lists[category_id]['users']:
        return

    user_lists[category_id]['users'].append(user_id)

    with open('admin_panel/data/user_lists.json', 'w') as f:
        json.dump(user_lists, f, indent=4)


def remove_user_from_category(user_id, category_id):
    """Remove the user with ID user_id from category with ID category_id, if the user does not exist in that list, do nothing."""
    user_lists = get_user_lists()

    if user_id not in user_lists[category_id]['users']:
        return

    user_lists[category_id]['users'].remove(user_id)

    with open('admin_panel/data/user_lists.json', 'w') as f:
        json.dump(user_lists, f, indent=4)


def get_category_label_by_id(category_id):
    """Get the label of a category given its ID."""
    user_lists = get_user_lists()
    return user_lists[category_id]['label']


def get_users_by_category_id(category_id):
    user_lists = get_user_lists()
    return user_lists[category_id]['users']


def set_category_user_list(category_id, user_list):
    # Sets the list for a given category
    user_lists = get_user_lists()

    user_lists[category_id]['users'] = user_list

    with open('admin_panel/data/user_lists.json', 'w') as f:
        json.dump(user_lists, f, indent=4)


def add_user_list_to_category(category_id, user_list):
    # Adds a list of users to an existing list, removing duplicates
    user_lists = get_user_lists()

    for user in user_list:
        if user not in user_lists[category_id]['users']:
            user_lists[category_id]['users'].append(user)

    with open('admin_panel/data/user_lists.json', 'w') as f:
        json.dump(user_lists, f, indent=4)


def remove_user_list_from_category(category_id, user_list):
    # Removes a list of users from an existing list
    user_lists = get_user_lists()

    for user in user_list:
        if user in user_lists[category_id]['users']:
            user_lists[category_id]['users'].remove(user)

    with open('admin_panel/data/user_lists.json', 'w') as f:
        json.dump(user_lists, f, indent=4)


def is_user_admin(user_id):
    with open('admin_panel/data/admins.json', 'r') as f:
        admins = json.load(f)

    return user_id in admins['admins']


def admin_required(func):
    # A decorator which makes a function require admin privileges.

    async def wrapper(update, context):
        chat_id = get_chat_id(update)
        if not is_user_admin(chat_id):
            context.user_data.clear()
            return ConversationHandler.END
        return await func(update, context)

    return wrapper


def get_chat_id(update):
    try:
        chat_id = update.message.chat_id
    except:
        # If the try block fails, that means it wasn't a user command and instead was a callback query.
        chat_id = update.callback_query.from_user.id

    return chat_id


def get_update_type(update):
    # Get the update type, returns either "CALLBACK_QUERY" or "MESSAGE"
    try:
        chat_id = update.message.chat_id
        return 'MESSAGE'
    except:
        return 'CALLBACK_QUERY'


def handle_telegram_errors(func):
    """
    Decorator that handles common Telegram errors and cleans up user_data.
    Wraps async functions that take Update and CallbackContext as parameters.
    """
    @wraps(func)
    async def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        try:
            return await func(update, context, *args, **kwargs)
        except error.BadRequest as e:
            await context.bot.send_message(
                update.effective_chat.id,
                f'⚠️ Error: User ID might be invalid or bot has no permission: {str(e)}'
            )
        except Exception as e:
            await context.bot.send_message(
                update.effective_chat.id,
                f'🚨 An error occurred: {str(e)}'
            )

        context.user_data.clear()
        return ConversationHandler.END

    return wrapper
