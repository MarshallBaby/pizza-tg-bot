import os
import telebot

bot = telebot.TeleBot('1504321352:AAHn4j-hFEDij8FSSbTrOiDOTBE_xekN0gc')

#--------START CONFIGURATION----------

# /start текст
start_reply_text = "Привет, человек! Это пример START ответа."

# /help текст
help_reply_text = "Это пример HELP ответа."


#--------END CONFIGURATION----------



@bot.message_handler(commands=['help'])
def help_reply(message):
    bot.reply_to(message, help_reply_text)

@bot.message_handler(commands=['start'])
def help_reply(message):
    bot.reply_to(message, start_reply_text)    

bot.polling()

