"""
Keyboard constants for all bot buttons and layouts.
User keyboards are localized (EN/TR), admin keyboards are English-only.
"""

from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from utils.utilities import get_category_id_list

# User Buttons (Localized)
EN_BUTTONS = {
	# Main Menu
	'OFFERS': '💰 CAN VIP offers',
	'RESULTS': '📈 CAN VIP results',
	'CONTACT_ADMIN': '📞 Contact admin',
	# Offers Menu
	'GET_WALLET': '💰 Get our wallet address',
	'MAIN_MENU': '🔙 Main menu',
	'BACK': '🔙 Back',
	# Wallet Menu
	'WALLET_TRC20': '💰 USDT TRC20',
	'WALLET_BEP20': '💰 USDT BEP20',
	# Results Menu
	'FEBRUARY_2025': '📅 February 2025',
	'JANUARY_2025': '📅 January 2025',
	'NOVEMBER_2024': '📅 November 2024',
	'OCTOBER_2024': '📅 October 2024',
	'SEPTEMBER_2024': '📅 September 2024',
	'JULY_2024': '📅 July 2024',
	'MAY_2024': '📅 May 2024',
	'MARCH_2024': '📅 March 2024',
	'JANUARY_2024': '📅 January 2024',
	'DECEMBER_2023': '📅 December 2023',
	'NOVEMBER_2023': '📅 November 2023',
	'OCTOBER_2023': '📅 October 2023',
	'JULY_2023': '📅 July 2023',
	# Common Buttons
	'YES': '✅ Yes',
	'NO': '❌ Cancel',
	'CANCEL': '❌ Cancel',
}

TR_BUTTONS = {
	# Main Menu
	'OFFERS': '💰 VIP üye',
	'RESULTS': '📈 VIP sistemimiz nasıl çalışıyor?',
	'CONTACT_ADMIN': '📞 Destek Konuş',
	# Offers Menu
	'GET_WALLET': '💰 Katılmak için bu adresimiz',
	'MAIN_MENU': '🔙 Özel menü',
	'BACK': '🔙 Geri dön',
	# Wallet Menu
	'WALLET_TRC20': '💰 USDT TRC20 cüzdan',
	'WALLET_BEP20': '💰 USDT BEP20 cüzdan',
	# Results Menu
	'FEBRUARY_2025': '📅 February 2025',
	'JANUARY_2025': '📅 January 2025',
	'NOVEMBER_2024': '📅 November 2024',
	'OCTOBER_2024': '📅 October 2024',
	'SEPTEMBER_2024': '📅 September 2024',
	'JULY_2024': '📅 July 2024',
	'MAY_2024': '📅 May 2024',
	'MARCH_2024': '📅 March 2024',
	'JANUARY_2024': '📅 January 2024',
	'DECEMBER_2023': '📅 December 2023',
	'NOVEMBER_2023': '📅 November 2023',
	'OCTOBER_2023': '📅 October 2023',
	'JULY_2023': '📅 July 2023',
	# Common Buttons
	'YES': '✅ Evet',
	'NO': '❌ İptal',
	'CANCEL': '❌ İptal',
}

# Admin Buttons (English-only)
ADMIN_BUTTONS = {
	# Main Menu
	'SET_CATEGORY': '📝 Set category list',
	'ADD_TO_CATEGORY': '➕ Add to category list',
	'REMOVE_FROM_CATEGORY': '➖ Remove from category list',
	'BULK_SEND': '📨 Bulk message to category',
	'EXPORT_HISTORY': '📊 Export user history',
	'SHOW_HELP': '❓ Show help',
	# Common Buttons
	'YES': '✅ Yes',
	'NO': '❌ Cancel',
	'CANCEL': '❌ Cancel',
	'MAIN_MENU': '🔙 Main menu',  # Added for admin panel
}

