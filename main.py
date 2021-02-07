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

def bsm(message, value):
    bot.send_message(message.chat.id, value)

def is_registered(message):
    connection.commit()
    sql = "SELECT * FROM `registered_users` WHERE `chat_id` = " + str(message.chat.id)
    cursor.execute(sql)
    res = cursor.fetchall()
    if (res == ()):
        sql = "INSERT INTO `registered_users` (`chat_id`, `first_name`, `last_name`) VALUES (%s, %s, %s)"
        cursor.execute(sql, (message.chat.id, str(message.from_user.first_name), str(message.from_user.last_name)))
        connection.commit()
        
def current_field_get(message):
    connection.commit()
    sql = "SELECT `current_field` FROM `registered_users` WHERE `chat_id` =  " + str(message.chat.id)
    cursor.execute(sql)
    return cursor.fetchone()[0]

def current_field_upload(message, value):
    connection.commit()
    sql = "UPDATE `registered_users` SET `current_field` = " + str(value) + " WHERE `chat_id` = " + str(message.chat.id)
    cursor.execute(sql)
    connection.commit()
    return 0

@bot.message_handler(commands=['help'])
def help_reaction(message):
    bot.send_message(message.chat.id , config['Bot']['help_reply_text'])

@bot.message_handler(commands=['start'])
def user_registration(message):
    is_registered(message)
    bot.send_message(message.chat.id, config['Bot']['start_reply_text'])
    
@bot.message_handler(commands=['new'])
def new_reaction(message):
    is_registered(message) 
    bsm(message, "Im /new")
    current_field_upload(message, 2)    
        
@bot.message_handler(content_types=['text'])
def text_reaction(message):
    is_registered(message) 
    if(current_field_get(message) == -1):
        bot.send_message(message.chat.id, config['Bot']['text_no_func_reaction'])



bot.polling()