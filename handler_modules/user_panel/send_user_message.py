from telegram import Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext, CallbackQueryHandler

from utils import fixed_keyboards
from utils.strings import MONTHLY_RESULTS_END
from utils.utilities import (
	get_chat_id,
	get_message_labels,
	get_user_panel_message_id,
	log_user_panel_errors,
)
from dotenv import dotenv_values


MONTH_NAMES = [
	'JANUARY',
	'FEBRUARY',
	'MARCH',
	'APRIL',
	'MAY',
	'JUNE',
	'JULY',
	'AUGUST',
	'SEPTEMBER',
	'OCTOBER',
	'NOVEMBER',
	'DECEMBER',
]


@log_user_panel_errors
async def send_user_message(update: Update, context: CallbackContext):
	"""
	Send a message to the user pressing the button in the user panel.
	"""
	user_id = get_chat_id(update)
	message_id = get_user_panel_message_id(
		update.callback_query.data, user_id=str(user_id)
	)
	user_panel_messages_channel_id = dotenv_values('.env.secret')[
		'USER_PANEL_MESSAGE_CHANNEL_ID'
	]

	# Handle RESULTS_P1 and RESULTS_P2 callbacks by updating the reply markup
	if update.callback_query.data == 'RESULTS_P1':
		await update.callback_query.edit_message_reply_markup(
			reply_markup=fixed_keyboards.RESULTS
		)
		await update.callback_query.answer()
		return
	elif update.callback_query.data == 'RESULTS_P2':
		await update.callback_query.edit_message_reply_markup(
			reply_markup=fixed_keyboards.RESULTS_P2
		)
		await update.callback_query.answer()
		return
	

	# Keyboard is different for different states
	if update.callback_query.data == 'RESULTS':
		keyboard = fixed_keyboards.RESULTS


	elif update.callback_query.data == 'OFFERS':
		keyboard = fixed_keyboards.OFFERS
	elif update.callback_query.data == 'HOW_IT_WORKS':
		keyboard = fixed_keyboards.HOW_IT_WORKS
	elif update.callback_query.data == 'SELECT_WALLET_ADDRESS':
		keyboard = fixed_keyboards.SELECT_WALLET_ADDRESS
	elif update.callback_query.data == 'SAMPLE_SIGNALS_SELECT_TYPE':
		keyboard = fixed_keyboards.SAMPLE_SIGNALS_SELECT_TYPE

	# If the user pressed a wallet address button
	elif update.callback_query.data.startswith('WALLET_'):
		keyboard = fixed_keyboards.SHOW_WALLET_ADDRESS

	# If the user pressed a monthly results button
	elif any(month in update.callback_query.data for month in MONTH_NAMES):
		keyboard = fixed_keyboards.SHOW_MONTHLY_RESULTS

	elif not (
		update.callback_query.data == 'SAMPLE_SIGNALS_SELECT_TYPE'
		or update.callback_query.data == 'CAN_BAG'
		or update.callback_query.data == 'FUTURES'
	):
		keyboard = fixed_keyboards.RETURN_TO_MAIN_MENU

	# Handle sample signals buttons
	else:
		await update.callback_query.answer()

	try:
		# Handle album messages
		if (
			isinstance(message_id, dict)
			and 'FIRST_ID' in message_id
			and 'ALBUM_LENGTH' in message_id
		):
			message_ids = list(
				range(
					message_id['FIRST_ID'],
					message_id['FIRST_ID'] + message_id['ALBUM_LENGTH'],
				)
			)

			await context.bot.copy_messages(
				from_chat_id=user_panel_messages_channel_id,
				message_ids=message_ids,
				chat_id=user_id,
			)

			await context.bot.send_message(
				chat_id=user_id,
				text=MONTHLY_RESULTS_END,
				reply_markup=keyboard,
			)

			await update.callback_query.delete_message()

		# Otherwise, it's a single message, either a single photo or a pure text message.
		else:
			await context.bot.copy_message(
				from_chat_id=user_panel_messages_channel_id,
				message_id=message_id,
				chat_id=user_id,
				reply_markup=keyboard,
			)

			await update.callback_query.delete_message()

	# This except block happens when there is a text-only message sent after a post containing photos
	except BadRequest:
		await context.bot.copy_message(
			from_chat_id=user_panel_messages_channel_id,
			message_id=message_id,
			chat_id=user_id,
			reply_markup=keyboard,
		)

		await update.callback_query.delete_message()

	await update.callback_query.answer()


# The pattern for the handler should be all the keys in the user_panel_message_ids.json file
message_ids = get_message_labels()

send_user_message_handlers = [
	CallbackQueryHandler(send_user_message, pattern=message_callback_query_data)
	for message_callback_query_data in message_ids.keys()
]
