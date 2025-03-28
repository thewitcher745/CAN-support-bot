"""
String constants for all bot messages.
User messages are localized (EN/TR), admin messages are English-only.
"""

# User Messages (Localized)
EN_STRINGS = {
	# User Welcome Messages
	'USER_WELCOME': "🤖 Hello, {name}! I'm a bot that helps you contact CAN support. Choose your desired option from the menu below to continue.",
	'USER_WELCOME_BACK': '🤖 Welcome back! Choose your desired option from the menu below to continue.',
	'USER_HELP': '📝 This bot is used to contact users. Select your desired option after using the /start command.',
	# User Operation Messages
	'OPERATION_CANCELED': '❌ Operation canceled by the user.',
	# Monthly Results Messages
	'MONTHLY_RESULTS_END': '🔚 Choose an option to continue.',
}

TR_STRINGS = {
	# User Welcome Messages
	'USER_WELCOME': '🤖 Merhaba, {name}! Ben, Crypto Attila desteğine ulaşmanıza yardımcı olan bir botum. Size nasıl yardımcı olabilirim?',
	'USER_WELCOME_BACK': '🤖 Tekrar hoş geldiniz! Devam etmek için menüden istediğiniz seçeneği seçin.',
	'USER_HELP': '📝 Neler yapabileceğimi görmek için /help komutunu kullanın.',
	# User Operation Messages
	'OPERATION_CANCELED': '❌ İşlem kullanıcı tarafından iptal edildi.',
	# Monthly Results Messages
	'MONTHLY_RESULTS_END': '🔚 Devam etmek için bir seçenek seçin.',
}

# Admin Messages (English-only)
ADMIN_STRINGS = {
	# Admin Welcome Messages
	'ADMIN_WELCOME': "🔰 Welcome to the admin panel, {name}! Use /help to see what I can do, or use the 'Show help' button below.",
	'ADMIN_WELCOME_BACK': "🔰 Welcome back to the admin panel! Use /help to see what I can do, or use the 'Show help' button below.",
	'ADMIN_HELP': """
📝 This bot is used to contact users. Currently it supports the following commands and functionalities:

/send <user id>: This command forwards a message to a single user given the user's ID. To select what message to forward, reply to the desired message with this command. If no user ID is given, the message is reflected back to the sender. If no message is replied to, a test message is sent instead. 📱

/setcategory: This command assigns a list of user ID's to the selected category. After replying to the user list with this command, select which category you would like to add the users to. This overwrites the existing list. 📈

/addtocategory: This command adds a list of ID's to the selected category. After replying to the user list with this command, select which category you would like to add the users to. 📈

/removefromcategory: This command removes a list of ID's from the selected category. After replying to the user list with this command, select which category you would like to remove the users from. 📈

/bulksend <user id>: This command sends a message to all users in a category, selected in a dialog after the command is used. 📈
""",
	# Bulk Send Messages
	'BULK_SEND_MESSAGE_SELECTED': '📧 Message selected for bulk sending. Now select the category you wish the message to be sent to.\n\nUse /cancel to cancel the operation.',
	'BULK_SEND_ERROR_REPLY': '⚠️ Error: The command /bulksend can only be used in reply to a message. Please make sure you reply to a message with the command and try again.',
	'BULK_SEND_PROMPT': '📨 Send the message you wish to be sent to users in a category.',
	'BULK_SEND_CATEGORY_SELECTED': '❓ Category {category} selected successfully. Are you sure you want to send the provided message to all {count} users in this category?',
	'BULK_SEND_ERROR_USER': '⚠️ Error: Message sending failed for user ID {user_id}: {error}',
	'BULK_SEND_SUCCESS': '✅ Message sent to all users in category {category} successfully!',
	# Category Management Messages
	'CATEGORY_ERROR_REPLY': "⚠️ You have to use this command in reply to a list of user ID's.",
	'CATEGORY_SELECT_PROMPT': '📈 Please select a category to set the user list for:\n\nUse /cancel to cancel the operation.',
	'CATEGORY_USER_LIST_PROMPT': '📋 Send the list of user IDs you want to set for the category.',
	'CATEGORY_CONFIRM_SET': '❓ Are you sure you want to set the user list for category {category}?',
	'CATEGORY_SET_SUCCESS': '✅ Category {category} set successfully!',
	# Add to Category Messages
	'ADD_TO_CATEGORY_SELECT_PROMPT': '📈 Please select a category to add the user list to:\n\nUse /cancel to cancel the operation.',
	'ADD_TO_CATEGORY_USER_LIST_PROMPT': '📋 Send the list of user IDs you want to add to a category.',
	'ADD_TO_CATEGORY_CONFIRM': '❓ Are you sure you want to add the user list to category {category}?',
	'ADD_TO_CATEGORY_SUCCESS': '✅ Selected list added to category {category} successfully!',
	# Remove from Category Messages
	'REMOVE_FROM_CATEGORY_SELECT_PROMPT': '📈 Please select a category to remove the user list from:\n\nUse /cancel to cancel the operation.',
	'REMOVE_FROM_CATEGORY_USER_LIST_PROMPT': '📋 Send the list of user IDs you want to remove from a category.',
	'REMOVE_FROM_CATEGORY_CONFIRM': '❓ Are you sure you want to remove the user list from category {category}?',
	'REMOVE_FROM_CATEGORY_SUCCESS': '✅ Selected list removed from category {category} successfully!',
	# Export History Messages
	'EXPORT_HISTORY_START': '📊 Preparing to export history...',
	'EXPORT_HISTORY_SUCCESS': '✅ History exported successfully!',
	'EXPORT_HISTORY_ERROR': '⚠️ Error exporting history: {error}',
	# Send Message Messages
	'SEND_MESSAGE_PROMPT': '📨 Send the message you want to forward:',
	'SEND_MESSAGE_SUCCESS': '✅ Message sent successfully to user {user_id}',
	'SEND_MESSAGE_ERROR': '⚠️ Error sending message: {error}',
	'ADMIN_OPERATION_CANCELED': '❌ Operation canceled by the user.',
	# User Panel Logs Messages
	'SEND_USER_LOGS_SUCCESS': '✅ User panel logs sent successfully!',
	'SEND_USER_LOGS_ERROR': '⚠️ Error sending user panel logs: {error}',
	'SEND_USER_LOGS_NO_FILE': '⚠️ No user panel logs found for the current locale.',
	# Clear User Logs Messages
	'CLEAR_USER_LOGS_CONFIRM': '❓ Are you sure you want to clear the user panel logs for the current locale ({locale})?',
	'CLEAR_USER_LOGS_SUCCESS': '✅ User panel logs cleared successfully!',
	'CLEAR_USER_LOGS_NO_FILE': '⚠️ No user panel logs found to clear for the current locale.',
}
