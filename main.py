from telegram.ext import Application, CommandHandler, ConversationHandler, CallbackQueryHandler
import logging
from dotenv import dotenv_values

from admin_panel import basic_handlers
from admin_panel.handler_modules import set_category
from admin_panel.handler_modules import bulk_send
from admin_panel.handler_modules import send_message

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
    application.add_handler(CommandHandler('start', basic_handlers.start))
    application.add_handler(CommandHandler('help', basic_handlers.show_help))
    application.add_handler(CommandHandler('send', send_message.send_message))
    application.add_handler(ConversationHandler(
        entry_points=[CommandHandler('bulksend', bulk_send.get_message)],
        states={'GET_CATEGORY_ID': [CallbackQueryHandler(bulk_send.get_category_id)],
                'CONFIRM_BULK_SEND': [CallbackQueryHandler(bulk_send.confirm)]},
        fallbacks=[CommandHandler('cancel', basic_handlers.cancel_operation)]
    ))
    application.add_handler(ConversationHandler(
        entry_points=[CommandHandler('setcategory', set_category.get_user_list)],
        states={'GET_CATEGORY_ID_TO_SET': [CallbackQueryHandler(set_category.get_category_id)],
                'CONFIRM_SET_CATEGORY': [CallbackQueryHandler(callback=set_category.confirm)]},
        fallbacks=[CommandHandler('cancel', basic_handlers.cancel_operation)]
    ))

    # Start the bot
    application.run_polling()


if __name__ == '__main__':
    main()
