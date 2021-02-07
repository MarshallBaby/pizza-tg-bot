import os
import sys
import numpy as np
from numpy import *
import telebot
import configparser
import pymysql

from pymysql.cursors import DictCursor

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='pizzatgdatabase',
    charset='utf8mb4',
    cursorclass=DictCursor
)


with connection.cursor() as cursor:
    sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
    cursor.execute(sql, ('pizzalapapizza', 'makarena'))


connection.commit()

# with connection:
#     with connection.cursor() as cursor:
#         # Create a new record
#         sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
#         cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

#     # connection is not autocommit by default. So you must commit to save
#     # your changes.
#     connection.commit()

#     with connection.cursor() as cursor:
#         # Read a single record
#         sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
#         cursor.execute(sql, ('webmaster@python.org',))
#         result = cursor.fetchone()
#         print(result)


# from pprint import pprint
# import httplib2 
# import apiclient.discovery
# from oauth2client.service_account import ServiceAccountCredentials	

# CREDENTIALS_FILE = 'pizza-tg-bot-be9f47d83502.json'
# # ID Google Sheets документа (можно взять из его URL)
# spreadsheet_id = '1ne95wg3LVvU2N-OuL1QHpyzJSxGERkabAVfOXlgQ_EQ'

# # Авторизуемся и получаем service — экземпляр доступа к API
# credentials = ServiceAccountCredentials.from_json_keyfile_name(
#     CREDENTIALS_FILE,
#     ['https://www.googleapis.com/auth/spreadsheets',
#      'https://www.googleapis.com/auth/drive'])
# httpAuth = credentials.authorize(httplib2.Http())
# service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

# values = service.spreadsheets().values().get(
#     spreadsheetId=spreadsheet_id,
#     range='A1:E10',
#     majorDimension='COLUMNS'
# ).execute()
# pprint(values)



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

