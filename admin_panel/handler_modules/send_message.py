from telegram import Update
from telegram.ext import CallbackContext

from admin_panel.utilities import admin_required, handle_telegram_errors


@handle_telegram_errors
@admin_required
async def send_message(update: Update, context: CallbackContext):
    """Send a message to a target Telegram user.
    
    This handler allows admins to send messages to specific users either by:
    1. Forwarding an existing message by replying to it
    2. Sending a test message with the user's ID
    
    Args:
        update (Update): The incoming update from Telegram
        context (CallbackContext): The callback context
        
    The command format is: /send_message <user_id>
    If no user_id is provided, the message will be sent back to the sender.
    """
    # Extract target user ID from command or fallback to sender's ID
    try:
        target_user_id = update.message.text.split(' ')[1]
    except IndexError:
        await update.message.reply_text('⚠️ No target user specified, reflecting message back to sender...')
        target_user_id = update.message.from_user.id

    if update.message.reply_to_message:
        # Forward the replied-to message to target user
        await update.message.reply_text(f'📧 Forwarding message to user {target_user_id}...')
        await context.bot.copy_message(
            chat_id=target_user_id,
            from_chat_id=update.effective_chat.id,
            message_id=update.message.reply_to_message.message_id
        )
    else:
        # Send a test message when no message is being replied to
        await update.message.reply_text(f'📨 Sending message to user {target_user_id}...')
        await context.bot.send_message(
            chat_id=target_user_id,
            text=f'This is a test message sent to user {target_user_id}'
        )
