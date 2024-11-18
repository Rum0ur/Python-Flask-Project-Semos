## za telegram bot info
## https://t.me/pythonFlaskProjectBot
## 7848660184:AAGOk10bH2iDGAExmRi0e1q9vM9NRHHOFE4
## https://core.telegram.org/bots/api

import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Enable logging to help debug issues with the bot
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask endpoint URL
FLASK_API_URL = "http://127.0.0.1:5000/user"  # Change to your Flask server's URL

# Command handler for the "/user" command
async def user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Extract the user ID from the command
    try:
        user_id = context.args[0]  # Expecting /user <user_id>
        response = requests.post(FLASK_API_URL, json={"user_id": user_id})

        if response.status_code == 200:
            user_data = response.json()
            await update.message.reply_text(f"User Data:\nName: {user_data['name']}\nE-mail: {user_data['email']}\nAge: {user_data['age']}\nTotal spent: ${user_data['total_spent']}")
        else:
            await update.message.reply_text(f"Error: {response.status_code}")
    except IndexError:
        await update.message.reply_text("Please provide a user ID. Example: /user 90")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

# Function to start the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Use /user <user_id> to get user data.")

def main():
    # Set up the Telegram bot with your token
    application = Application.builder().token("7848660184:AAGOk10bH2iDGAExmRi0e1q9vM9NRHHOFE4").build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("user", user))

    # Start the bot and begin polling
    application.run_polling()

if __name__ == '__main__':
    main()