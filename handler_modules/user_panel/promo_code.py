from telegram import (
	Update,
)
from telegram.ext import (
	ConversationHandler,
	CommandHandler,
	CallbackQueryHandler,
	MessageHandler,
	CallbackContext,
	filters,
)

from handler_modules.basic_handlers import cancel_operation
from utils import fixed_keyboards, strings
from utils.utilities import (
	is_valid_promo_code,
	add_user_to_category,
	log_user_interaction,
	log_user_action_detail,
)


@log_user_interaction
async def start_enter_promo_code(update: Update, context: CallbackContext):
	"""
	Start the conversation and prompt the user to enter a promo code.

	Args:
	        update (Update): The Telegram update object
	        context (CallbackContext): The Telegram context object

	Returns:
	        str: The next state in the conversation
	"""
	await update.callback_query.answer()

	await update.callback_query.edit_message_text(
		text=strings.PROMO_CODE_INPUT,
		reply_markup=fixed_keyboards.CANCEL_OPERATION,
	)

	return 'PROMO_CODE_INPUT'


@log_user_interaction
async def check_promo_code(update: Update, context: CallbackContext):
	# Get the promo code from the user's input
	promo_code = update.message.text.strip().upper()
	log_user_action_detail(update, f'PROMO_CODE_ENTERED_{promo_code}')
	user_id = str(update.effective_user.id)

	# Check if the promo code is valid
	if is_valid_promo_code(promo_code):
		# Add the user to a category with the same label as the promo code
		add_user_to_category(user_id, category_label=promo_code)

		await update.message.reply_text(
			text=strings.PROMO_CODE_VALID,
			reply_markup=fixed_keyboards.PROMO_CODE_VALID,
		)
	else:
		await update.message.reply_text(
			text=strings.PROMO_CODE_INVALID,
			reply_markup=fixed_keyboards.RETURN_TO_MAIN_MENU,
		)

	return ConversationHandler.END


check_promo_code_handler = ConversationHandler(
	entry_points=[
		CallbackQueryHandler(
			callback=start_enter_promo_code, pattern='START_ENTER_PROMO_CODE'
		)
	],
	states={
		'PROMO_CODE_INPUT': [
			MessageHandler(filters=~filters.COMMAND, callback=check_promo_code)
		]
	},
	fallbacks=[
		CommandHandler('cancel', cancel_operation),
		CallbackQueryHandler(cancel_operation, pattern='CANCEL'),
	],
)
