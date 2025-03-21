import json
import csv
import os
from telegram import Update
from telegram.ext import CallbackContext

from utils.fixed_keyboards import RETURN_TO_MAIN_MENU
from utils.utilities import get_chat_id, get_categories_for_user, get_category_label_by_id


async def export_history(update: Update, context: CallbackContext):
    """
    Handler to export user history to CSV and send it to the admin.
    
    Reads user history from JSON file, converts it to CSV format with user details
    and their associated categories, then sends the CSV file to the admin via Telegram.
    
    Args:
        update (Update): The incoming update from Telegram
        context (CallbackContext): The callback context
        
    Returns:
        None
        
    Raises:
        Exception: If there's an error during file operations or sending messages
    """
    try:
        # Get chat ID for the current admin user
        chat_id = get_chat_id(update)

        # Define file paths
        history_file = 'admin_panel/data/user_history.json'
        csv_path = f'admin_panel/data/user_history.csv'

        # Read user history from JSON
        with open(history_file, 'r', encoding='utf-8') as f:
            user_history = json.load(f)

        # Define CSV structure and write data
        fieldnames = [
            'user_id', 'first_name', 'last_name',
            'language', 'username', 'start_time', 'categories'
        ]
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            # Process each user entry
            for entry in user_history:
                # Get categories for current user
                categories_containing_user = get_categories_for_user(
                    entry.get('user_id', '')
                )
                
                # Write user data to CSV
                writer.writerow({
                    'user_id': entry.get('user_id', ''),
                    'first_name': entry.get('first_name', ''),
                    'last_name': entry.get('last_name', ''),
                    'language': entry.get('language', ''),
                    'username': entry.get('username', ''),
                    'start_time': entry.get('start_time', ''),
                    'categories': ' | '.join(categories_containing_user)
                })

        # Send CSV file to admin
        with open(csv_path, 'rb') as file:
            await context.bot.send_document(
                chat_id=chat_id,
                document=file,
                filename='user_history.csv'
            )

        # Send success confirmation
        await context.bot.send_message(
            chat_id=chat_id,
            text='✅ User history has been successfully exported to CSV!',
            reply_markup=RETURN_TO_MAIN_MENU
        )

        # Cleanup temporary CSV file
        os.remove(csv_path)

        # Acknowledge the callback query
        await update.callback_query.answer()

    except Exception as e:
        # Handle any errors during export process
        await update.callback_query.message.reply_text(
            f"Error exporting user history: {str(e)}",
            reply_markup=RETURN_TO_MAIN_MENU
        )
        await update.callback_query.answer()
