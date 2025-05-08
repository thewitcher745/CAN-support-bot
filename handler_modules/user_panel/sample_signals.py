from dotenv import dotenv_values
from telegram import Update
from telegram.ext import CallbackContext, CallbackQueryHandler

from utils import fixed_keyboards
from utils.utilities import (
	get_chat_id,
	get_user_panel_message_id,
	log_user_interaction,
	log_user_action_detail,
	log_user_panel_errors,
)


@log_user_panel_errors
async def start_sample_signals(update: Update, context: CallbackContext):
	"""
	Handle the sample signals button press in the user panel.
	Shows the sample signals selection menu.
	"""
	user_id = get_chat_id(update)
	message_id = get_user_panel_message_id(
		'SAMPLE_SIGNALS_SELECT_TYPE', user_id=str(user_id)
	)
	user_panel_messages_channel_id = dotenv_values('.env.secret')[
		'USER_PANEL_MESSAGE_CHANNEL_ID'
	]

	# Use the sample signals keyboard
	keyboard = fixed_keyboards.SAMPLE_SIGNALS_SELECT_TYPE

	await update.callback_query.answer()

	try:
		await context.bot.copy_message(
			from_chat_id=user_panel_messages_channel_id,
			message_id=message_id,
			chat_id=user_id,
			reply_markup=keyboard,
		)

		await update.callback_query.delete_message()

	except Exception as e:
		# Handle any errors
		print(f'Error in sample_signals handler: {e}')


@log_user_interaction
@log_user_panel_errors
async def get_signal_type(update: Update, context: CallbackContext):
	"""
	Handle the selection of a sample signal type (CAN_BAG or FUTURES).
	Shows the available signals for the selected type.
	"""
	user_id = get_chat_id(update)
	signal_type = update.callback_query.data.removeprefix('SAMPLE_SIGNALS_')
	log_user_action_detail(update, f'SIGNAL_TYPE_{signal_type}')
	context.user_data['signal_type'] = signal_type

	# Get the message ID for this signal type
	message_id = get_user_panel_message_id(
		update.callback_query.data, user_id=str(user_id)
	)
	user_panel_messages_channel_id = dotenv_values('.env.secret')[
		'USER_PANEL_MESSAGE_CHANNEL_ID'
	]

	await update.callback_query.answer()

	await context.bot.copy_message(
		from_chat_id=user_panel_messages_channel_id,
		message_id=message_id,
		chat_id=user_id,
		reply_markup=fixed_keyboards.create_sample_signals_pair_select_keyboard(
			signal_type
		),
	)

	await update.callback_query.delete_message()


@log_user_panel_errors
async def get_signal_message_id(update: Update, context: CallbackContext):
	"""
	Handle the selection of a specific sample signal.
	Shows the selected signal message.
	"""
	user_id = get_chat_id(update)
	# The callback data is the message ID of the sample signal
	callback_data = update.callback_query.data

	# Extract signal type and message ID from callback data
	# Format: SAMPLE_SIGNAL_TYPE_MESSAGEID:
	message_id = int(callback_data.split(':')[1])

	sample_signals_channel_id = dotenv_values('.env.secret')[
		'SAMPLE_SIGNALS_CHANNEL_ID'
	]

	await update.callback_query.answer()
	# Get the signal type from the callback query
	signal_type = callback_data.split(':')[0]
	keyboard = (
		fixed_keyboards.SAMPLE_SIGNAL_CAN_BAG
		if signal_type == 'CAN_BAG'
		else fixed_keyboards.SAMPLE_SIGNAL_FUTURES
	)

	await context.bot.copy_message(
		from_chat_id=sample_signals_channel_id,
		message_id=message_id,
		chat_id=user_id,
		reply_markup=keyboard,
	)

	await update.callback_query.delete_message()


start_sample_signals = CallbackQueryHandler(
	callback=start_sample_signals, pattern='SAMPLE_SIGNALS_SELECT_TYPE'
)
get_sample_signal_type = CallbackQueryHandler(
	callback=get_signal_type,
	pattern='^(SAMPLE_SIGNALS_CAN_BAG|SAMPLE_SIGNALS_FUTURES)$',
)
get_sample_signal_id = CallbackQueryHandler(
	callback=get_signal_message_id, pattern='^(CAN_BAG|FUTURES):[0-9]+'
)

sample_signal_handlers = [
	start_sample_signals,
	get_sample_signal_type,
	get_sample_signal_id,
]
