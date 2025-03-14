# Telegram Message Sender Bot

A Telegram bot that allows users to send or forward messages to any Telegram user using their user ID, as well as categorizing users into different
lists for (TBD) bulk messaging.

## Features

- Sends or forwards messages to any Telegram user using their user ID (Provided they have given the bot the necessary permission)
- Message forwarding is done anonymously, and is accomplished by replying to the message to be forwarded with the `/send` command.
- Can set and unset categories for different users using their ID, using the /setcategory and /unsetcategory commands.
- Fallback to sending messages back to the sender.
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

## Usage

1. Start the bot:
   ```bash
   python main.py
   ```

2. In Telegram, start a conversation with your bot by sending the `/start` command.

3. Use the /help command to view a guide on using the bot.

## How to Find a User ID

To find a Telegram user ID:

- Forward a message from the target user to [@userinfobot](https://t.me/userinfobot)
- Use another bot like [@getidsbot](https://t.me/getidsbot)

## Error Handling

The bot includes error handling for:

- Invalid user IDs
- Permission errors (when a user has blocked the bot)
- Other exceptions that might occur during operation

## Logging

The bot uses Python's built-in logging module to provide information about its operation.
