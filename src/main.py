import logging

from dotenv import dotenv_values
from telegram import Update
from telegram.ext import ContextTypes, Application, CommandHandler, CallbackContext


logging.basicConfig(
    format="%(levelname)s- %(name)s - %(asctime)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)
config = dotenv_values(".env")

async def start(update: Update, _:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Use /wander_to YOUR_URL to track website status.') 

async def list_destinations(update: Update, _:ContextTypes.DEFAULT_TYPE):
    pass

def main():
    """Attach handlers and run the bot."""
    application = Application.builder().token(config.get('BOT_TOKEN', 'EMPTY')).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('list_destinations', list_destinations))
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()