# User Keyboards (Localized)
EN_KEYBOARDS = {
	'CONFIRMATION': InlineKeyboardMarkup(
		[
			[
				InlineKeyboardButton(EN_BUTTONS['YES'], callback_data='CONFIRM'),
				InlineKeyboardButton(EN_BUTTONS['NO'], callback_data='CANCEL'),
			]
		]
	),
	'CANCEL_OPERATION': InlineKeyboardMarkup(
		[[InlineKeyboardButton(EN_BUTTONS['CANCEL'], callback_data='CANCEL')]]
	),
	'CATEGORIES': InlineKeyboardMarkup(
		[
			[InlineKeyboardButton(user_category_label, callback_data=user_category_id)]
			for user_category_id, user_category_label in get_category_id_list()
		]
		+ [[InlineKeyboardButton(EN_BUTTONS['CANCEL'], callback_data='CANCEL')]]
	),
	'RETURN_TO_MAIN_MENU': InlineKeyboardMarkup(
		[
			[
				InlineKeyboardButton(
					EN_BUTTONS['MAIN_MENU'], callback_data='RETURN_TO_MAIN_MENU'
				)
			]
		]
	),
	'USER_PANEL_MAIN': InlineKeyboardMarkup(
		[
			[InlineKeyboardButton(EN_BUTTONS['OFFERS'], callback_data='OFFERS')],
			[InlineKeyboardButton(EN_BUTTONS['RESULTS'], callback_data='RESULTS')],
			[
				InlineKeyboardButton(
					EN_BUTTONS['CONTACT_ADMIN'], url='https://t.me/CANSupport'
				)
			],
		]
	),
	'OFFERS': InlineKeyboardMarkup(
		[
			[
				InlineKeyboardButton(
					EN_BUTTONS['GET_WALLET'], callback_data='SELECT_WALLET_ADDRESS'
				)
			],
			[
				InlineKeyboardButton(
					EN_BUTTONS['CONTACT_ADMIN'], url='https://t.me/CANSupport'
				)
			],
			[
				InlineKeyboardButton(
					EN_BUTTONS['MAIN_MENU'], callback_data='RETURN_TO_MAIN_MENU'
				)
			],
		]
	),
	'SELECT_WALLET_ADDRESS': InlineKeyboardMarkup(
		[
			[
				InlineKeyboardButton(
					EN_BUTTONS['WALLET_TRC20'], callback_data='WALLET_TRC20'
				)
			],
			[
				InlineKeyboardButton(
					EN_BUTTONS['WALLET_BEP20'], callback_data='WALLET_BEP20'
				)
			],
			[
				InlineKeyboardButton(
					EN_BUTTONS['MAIN_MENU'], callback_data='RETURN_TO_MAIN_MENU'
				),
				InlineKeyboardButton(EN_BUTTONS['BACK'], callback_data='OFFERS'),
			],
		]
	),
	'SHOW_WALLET_ADDRESS': InlineKeyboardMarkup(
		[
			[
				InlineKeyboardButton(
					EN_BUTTONS['MAIN_MENU'], callback_data='RETURN_TO_MAIN_MENU'
				),
				InlineKeyboardButton(
					EN_BUTTONS['BACK'], callback_data='SELECT_WALLET_ADDRESS'
				),
			]
		]
	),
	'SHOW_MONTHLY_RESULTS': InlineKeyboardMarkup(
		[
			[
				InlineKeyboardButton(
					EN_BUTTONS['MAIN_MENU'], callback_data='RETURN_TO_MAIN_MENU'
				),
				InlineKeyboardButton(EN_BUTTONS['BACK'], callback_data='RESULTS'),
			]
		]
	),
	'RESULTS': InlineKeyboardMarkup(
		[
			[
				InlineKeyboardButton(
					EN_BUTTONS['FEBRUARY_2025'], callback_data='FEBRUARY_2025'
				),
				InlineKeyboardButton(
					EN_BUTTONS['JANUARY_2025'], callback_data='JANUARY_2025'
				),
			],
			[
				InlineKeyboardButton(
					EN_BUTTONS['NOVEMBER_2024'], callback_data='NOVEMBER_2024'
				),
				InlineKeyboardButton(
					EN_BUTTONS['OCTOBER_2024'], callback_data='OCTOBER_2024'
				),
			],
			[
				InlineKeyboardButton(
					EN_BUTTONS['SEPTEMBER_2024'], callback_data='SEPTEMBER_2024'
				),
				InlineKeyboardButton(
					EN_BUTTONS['JULY_2024'], callback_data='JULY_2024'
				),
			],
			[
				InlineKeyboardButton(EN_BUTTONS['MAY_2024'], callback_data='MAY_2024'),
				InlineKeyboardButton(
					EN_BUTTONS['MARCH_2024'], callback_data='MARCH_2024'
				),
			],
			[
				InlineKeyboardButton(
					EN_BUTTONS['JANUARY_2024'], callback_data='JANUARY_2024'
				),
				InlineKeyboardButton(
					EN_BUTTONS['DECEMBER_2023'], callback_data='DECEMBER_2023'
				),
			],
			[
				InlineKeyboardButton(
					EN_BUTTONS['NOVEMBER_2023'], callback_data='NOVEMBER_2023'
				),
				InlineKeyboardButton(
					EN_BUTTONS['OCTOBER_2023'], callback_data='OCTOBER_2023'
				),
			],
			[InlineKeyboardButton(EN_BUTTONS['JULY_2023'], callback_data='JULY_2023')],
			[
				InlineKeyboardButton(
					EN_BUTTONS['MAIN_MENU'], callback_data='RETURN_TO_MAIN_MENU'
				)
			],
		]
	),
}

