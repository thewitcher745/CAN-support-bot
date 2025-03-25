"""
Keyboard management module for the bot.
Contains localized keyboards for user messages and English-only keyboards for admin messages.
All keyboards are exposed as module-level variables.
"""

from utils.config import Config
from utils.keyboard_constants import EN_KEYBOARDS, TR_KEYBOARDS, ADMIN_KEYBOARDS

# Get current locale
locale = Config.get_locale().value

# Import localized keyboards based on current locale
keyboards = EN_KEYBOARDS if locale == 'EN' else TR_KEYBOARDS

# Expose all localized keyboards as module-level variables
for name, value in keyboards.items():
	globals()[name] = value

# Expose all admin keyboards as module-level variables
for name, value in ADMIN_KEYBOARDS.items():
	globals()[name] = value
