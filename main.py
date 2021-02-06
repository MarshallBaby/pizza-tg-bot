import os
import sys
import numpy as np
from numpy import *
import telebot
import configparser

config = configparser.ConfigParser()
config.read("settings.ini")
bot = telebot.TeleBot(config['Telegram']['token'])




start_reply_text = config['Bot']['start_reply_text']
help_reply_text = config['Bot']['help_reply_text']
data_fields_amount = 5
data_answ_array = np.array([
    'Введите первое значение',
    'Введите второе значение',
    'Введите третье значение',
    'Введите четвертое значение',
    'Введите пятое значение',
    
])

if data_fields_amount != len(data_answ_array):
    print("Кол-во полей записи не соотв. кол-ву обращений")
    print('ERROR: data_fields_amount != len(data_answ_array)')
    sys.exit()


@bot.message_handler(commands=['help'])
def help_reply(message):
    bot.reply_to(message, help_reply_text)

@bot.message_handler(commands=['start'])
def help_reply(message):
    bot.reply_to(message, start_reply_text)    

@bot.message_handler(commands=['new'])
def new_request(message):
    data_collector(message)

def data_collector(message):
    for i in data_answ_array:
        bot.send_message(message.chat.id, i)


bot.polling()

