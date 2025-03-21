from telegram import Update
from telegram.ext import CallbackContext

user_data = {}
async def configure(update: Update, callback: CallbackContext):

    def start(update: Update, context: CallbackContext) -> None:
        update.message.reply_text("Hello! Please enter your name:")
        return

    # Function to handle user input
    def get_user_input(update: Update, context: CallbackContext) -> None:
        user_id = update.message.from_user.id
        user_name = update.message.text  # Capture user input
        
        # Store user input in dictionary
        user_data[user_id] = user_name

        update.message.reply_text(f"Thanks, {user_name}! Your name has been saved.")

    start(update, callback)
    get_user_input(update, callback)