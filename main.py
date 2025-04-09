from telegram.ext import (
	Application,
	CommandHandler,
	CallbackQueryHandler,
)
import logging

from handler_modules import basic_handlers
from handler_modules.admin_panel import (
	set_category,
	add_to_category,
	bulk_send,
	send_message,
	remove_from_category,
	export_history,
	send_user_logs,
	clear_user_logs,
)
from handler_modules.user_panel import promo_code, send_user_message, sample_signals
from utils.utilities import get_bot_token

# Enable logging
logging.basicConfig(
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def main():
	# Get the appropriate bot token based on locale
	token = get_bot_token()

	application = (
		Application.builder().token(token).read_timeout(30).write_timeout(30).build()
	)

	# Start/Main menu
	application.add_handler(CommandHandler('start', basic_handlers.start))
	application.add_handler(
		CallbackQueryHandler(
			callback=basic_handlers.start, pattern='RETURN_TO_MAIN_MENU'
		)
	)

	# Help menu
	application.add_handler(CommandHandler('help', basic_handlers.show_help))
	application.add_handler(
		CallbackQueryHandler(callback=basic_handlers.show_help, pattern='SHOW_HELP')
	)

	# application.add_handler(CommandHandler('send', send_message.send_message))

	application.add_handler(bulk_send.bulk_send_handler)
	application.add_handler(set_category.set_category_handler)
	application.add_handler(add_to_category.add_to_category_handler)
	application.add_handler(remove_from_category.remove_from_category_handler)
	application.add_handler(export_history.export_history_handler)
	application.add_handler(send_user_logs.send_user_logs_handler)
	application.add_handler(clear_user_logs.clear_user_logs_handler)

	# User panel handlers are multiple handlers, so we need to add them all
	application.add_handler(promo_code.check_promo_code_handler)

	for handler in sample_signals.sample_signal_handlers:
		application.add_handler(handler)

	for handler in send_user_message.send_user_message_handlers:
		application.add_handler(handler)

	# Start the bot
	application.run_polling()


if __name__ == '__main__':
	main()