TR_KEYBOARDS = {
	'CONFIRMATION': InlineKeyboardMarkup(
		[
			[
				InlineKeyboardButton(TR_BUTTONS['YES'], callback_data='CONFIRM'),
				InlineKeyboardButton(TR_BUTTONS['NO'], callback_data='CANCEL'),
			]
		]
	),
	'CANCEL_OPERATION': InlineKeyboardMarkup(
		[[InlineKeyboardButton(TR_BUTTONS['CANCEL'], callback_data='CANCEL')]]
	),
	'RETURN_TO_MAIN_MENU': InlineKeyboardMarkup(
		[
			[
				InlineKeyboardButton(
					TR_BUTTONS['MAIN_MENU'], callback_data='RETURN_TO_MAIN_MENU'
				)
			]
		]
	),
	'USER_PANEL_MAIN': InlineKeyboardMarkup(
		[
			[InlineKeyboardButton(TR_BUTTONS['OFFERS'], callback_data='OFFERS')],
			# [InlineKeyboardButton(TR_BUTTONS['RESULTS'], callback_data='RESULTS')],
			[
				InlineKeyboardButton(
					TR_BUTTONS['CONTACT_ADMIN'], url='https://t.me/Attiladestek'
				)
			],
		]
	),
	'OFFERS': InlineKeyboardMarkup(
		[
			[
				InlineKeyboardButton(
					TR_BUTTONS['GET_WALLET'], callback_data='SELECT_WALLET_ADDRESS'
				)
			],
			[
				InlineKeyboardButton(
					TR_BUTTONS['CONTACT_ADMIN'], url='https://t.me/Attiladestek'
				)
			],
			[
				InlineKeyboardButton(
					TR_BUTTONS['MAIN_MENU'], callback_data='RETURN_TO_MAIN_MENU'
				)
			],
		]
	),
	'SELECT_WALLET_ADDRESS': InlineKeyboardMarkup(
		[
			[
				InlineKeyboardButton(
					TR_BUTTONS['WALLET_TRC20'], callback_data='WALLET_TRC20'
				)
			],
			[
				InlineKeyboardButton(
					TR_BUTTONS['WALLET_BEP20'], callback_data='WALLET_BEP20'
				)
			],
			[
				InlineKeyboardButton(
					TR_BUTTONS['MAIN_MENU'], callback_data='RETURN_TO_MAIN_MENU'
				),
				InlineKeyboardButton(TR_BUTTONS['BACK'], callback_data='OFFERS'),
			],
		]
	),
	'SHOW_WALLET_ADDRESS': InlineKeyboardMarkup(
		[
			[
				InlineKeyboardButton(
					TR_BUTTONS['MAIN_MENU'], callback_data='RETURN_TO_MAIN_MENU'
				),
				InlineKeyboardButton(
					TR_BUTTONS['BACK'], callback_data='SELECT_WALLET_ADDRESS'
				),
			]
		]
	),
	'SHOW_MONTHLY_RESULTS': InlineKeyboardMarkup(
		[
			[
				InlineKeyboardButton(
					TR_BUTTONS['MAIN_MENU'], callback_data='RETURN_TO_MAIN_MENU'
				),
				InlineKeyboardButton(TR_BUTTONS['BACK'], callback_data='RESULTS'),
			]
		]
	),
	'RESULTS': InlineKeyboardMarkup(
		[
			[
				InlineKeyboardButton(
					TR_BUTTONS['FEBRUARY_2025'], callback_data='FEBRUARY_2025'
				),
				InlineKeyboardButton(
					TR_BUTTONS['JANUARY_2025'], callback_data='JANUARY_2025'
				),
			],
			[
				InlineKeyboardButton(
					TR_BUTTONS['NOVEMBER_2024'], callback_data='NOVEMBER_2024'
				),
				InlineKeyboardButton(
					TR_BUTTONS['OCTOBER_2024'], callback_data='OCTOBER_2024'
				),
			],
			[
				InlineKeyboardButton(
					TR_BUTTONS['SEPTEMBER_2024'], callback_data='SEPTEMBER_2024'
				),
				InlineKeyboardButton(
					TR_BUTTONS['JULY_2024'], callback_data='JULY_2024'
				),
			],
			[
				InlineKeyboardButton(TR_BUTTONS['MAY_2024'], callback_data='MAY_2024'),
				InlineKeyboardButton(
					TR_BUTTONS['MARCH_2024'], callback_data='MARCH_2024'
				),
			],
			[
				InlineKeyboardButton(
					TR_BUTTONS['JANUARY_2024'], callback_data='JANUARY_2024'
				),
				InlineKeyboardButton(
					TR_BUTTONS['DECEMBER_2023'], callback_data='DECEMBER_2023'
				),
			],
			[
				InlineKeyboardButton(
					TR_BUTTONS['NOVEMBER_2023'], callback_data='NOVEMBER_2023'
				),
				InlineKeyboardButton(
					TR_BUTTONS['OCTOBER_2023'], callback_data='OCTOBER_2023'
				),
			],
			[InlineKeyboardButton(TR_BUTTONS['JULY_2023'], callback_data='JULY_2023')],
			[
				InlineKeyboardButton(
					TR_BUTTONS['MAIN_MENU'], callback_data='RETURN_TO_MAIN_MENU'
				)
			],
		]
	),
}

