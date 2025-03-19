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
- Fallback to sending messages back to the sender
- Error handling for invalid user IDs or permission issues

## Prerequisites

- Python 3.7+
- A Telegram bot token (obtained from [@BotFather](https://t.me/botfather))

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
   BOT_TOKEN=your_telegram_bot_token_here
   ```

4. Create required JSON files:

   Create `admin_panel/data/admins.json`:
   ```json
   {
     "admins": [
       admin_id_1,
       admin_id_2
     ]
   }
   ```

   Create `admin_panel/data/user_lists.json` with the desired categories (the 'INTERESTED' category is required):
   ```json
   {
       "0": {
           "label": "INTERESTED",
           "users": []
       },
       "1": {
           "label": "VIP",
           "users": []
       }
   }
   ```

## Usage

1. Start the bot:
   ```bash
   python main.py
   ```

2. In Telegram, start a conversation with your bot by sending the `/start` command.

3. Available commands:
   - `/help` - View guide on using the bot
   - `/send` - Send or forward a message to a user ID
   - `/admin` - Access admin panel (admin only)
   - `/setcategory` - Set a user's category (admin only)
   - `/unsetcategory` - Remove a user from a category (admin only)
   - `/addusers` - Add multiple users to a category (admin only)
   - `/removeusers` - Remove multiple users from a category (admin only)

## Admin Panel

The admin panel provides a keyboard interface for:
- Managing users in each category
- Adding/removing users from categories
- Sending messages to users in bulk
- Viewing the help

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
- Other exceptions that might occur during operation

## Logging

The bot uses Python's built-in logging module to provide information about its operation.