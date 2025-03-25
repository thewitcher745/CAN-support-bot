"""
String management module for the bot.
Contains localized strings for user messages and English-only strings for admin messages.
All strings are exposed as module-level variables.
"""

from utils.config import Config
from utils.string_constants import EN_STRINGS, TR_STRINGS, ADMIN_STRINGS

# Get current locale
locale = Config.get_locale().value

# Import localized strings based on current locale
strings = EN_STRINGS if locale == 'EN' else TR_STRINGS

# Expose all localized strings as module-level variables
for name, value in strings.items():
	globals()[name] = value

# Expose all admin strings as module-level variables
for name, value in ADMIN_STRINGS.items():
	globals()[name] = value
