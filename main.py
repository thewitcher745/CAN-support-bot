from telegram.ext import Application, CommandHandler
import logging
from dotenv import dotenv_values

from admin_panel.handlers import send_message

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Replace with your bot token from BotFather
TOKEN = dotenv_values('.env.secret')['BOT_TOKEN']


def main():
    application = Application.builder().token(TOKEN).read_timeout(30).write_timeout(30).build()

    # Commands
    application.add_handler(CommandHandler('send', send_message))

    # Start the bot
    application.run_polling()


if __name__ == '__main__':
    main()
