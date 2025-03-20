import json
import csv
import os
from telegram import Update
from telegram.ext import CallbackContext

from admin_panel.fixed_keyboards import RETURN_TO_MAIN_MENU
from admin_panel.utilities import get_chat_id, get_categories_for_user, get_category_label_by_id


async def export_history(update: Update, context: CallbackContext):
    """Handler to export user history to CSV and send it to the admin."""

    try:
        chat_id = get_chat_id(update)

        # Read the user history JSON file
        history_file = 'admin_panel/data/user_history.json'
        with open(history_file, 'r', encoding='utf-8') as f:
            user_history = json.load(f)

        csv_path = f'admin_panel/data/user_history.csv'

        # Write data to CSV
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['user_id', 'first_name', 'last_name',
                          'language', 'username', 'start_time', 'categories']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for entry in user_history:
                # ID's of categories containing the user
                categories_containing_user = get_categories_for_user(
                    entry.get('user_id', ''))

                print(' | '.join(categories_containing_user))

                writer.writerow({
                    'user_id': entry.get('user_id', ''),
                    'first_name': entry.get('first_name', ''),
                    'last_name': entry.get('last_name', ''),
                    'language': entry.get('language', ''),
                    'username': entry.get('username', ''),
                    'start_time': entry.get('start_time', ''),
                    'categories': ' | '.join(categories_containing_user)
                })

        # Send the file to the user
        with open(csv_path, 'rb') as file:
            await context.bot.send_document(
                chat_id=chat_id,
                document=file,
                filename='user_history.csv'
            )

        # Send success message with return keyboard
        await context.bot.send_message(
            chat_id=chat_id,
            text='✅ User history has been successfully exported to CSV!',
            reply_markup=RETURN_TO_MAIN_MENU
        )

        # Clean up the file after sending
        os.remove(csv_path)

        # Answer the callback query
        await update.callback_query.answer()

    except Exception as e:
        await update.callback_query.message.reply_text(
            f"Error exporting user history: {str(e)}",
            reply_markup=RETURN_TO_MAIN_MENU
        )
        await update.callback_query.answer()
