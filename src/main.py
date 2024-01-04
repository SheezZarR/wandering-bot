from dotenv import dotenv_values
import telebot
import os

config = dotenv_values(".env")

bot = telebot.TeleBot(config.get('BOT_TOKEN', "empty"))


@bot.message_handler(commands=['start', 'Hello'])
def send_message(message):
    bot.reply_to(message, "Hiii!!")
    


bot.infinity_polling()

