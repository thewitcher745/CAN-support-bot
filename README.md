# Telegram Message Sender Bot

A Telegram bot that allows users to send or forward messages to any Telegram user using their user ID, as well as categorizing users into different
lists for bulk messaging and managing user categories through an admin panel.

## Features

- Sends or forwards messages to any Telegram user using their user ID (Provided they have given the bot the necessary permission)
- Message forwarding is done anonymously, and is accomplished by replying to the message to be forwarded with the `/send` command
- Admin panel for managing user categories and lists
- Keyboard interface for easy category management
- Can set and unset categories for different users using their ID, using the /setcategory and /unsetcategory commands
- Admin-only commands for managing user lists and categories
- Export user history and categories to CSV
- Automatic user registration tracking
- Fallback to sending messages back to the sender
- Error handling for invalid user IDs or permission issues
- Multi-language support (English and Turkish)
- Language setting configurable via --locale runtime argument
- Separate bot instances for each language

## Prerequisites

- Python 3.7+
- Telegram bot tokens for each language (obtained from [@BotFather](https://t.me/botfather))

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/thewitcher745/CAN-support-bot
   cd CAN-support-bot
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env.secret` file in the project root directory:
   ```
   BOT_TOKEN_EN=your_english_bot_token_here
   BOT_TOKEN_TR=your_turkish_bot_token_here
   USER_PANEL_MESSAGE_CHANNEL_ID=your_channel_id_here
   ```

4. Create required JSON files:

   Create `data/admins.json`:
   ```json
   {
     "admins": {
       "EN": [admin_id_1, admin_id_2],
       "TR": [admin_id_1, admin_id_2]
     }
     "admins": {
       "EN": [admin_id_1, admin_id_2],
       "TR": [admin_id_1, admin_id_2]
     }
   }
   ```

   Create `data/user_lists.json` with the desired categories (the 'INTERESTED' category is required):
   ```json
   {
     "EN": {
     "EN": {
       "0": {
         "label": "INTERESTED",
         "users": []
       },
       "1": {
         "label": "VIP",
         "users": []
       }
     },
     "TR": {
       "0": {
         "label": "İLGİLENEN",
         "users": []
       },
       "1": {
         "label": "VIP",
         "users": []
       }
     }
   }
   ```

   The bot will automatically create `data/user_history.json` to track user registrations.

## Usage

1. Start the bot with desired locale (Defaults to EN if not provided):
1. Start the bot with desired locale (Defaults to EN if not provided):
   ```bash
   python main.py --locale EN  # For English
   python main.py --locale TR  # For Turkish
   python main.py --locale EN  # For English
   python main.py --locale TR  # For Turkish
   ```

2. In Telegram, start a conversation with your bot by sending the `/start` command.

3. Available commands:
   - `/start` - Start the bot and access main menu
   - `/help` - View guide on using the bot
   - `/bulksend` - Send a message to all users in a selected category (admin only)
   - `/setcategory` - Assign users to a category (admin only)
   - `/addtocategory` - Add users to an existing category (admin only)
   - `/removefromcategory` - Remove users from a category (admin only)

## Admin Panel

The admin panel provides a keyboard interface for:
- Managing users in each category
- Adding/removing users from categories
- Sending messages to users in bulk
- Exporting user history and categories
- Viewing the help

Note: The admin panel interface remains in English regardless of the selected language.

Note: The admin panel interface remains in English regardless of the selected language.

## User Tracking

The bot automatically tracks:
- User ID
- First name
- Last name
- Username
- Language preference
- Registration date
- Category memberships

This data can be exported to CSV format using the export history feature.

## Language Support

The bot supports two languages:
- English (EN)
- Turkish (TR)

The language is set at startup using the --locale argument (e.g., --locale EN or --locale TR) and remains consistent throughout the bot's lifecycle. The user interface (messages, keyboards, etc.) will be displayed in the selected language, while the admin panel remains in English.

Each language version runs as a separate bot instance using its own bot token, allowing for independent operation and user bases.

## How to Find a User ID

To find a Telegram user ID:

- Forward a message from the target user to [@userinfobot](https://t.me/userinfobot)
- Use another bot like [@getidsbot](https://t.me/getidsbot)

## Error Handling

The bot includes error handling for:

- Invalid user IDs
- Permission errors (when a user has blocked the bot)
- Admin authentication failures
- Invalid category operations
- File operation errors
- Other exceptions that might occur during operation

## Logging

The bot uses Python's built-in logging module to provide information about its operation, including:
- Command usage
- Error tracking
- User interactions
- Admin operations