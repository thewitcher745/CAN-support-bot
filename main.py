from telegram.ext import Application, CommandHandler, ConversationHandler, CallbackQueryHandler
import logging
from dotenv import dotenv_values

from admin_panel.handlers import start, send_message, show_help, cancel_operation, unset_category, \
    finalize_unset_category, bulk_send, finalize_bulk_send, confirm_bulk_send
from admin_panel.handlers import set_category

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
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', show_help))
    application.add_handler(CommandHandler('send', send_message))
    application.add_handler(ConversationHandler(
        entry_points=[CommandHandler('bulksend', bulk_send)],
        states={'FINALIZE_BULK_SEND': [CallbackQueryHandler(finalize_bulk_send)],
                'CONFIRM_BULK_SEND': [CommandHandler('yes', confirm_bulk_send)]},
        fallbacks=[CommandHandler('cancel', cancel_operation)]
    ))
    application.add_handler(ConversationHandler(
        entry_points=[CommandHandler('setcategory', set_category.get_user_list)],
        states={'GET_CATEGORY_ID_TO_SET': [CallbackQueryHandler(set_category.get_category_id)],
                'CONFIRM_SET_CATEGORY': [CallbackQueryHandler(callback=set_category.confirm)]},
        fallbacks=[CommandHandler('cancel', cancel_operation)]
    ))
    application.add_handler(ConversationHandler(
        entry_points=[CommandHandler('unsetcategory', unset_category)],
        states={'FINALIZE_UNSET_CATEGORY': [CallbackQueryHandler(finalize_unset_category)]},
        fallbacks=[CommandHandler('cancel', cancel_operation)]
    ))

    # Start the bot
    application.run_polling()


if __name__ == '__main__':
    main()
