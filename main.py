import os
import sys
import numpy as np
from numpy import *
import telebot
import configparser
import pymysql
import pickle

# from pymysql.cursors import DictCursor

# SQL подключение
connection = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    charset = 'utf8mb4',
    db='pizzatgdatabase',
    # cursorclass=DictCursor
)

cursor = connection.cursor()

#SQL проверка подключения
if connection.open != 1:
    print("SQL connection ERROR")
    sys.exit()
else :
    print("SQL connected sucsessfully")
    
#TeleBot подключение

config = configparser.ConfigParser()
config.read("settings.ini")
bot = telebot.TeleBot(config['Telegram']['token'])

@bot.message_handler(commands=['start'])
def user_registration(message):
    chat_id = message.chat.id
    connection.commit()
    sql = "SELECT * FROM `registered_users` WHERE `chat_id` = " + str(chat_id)
    cursor.execute(sql)
    res = cursor.fetchall()
    print(res)
    if (res == ()):
        sql = "INSERT INTO `registered_users` (`chat_id`, `first_name`, `last_name`) VALUES (%s, %s, %s)"
        cursor.execute(sql, (message.chat.id, message.from_user.first_name, message.from_user.last_name))
        connection.commit()
        print('Done!')
    
bot.polling()