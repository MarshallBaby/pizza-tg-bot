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

global collector_mode
collector_mode = 0
global current_field
current_field = 0
global data__array
data_array = []

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
    global collector_mode
    collector_mode = 1
    data_collector(message)

def data_collector(message):
    global data_array
    global current_field
    global collector_mode
    if (current_field == data_fields_amount):
        current_field = 0
        collector_mode = 0
        final_message = ""
        for i in data_array:
            bot.send_message(message.chat.id, i)
        data_array = []
    else:
        bot.send_message(message.chat.id, data_answ_array[current_field])

@bot.message_handler(content_types=['text'])
def data_loop(message):
    if (collector_mode == 1):
        global current_field
        data_array.append(message.text)
        current_field += 1
        data_collector(message)


bot.polling()