# Admin Keyboards (English-only)
ADMIN_KEYBOARDS = {
	'ADMIN_PANEL_MAIN': InlineKeyboardMarkup(
		[
			[
				InlineKeyboardButton(
					ADMIN_BUTTONS['SET_CATEGORY'], callback_data='START_SET_CATEGORY'
				)
			],
			[
				InlineKeyboardButton(
					ADMIN_BUTTONS['ADD_TO_CATEGORY'],
					callback_data='START_ADD_TO_CATEGORY',
				)
			],
			[
				InlineKeyboardButton(
					ADMIN_BUTTONS['REMOVE_FROM_CATEGORY'],
					callback_data='START_REMOVE_FROM_CATEGORY',
				)
			],
			[
				InlineKeyboardButton(
					ADMIN_BUTTONS['BULK_SEND'], callback_data='START_BULK_SEND'
				)
			],
			[
				InlineKeyboardButton(
					ADMIN_BUTTONS['EXPORT_HISTORY'], callback_data='EXPORT_HISTORY'
				)
			],
			[
				InlineKeyboardButton(
					ADMIN_BUTTONS['SHOW_HELP'], callback_data='SHOW_HELP'
				)
			],
		]
	),
	'CATEGORIES': InlineKeyboardMarkup(
		[
			[InlineKeyboardButton(user_category_label, callback_data=user_category_id)]
			for user_category_id, user_category_label in get_category_id_list()
		]
		+ [[InlineKeyboardButton(EN_BUTTONS['CANCEL'], callback_data='CANCEL')]]
	),
	# Add common admin keyboards
	'ADMIN_CONFIRMATION': InlineKeyboardMarkup(
		[
			[
				InlineKeyboardButton(ADMIN_BUTTONS['YES'], callback_data='CONFIRM'),
				InlineKeyboardButton(ADMIN_BUTTONS['NO'], callback_data='CANCEL'),
			]
		]
	),
	'ADMIN_CANCEL_OPERATION': InlineKeyboardMarkup(
		[[InlineKeyboardButton(ADMIN_BUTTONS['CANCEL'], callback_data='CANCEL')]]
	),
	'ADMIN_RETURN_TO_MAIN_MENU': InlineKeyboardMarkup(
		[
			[
				InlineKeyboardButton(
					ADMIN_BUTTONS['MAIN_MENU'], callback_data='RETURN_TO_MAIN_MENU'
				)
			]
		]
	),
}
