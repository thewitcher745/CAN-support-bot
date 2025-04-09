"""
Keyboard management module for the bot.
Contains localized keyboards for user messages and English-only keyboards for admin messages.
All keyboards are exposed as module-level variables.
"""

from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from utils.config import Config
from utils.utilities import get_signals_for_type
from utils.keyboard_constants import (
	EN_KEYBOARDS,
	TR_KEYBOARDS,
	ADMIN_KEYBOARDS,
	EN_BUTTONS,
	TR_BUTTONS,
)

# Get current locale
locale = Config.get_locale().value

# Import localized keyboards based on current locale
keyboards = EN_KEYBOARDS if locale == 'EN' else TR_KEYBOARDS
button_labels = EN_BUTTONS if locale == 'EN' else TR_BUTTONS

# Expose all localized keyboards as module-level variables
for name, value in keyboards.items():
	globals()[name] = value

# Expose all admin keyboards as module-level variables
for name, value in ADMIN_KEYBOARDS.items():
	globals()[name] = value


def create_sample_signals_pair_select_keyboard(
	signal_type: str,
) -> InlineKeyboardMarkup:
	# Dynamically generate the keyboard based on the signal type
	signal_list = get_signals_for_type(signal_type)
	keyboard = InlineKeyboardMarkup(
		[
			[
				InlineKeyboardButton(
					text=f'{signal["title"]} - {signal["pair_name"]}',
					callback_data=f'{signal_type}:{signal["message_id"]}',
				)
			]
			for signal in signal_list
		]
		+ [
			[
				InlineKeyboardButton(
					text=button_labels['MAIN_MENU'],
					callback_data='RETURN_TO_MAIN_MENU',
				),
				InlineKeyboardButton(
					text=button_labels['BACK'],
					callback_data='SAMPLE_SIGNALS_SELECT_TYPE',
				),
			]
		]
	)

	return keyboard
