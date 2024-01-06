from asyncio import current_task
import requests
import logging
from typing import Text

from dotenv import dotenv_values
from telegram import Update
from telegram.ext import ContextTypes, Application, CommandHandler, CallbackContext


logging.basicConfig(
    format="%(levelname)s- %(name)s - %(asctime)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)
config = dotenv_values(".env")

async def start(update: Update, _:ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text('Hello! Use /set_destination YOUR_URL DELAY_SECONDS to track website status.') 

async def abolish_path():
    pass

async def wander_to(context: CallbackContext):
    """ Visit specified link and send a message if resource is not avaiable. """
    job = context.job
    destination = job.data 

    try:
        response = requests.get(destination)

        await context.bot.send_message(job.chat_id, f'The {destination} is accessible. Status code: {response.status_code}') 
    except requests.Timeout as tmout:
        await context.bot.send_message(job.chat_id, f'The resource {destination} take too long to respond!')

    except ConnectionError as conerr:
        # DNS failure, refused etc...
        await context.bot.send_message(job.chat_id, f'The resource {destination} is not available!')

    except Exception as unexp_except:
        # Something is way off...
        logging.exception(f'Got unexpected exception: {unexp_except}')
        await context.bot.send_message(job.chat_id, f'Unable to visit places... Got unexpected exception.')
        

async def set_destination(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Command to add a new destination to be visited periodically """

    chat_id = update.effective_message.chat_id
    
    try:
        destination = context.args[0]
        timer = float(context.args[1])
        
        if timer < 0:
            await update.effective_message.reply_text('Incorrect time') 
            return
        
        context.job_queue.run_repeating(wander_to, interval=timer, chat_id=chat_id, name=str(chat_id), data=destination)

        await update.effective_message.reply_text('Location was added!')
    except (IndexError, ValueError):
        await update.effective_message.reply_text('Usage: /set_destination destination(URL) frequency(time in seconds)')
        
    
async def remove_destination(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Command to remove existing destination by given name."""
    current_jobs = context.job_queue.get_jobs_by_name(str(update.effective_message.chat_id)) 
    logger.info(current_jobs) 
    for job in current_jobs:
        job.schedule_removal()

    await update.effective_message.reply_text(f'Removed {len(current_jobs)} destinations')


async def edit_destination(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Function allows to change actively running jobs. E.g. change frequency """
    current_jobs = context.job_queue.get_jobs_by_name(str(update.effective_message.chat_id))
    new_destination = context.args[0]
    
    logger.info(f'New dest for jobs: {new_destination}')
    for job in current_jobs:
        job.data = new_destination
    logger.info(f'Updated: {len(current_jobs)}') 
    await update.effective_message.reply_text(f'Updated: {len(current_jobs)}')

async def list_destinations(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Function that prints user created destinations. """
    current_jobs = context.job_queue.jobs()
    
    reply_message = f'Existing jobs: {len(current_jobs)}\n'

    for ind, job in enumerate(current_jobs):

        # Since job.date is set to destination we can print it right away! 
        reply_message += f'{ind + 1}. Name: {job.name}. {job.data}\n' 

    await update.effective_message.reply_text(reply_message)


def main():
    """Attach handlers and run the bot."""
    application = Application.builder().token(config.get('BOT_TOKEN', 'EMPTY')).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('list_destinations', list_destinations))
    application.add_handler(CommandHandler('set_destination', set_destination))
    application.add_handler(CommandHandler('rm_destinations', remove_destination))
    application.add_handler(CommandHandler('edit_destination', edit_destination))
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()

