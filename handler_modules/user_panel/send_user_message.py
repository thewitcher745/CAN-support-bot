import json
from telegram import Update
from telegram.ext import CallbackContext, CallbackQueryHandler

from utils import fixed_keyboards
from utils.utilities import get_chat_id, get_user_panel_message_id
from dotenv import dotenv_values


async def send_user_message(update: Update, context: CallbackContext):
	"""
	Send a message to the user pressing the button in the user panel.
	"""
	user_id = get_chat_id(update)
	message_id = get_user_panel_message_id(update.callback_query.data)
	user_panel_messages_channel_id = dotenv_values('.env.secret')[
		'USER_PANEL_MESSAGE_CHANNEL_ID'
	]

	# Keyboard is different for different states
	if update.callback_query.data == 'RESULTS':
		keyboard = fixed_keyboards.MONTHLY_RESULTS
	elif update.callback_query.data == 'VIP_OFFERS':
		keyboard = fixed_keyboards.VIP_OFFERS
	else:
		keyboard = fixed_keyboards.RETURN_TO_MAIN_MENU

	await context.bot.copy_message(
		from_chat_id=user_panel_messages_channel_id,
		message_id=message_id,
		chat_id=user_id,
		reply_markup=keyboard,
	)

	await update.callback_query.delete_message()

	await update.callback_query.answer()


# The pattern for the handler should be all the keys in the user_panel_message_ids.json file
with open('data/user_panel_message_ids.json', 'r') as f:
	message_ids = json.load(f)

send_user_message_handlers = [
	CallbackQueryHandler(send_user_message, pattern=message_callback_query_data)
	for message_callback_query_data in message_ids.keys()
]
