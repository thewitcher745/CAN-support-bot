from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from utils.utilities import get_category_id_list

CONFIRMATION = InlineKeyboardMarkup(
	[
		[
			InlineKeyboardButton('✅ Yes', callback_data='CONFIRM'),
			InlineKeyboardButton('❌ Cancel', callback_data='CANCEL'),
		]
	]
)

CANCEL_OPERATION = InlineKeyboardMarkup(
	[[InlineKeyboardButton('❌ Cancel', callback_data='CANCEL')]]
)

CATEGORIES = InlineKeyboardMarkup(
	[
		[InlineKeyboardButton(user_category_label, callback_data=user_category_id)]
		for user_category_id, user_category_label in get_category_id_list()
	]
	+ [[InlineKeyboardButton('❌ Cancel', callback_data='CANCEL')]]
)

RETURN_TO_MAIN_MENU = InlineKeyboardMarkup(
	[
		[
			InlineKeyboardButton(
				'🔙 Main menu', callback_data='RETURN_TO_MAIN_MENU'
			)
		]
	]
)


ADMIN_PANEL_MAIN = InlineKeyboardMarkup(
	[
		[
			InlineKeyboardButton(
				'📝 Set category list', callback_data='START_SET_CATEGORY'
			)
		],
		[
			InlineKeyboardButton(
				'➕ Add to category list', callback_data='START_ADD_TO_CATEGORY'
			)
		],
		[
			InlineKeyboardButton(
				'➖ Remove from category list',
				callback_data='START_REMOVE_FROM_CATEGORY',
			)
		],
		[
			InlineKeyboardButton(
				'📨 Bulk message to category', callback_data='START_BULK_SEND'
			)
		],
		[
			InlineKeyboardButton(
				'📊 Export user history', callback_data='EXPORT_HISTORY'
			)
		],
		[InlineKeyboardButton('❓ Show help', callback_data='SHOW_HELP')],
	]
)

USER_PANEL_MAIN = InlineKeyboardMarkup(
	[
		[InlineKeyboardButton('💰 CAN VIP offers', callback_data='OFFERS')],
		[InlineKeyboardButton('📈 CAN VIP results', callback_data='RESULTS')],
		[InlineKeyboardButton('📞 Contact admin', url='https://t.me/CANSupport')],
	]
)

OFFERS = InlineKeyboardMarkup(
	[
		[
			InlineKeyboardButton(
				'💰 Get our wallet address', callback_data='SELECT_WALLET_ADDRESS'
			)
		],
		[
			InlineKeyboardButton(
				'🔙 Main menu', callback_data='RETURN_TO_MAIN_MENU'
			)
		],
	]
)

SELECT_WALLET_ADDRESS = InlineKeyboardMarkup(
	[
		[InlineKeyboardButton('💰 USDT TRC20', callback_data='WALLET_TRC20')],
		[InlineKeyboardButton('💰 USDT BEP20', callback_data='WALLET_BEP20')],
		[
			InlineKeyboardButton(
				'🔙 Main menu', callback_data='RETURN_TO_MAIN_MENU'
			),
			InlineKeyboardButton('🔙 Previous menu', callback_data='OFFERS'),
		],
	]
)

SHOW_WALLET_ADDRESS = InlineKeyboardMarkup(
	[
		[
			InlineKeyboardButton(
				'🔙 Main menu', callback_data='RETURN_TO_MAIN_MENU'
			),
			InlineKeyboardButton(
				'🔙 Previous menu', callback_data='SELECT_WALLET_ADDRESS'
			),
		]
	]
)

SHOW_MONTHLY_RESULTS = InlineKeyboardMarkup(
	[
		[
			InlineKeyboardButton(
				'🔙 Main menu', callback_data='RETURN_TO_MAIN_MENU'
			),
			InlineKeyboardButton('🔙 Previous menu', callback_data='RESULTS'),
		]
	]
)


RESULTS = InlineKeyboardMarkup(
	[
		[InlineKeyboardButton('📅 January 2025', callback_data='JANUARY_2025')],
		[InlineKeyboardButton('📅 February 2025', callback_data='FEBRUARY_2025')],
		[InlineKeyboardButton('📅 November 2024', callback_data='NOVEMBER_2024')],
		[
			InlineKeyboardButton(
				'🔙 Main menu', callback_data='RETURN_TO_MAIN_MENU'
			)
		],
	]
)
