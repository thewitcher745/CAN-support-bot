from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from admin_panel.utilities import get_category_id_list

CONFIRMATION = InlineKeyboardMarkup(
    [[InlineKeyboardButton('✅ Yes', callback_data='CONFIRM'), InlineKeyboardButton(
        '❌ Cancel', callback_data='CANCEL')]]
)

CANCEL_OPERATION = InlineKeyboardMarkup(
    [[InlineKeyboardButton('❌ Cancel', callback_data='CANCEL')]])

CATEGORIES = InlineKeyboardMarkup(
    [[InlineKeyboardButton(user_category_label, callback_data=user_category_id)] for user_category_id, user_category_label in
     get_category_id_list()] + [[InlineKeyboardButton('❌ Cancel', callback_data='CANCEL')]]
)

RETURN_TO_MAIN_MENU = InlineKeyboardMarkup([[InlineKeyboardButton(
    '🔙 Return to main menu', callback_data='RETURN_TO_MAIN_MENU')]])

ADMIN_PANEL_MAIN = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton('📝 Set category list',
                              callback_data='START_SET_CATEGORY')],
        [InlineKeyboardButton('➕ Add to category list',
                              callback_data='START_ADD_TO_CATEGORY')],
        [InlineKeyboardButton('➖ Remove from category list',
                              callback_data='START_REMOVE_FROM_CATEGORY')],
        [InlineKeyboardButton('📨 Bulk message to category',
                              callback_data='START_BULK_SEND')],
        [InlineKeyboardButton('📊 Export user history',
                              callback_data='EXPORT_HISTORY')],
        [InlineKeyboardButton('❓ Show help', callback_data='SHOW_HELP')]
    ]
)
