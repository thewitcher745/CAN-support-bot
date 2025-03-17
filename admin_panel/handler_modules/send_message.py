from telegram import error, Update
from telegram.ext import CallbackContext

from admin_panel.utilities import admin_required


@admin_required
async def send_message(update: Update, context: CallbackContext):
    """Send a message to the target user ID."""

    try:
        # Get the target user ID from the sender
        try:
            target_user_id = update.message.text.split(' ')[1]

        except IndexError:
            await update.message.reply_text('⚠️ No target user specified, reflecting message back to sender...')
            target_user_id = update.message.from_user.id

        # If the command is used in reply to a previous message, that message will be forwarded to the recipient without the sender data.
        if update.message.reply_to_message:
            # Confirmation message
            await update.message.reply_text(f'📧 Forwarding message to user {target_user_id}...')

            await context.bot.copy_message(chat_id=target_user_id, from_chat_id=update.effective_chat.id,
                                           message_id=update.message.reply_to_message.message_id)

        # If the command isn't used in a reply, just send the dev message...
        else:
            # Confirmation message
            await update.message.reply_text(f'📨 Sending message to user {target_user_id}...')

            # Send the message to the target user
            await context.bot.send_message(target_user_id, f'This is a test message sent to user {target_user_id}')

    except error.BadRequest as e:
        await update.message.reply_text(f'⚠️ Error: User ID might be invalid or bot has no permission: {str(e)}')

    except Exception as e:
        await update.message.reply_text(f'🚨 An error occurred: {str(e)}')

    return
