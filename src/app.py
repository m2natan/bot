from credentials import _TOKEN
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from functions.weekend_assignments import generate_weekend_assignments
from functions.cart_witness import generate_public_cart_witness
from functions.assignments import generate_assignments
# Import database functions
from database import init_db, save_user, update_user, user_exists, get_user_by_telegram_id

# Initialize database
init_db()

def get_button_keyboard():
    """Create raised buttons keyboard"""
    keyboard = [
        [KeyboardButton("📢🛒"), KeyboardButton("🌞📅"), KeyboardButton("✅✔️")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send initial message explaining the format and show buttons"""
    # Check if user already exists
    user_telegram_id = update.effective_user.id
    user = get_user_by_telegram_id(user_telegram_id)
    
    if user:
        await update.message.reply_text(
            f"😁 {user['fullname']}! You can update your information anytime."
        )
    else:
        await update.message.reply_text(
            "Welcome! Please provide your information in the following format:\n\n"
            "Full Name\n"
            "Nickname\n"
            "Group\n\n"
            "Example:\n"
            "John Doe\n"
            "johndoe\n"
            "Group A"
        )

async def process_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process the user's input and show confirmation buttons"""
    message_text = update.message.text
    
    # Handle button presses
    if message_text == "📢🛒":
        await generate_public_cart_witness(update, context)  # Function to return file
        return
    elif message_text == "🌞📅":
        await generate_weekend_assignments(update, context)  # Function to return file
        return
    elif message_text == "✅✔️":
        await generate_assignments(update, context)  # Function to return file
        return
    
    # Regular information processing (No split of full name anymore)
    parts = message_text.strip().split('\n')
    
    if len(parts) != 3:
        await update.message.reply_text(
            "⚠️ Invalid format! Please provide exactly 3 lines:\n"
            "Full Name\n"
            "Nickname\n"
            "Group"
        )
        return
    
    temp_data = {
        'fullname': parts[0].strip(),  # Keep the full name as a single field
        'nickname': parts[1].strip(),
        'group': parts[2].strip()
    }
    
    context.user_data['temp_data'] = temp_data
    
    # Create inline keyboard for confirmation
    keyboard = [
        [
            InlineKeyboardButton("✅ Save", callback_data='save'),
            InlineKeyboardButton("🔄 Update", callback_data='update')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "📋 Please confirm your information:\n\n"
        f"📝 Full Name: {temp_data['fullname']}\n"
        f"👤 Nickname: {temp_data['nickname']}\n"
        f"👥 Group: {temp_data['group']}\n\n"
        "Would you like to save this information or update it?",
        reply_markup=reply_markup
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    user_telegram_id = query.from_user.id
    temp_data = context.user_data.get('temp_data', {})
    
    if query.data == 'save':
        # Check if user already exists
        if user_exists(user_telegram_id):
            await query.message.edit_text("❌ User already exists. Please update your information.")
            return
        
        # Save user data
        save_user(user_telegram_id, temp_data['fullname'], temp_data['nickname'], temp_data['group'])
        
        await query.message.edit_text(
            "✅ Information saved successfully!\n\n"
            f"📝 Full Name: {temp_data['fullname']}\n"
            f"👤 Nickname: {temp_data['nickname']}\n"
            f"👥 Group: {temp_data['group']}\n\n"
            "You can update your information anytime by sending a new message in the same format."
        )
    
    elif query.data == 'update':
        await query.message.edit_text(
            "🔄 Please send your information again in the following format:\n\n"
            "Full Name\n"
            "Nickname\n"
            "Group"
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send help message"""
    await update.message.reply_text(
        "How to use this bot:\n\n"
        "Quick Actions:\n"
        "🔵 Button 1 - Quick action 1\n"
        "🟢 Button 2 - Quick action 2\n"
        "🔴 Button 3 - Quick action 3\n\n"
        "Information Input:\n"
        "1. Send your information in exactly 3 lines\n"
        "2. Each piece of information should be on a new line\n"
        "3. Format:\n"
        "Full Name\n"
        "Nickname\n"
        "Group\n\n"
        "Commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/status - Show your saved information"
    )

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show current saved information"""
    saved_info = context.user_data.get('saved_info', None)
    
    if saved_info:
        await update.message.reply_text(
            "📋 Your current saved information:\n\n"
            f"📝 Full Name: {saved_info['fullname']}\n"
            f"👤 Nickname: {saved_info['nickname']}\n"
            f"👥 Group: {saved_info['group']}"
        )
    else:
        await update.message.reply_text(
            "❌ No information saved yet!\n"
            "Please send your information in the required format."
        )

def main():
    # Create the application with your bot token
    application = Application.builder().token(_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_info))
    application.add_handler(CallbackQueryHandler(button_callback))

    # Start the bot
    print("Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
