from typing import Text, List
import requests
import logging

from dotenv import dotenv_values
from telegram import Update
from telegram.ext import ContextTypes, Application, CommandHandler, CallbackContext, Job

from ptbcontrib.ptb_jobstores.mongodb import PTBMongoDBJobStore

from replies import SET_TIMER_EXPLAIN, REMOVE_TIMER_EXPLAIN

logging.basicConfig(
    format="%(levelname)s- %(name)s - %(asctime)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)
config = dotenv_values(".env")

logger.info(f'Is key missing? {config.get("BOT_TOKEN") is None}')


async def start(update: Update, _: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(SET_TIMER_EXPLAIN)


async def wander_to(context: CallbackContext):
    """Visit specified link and send a message if resource is not avaiable."""
    job = context.job
    destination = job.data

    try:
        response = requests.get(destination)

        await context.bot.send_message(
            job.chat_id,
            f"The {destination} is accessible. Status code: {response.status_code}",
        )
    except requests.Timeout as tmout:
        await context.bot.send_message(
            job.chat_id, f"The resource {destination} take too long to respond!"
        )

    except ConnectionError as conerr:
        # DNS failure, refused etc...
        await context.bot.send_message(
            job.chat_id, f"The resource {destination} is not available!"
        )

    except Exception as unexp_except:
        # Something is way off...
        logging.exception(f"Got unexpected exception: {unexp_except}")
        await context.bot.send_message(
            job.chat_id, f"Unable to visit places... Got unexpected exception."
        )


async def set_destination(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Command to add a new destination to be visited periodically"""

    chat_id = update.effective_message.chat_id

    try:
        timer_name: Text = context.args[0]
        destination: Text = context.args[1]
        timer = float(context.args[2])

        if not timer_name:
            await update.effective_message.reply_text(SET_TIMER_EXPLAIN) 
            return

        if timer < 0:
            await update.effective_message.reply_text("Incorrect time")
            return

        context.job_queue.run_repeating(
            wander_to,
            interval=timer,
            chat_id=chat_id,
            name=timer_name,
            data=destination,
        )

        await update.effective_message.reply_text("Location was added!")
    except (IndexError, ValueError):
        await update.effective_message.reply_text(SET_TIMER_EXPLAIN)


async def remove_destination(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Command to remove existing destination by given name."""
    timer_name = context.args[0]
    
    if not timer_name:
        await update.effective_message.reply_text(REMOVE_TIMER_EXPLAIN) 
        return
    
    current_jobs = context.job_queue.get_jobs_by_name(timer_name)

    logger.info(current_jobs)
    
    if not current_jobs:
        await update.effective_message.reply_text(f'{timer_name.capitalize()} not found!')
        return

    for job in current_jobs:
        job.schedule_removal()

    await update.effective_message.reply_text(f'{timer_name} removed!')


async def edit_destination(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Function allows to change actively running jobs. E.g. change frequency"""

    timer_name = context.args[0]
    
    if not timer_name:
        await update.effective_message.reply_text()

    current_jobs = context.job_queue.get_jobs_by_name(
    )
    new_destination = context.args[0]

    logger.info(f"New dest for jobs: {new_destination}")
    for job in current_jobs:
        job.data = new_destination

    logger.info(f"Updated: {len(current_jobs)}")
    await update.effective_message.reply_text(f"Updated: {len(current_jobs)}")


async def list_destinations(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Function that prints user created destinations."""
    current_jobs = context.job_queue.jobs()

    reply_message = f"Existing jobs: {len(current_jobs)}\n"

    for ind, job in enumerate(current_jobs):
        # Since job.date is set to destination we can print it right away!
        reply_message += f"{ind + 1}. Name: {job.name}. {job.data}\n"

    await update.effective_message.reply_text(reply_message)


def main():
    """Attach handlers and run the bot."""
    application = Application.builder().token(config.get("BOT_TOKEN")).build()

    application.job_queue.scheduler.add_jobstore(
        PTBMongoDBJobStore(
            application=application,
            host=config.get('MONGO_CONNECT'),
        )
    )
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("list_destinations", list_destinations))
    application.add_handler(CommandHandler("set_destination", set_destination))
    application.add_handler(CommandHandler("rm_destination", remove_destination))
    application.add_handler(CommandHandler("edit_destination", edit_destination))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
