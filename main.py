from telegram.ext import Application, CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler, filters
import logging
from dotenv import dotenv_values

from admin_panel import basic_handlers
from admin_panel.handler_modules import set_category, add_to_category, bulk_send, send_message, remove_from_category

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Replace with your bot token from BotFather
TOKEN = dotenv_values('.env.secret')['BOT_TOKEN']


def main():
    application = Application.builder().token(
        TOKEN).read_timeout(30).write_timeout(30).build()

    # Start/Main menu
    application.add_handler(CommandHandler('start', basic_handlers.start))
    application.add_handler(CallbackQueryHandler(
        callback=basic_handlers.start, pattern='RETURN_TO_MAIN_MENU'))

    # Help menu
    application.add_handler(CommandHandler('help', basic_handlers.show_help))
    application.add_handler(CallbackQueryHandler(
        callback=basic_handlers.show_help, pattern='SHOW_HELP'))

    application.add_handler(CommandHandler('send', send_message.send_message))

    # Bulk sending
    application.add_handler(ConversationHandler(
        entry_points=[CommandHandler('bulksend', bulk_send.get_message_from_reply),
                      CallbackQueryHandler(callback=bulk_send.get_message_from_user_update, pattern='START_BULK_SEND')],
        states={'SET_MESSAGE_ID': [MessageHandler(filters=~filters.COMMAND, callback=bulk_send.set_message_id)],
                'GET_CATEGORY_ID': [CallbackQueryHandler(bulk_send.get_category_id)],
                'CONFIRM_BULK_SEND': [CallbackQueryHandler(bulk_send.confirm)]},
        fallbacks=[CommandHandler('cancel', basic_handlers.cancel_operation),
                   CallbackQueryHandler(basic_handlers.cancel_operation, pattern='CANCEL')]
    ))

    # Category setting
    application.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler(
                'setcategory', set_category.get_user_list_from_reply),
            CallbackQueryHandler(
                callback=set_category.get_user_list_from_user_update, pattern='START_SET_CATEGORY')
        ],
        states={
            'SET_USER_LIST': [MessageHandler(filters=~filters.COMMAND, callback=set_category.set_user_list)],
            'GET_CATEGORY_ID_TO_SET': [CallbackQueryHandler(set_category.get_category_id)],
            'CONFIRM_SET_CATEGORY': [CallbackQueryHandler(callback=set_category.confirm)]
        },
        fallbacks=[
            CommandHandler('cancel', basic_handlers.cancel_operation),
            CallbackQueryHandler(
                basic_handlers.cancel_operation, pattern='CANCEL')
        ]
    ))

    # Adding to category lists
    application.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('addtocategory',
                           add_to_category.get_user_list_from_reply),
            CallbackQueryHandler(
                callback=add_to_category.get_user_list_from_user_update, pattern='START_ADD_TO_CATEGORY')
        ],
        states={
            'SET_USER_LIST': [MessageHandler(filters=~filters.COMMAND, callback=add_to_category.set_user_list)],
            'GET_CATEGORY_ID_TO_ADD': [CallbackQueryHandler(add_to_category.get_category_id)],
            'CONFIRM_ADD_CATEGORY': [CallbackQueryHandler(callback=add_to_category.confirm)]
        },
        fallbacks=[
            CommandHandler('cancel', basic_handlers.cancel_operation),
            CallbackQueryHandler( 
                basic_handlers.cancel_operation, pattern='CANCEL')
        ]
    ))

    # Removing from category lists
    application.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('removefromcategory',
                           remove_from_category.get_user_list_from_reply),
            CallbackQueryHandler(
                callback=remove_from_category.get_user_list_from_user_update, pattern='START_REMOVE_FROM_CATEGORY')
        ],
        states={
            'SET_USER_LIST': [MessageHandler(filters=~filters.COMMAND, callback=remove_from_category.set_user_list)],
            'GET_CATEGORY_ID_TO_REMOVE': [CallbackQueryHandler(remove_from_category.get_category_id)],
            'CONFIRM_REMOVE_CATEGORY': [CallbackQueryHandler(callback=remove_from_category.confirm)]
        },
        fallbacks=[
            CommandHandler('cancel', basic_handlers.cancel_operation),
            CallbackQueryHandler(
                basic_handlers.cancel_operation, pattern='CANCEL')
        ]
    ))

    # Start the bot
    application.run_polling()


if __name__ == '__main__':
    main()
