# Telegram Message Sender Bot

A simple Telegram bot that allows sending messages to specific users by their user ID.

## Features

- Send messages to any Telegram user using their user ID (Provided they have given the bot the necessary permission)
- Fallback to sending test messages back to the sender
- Error handling for invalid user IDs or permission issues

## Prerequisites

- Python 3.7+
- A Telegram bot token (obtained from [@BotFather](https://t.me/botfather))

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/telegram-message-sender-bot.git
   cd telegram-message-sender-bot
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

3. To send a message to a specific user, use:
   ```
   /send user_id
   ```
   Where `user_id` is the Telegram user ID of the recipient.

4. If no user ID is provided, the bot will send the test message back to you.

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
