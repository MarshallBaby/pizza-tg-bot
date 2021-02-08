import os
import sys
import numpy as np
from numpy import *
import telebot
import configparser
import pymysql
import pickle
import json


config = configparser.ConfigParser()
config.read("settings.ini")
bot = telebot.TeleBot(config['Telegram']['token'])

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

global fields_amount
fields_amount = int(config['Table']['fields_amount'])

def bsm(message, value):
    bot.send_message(message.chat.id, value)

def is_registered(message):
    global fields_amount
    connection.commit()
    sql = "SELECT * FROM `registered_users` WHERE `chat_id` = " + str(message.chat.id)
    cursor.execute(sql)
    res = cursor.fetchall()
    if (res == ()):
        data_array = []
        for i in range(fields_amount):
            data_array.append("?")
        data_array = "#".join(data_array)
        sql = "INSERT INTO `registered_users` (`chat_id`, `first_name`, `last_name`, `data_array`) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (message.chat.id, str(message.from_user.first_name), str(message.from_user.last_name), data_array))
        connection.commit()
        del data_array
        del sql
        
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

def current_field_increment(message):
    connection.commit()
    sql = "SELECT `current_field` FROM `registered_users` WHERE `chat_id` =  " + str(message.chat.id)
    cursor.execute(sql)
    current_field = cursor.fetchone()[0]
    sql = "UPDATE `registered_users` SET `current_field` = " + str(current_field + 1) + " WHERE `chat_id` = " + str(message.chat.id)
    cursor.execute(sql)
    connection.commit()
    
def data_array_get(message):
    connection.commit()
    sql = "SELECT `data_array` FROM `registered_users` WHERE `chat_id` =  " + str(message.chat.id)
    cursor.execute(sql)
    data_array = cursor.fetchone()[0]
    return data_array.split("#")

def data_array_upload(message, data_array):
    connection.commit()
    # data_array = "#".join(data_array)
    sql = "UPDATE `registered_users` SET `data_array` = '" + str("#".join(data_array)) + "' WHERE `chat_id` = " + str(message.chat.id)
    print(sql)
    cursor.execute(sql)
    connection.commit()
    

            

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
    if(current_field_get(message) == -1):
        current_field_increment(message)
        bsm(message, "Создание нового массива")
        bsm(message, "Введите значение" + str(current_field_get(message)))
    else:
        print("Я еблан")
        connection.commit()
        sql = "DELETE FROM `registered_users` WHERE `chat_id` = " + str(message.chat.id)
        cursor.execute(sql)
        connection.commit()
        is_registered(message)
        bsm(message, "reset")
        
@bot.message_handler(content_types=['text'])
def text_reaction(message):
    global fields_amount
    is_registered(message) 
    if(current_field_get(message) == -1):
        bot.send_message(message.chat.id, config['Bot']['text_no_func_reaction'])
    else:
        print(current_field_get(message))
        if(current_field_get(message) >= fields_amount):
            array_send(message)
            connection.commit()
            sql = "DELETE FROM `registered_users` WHERE `chat_id` = " + str(message.chat.id)
            cursor.execute(sql)
            connection.commit()
            is_registered(message)
        else:
            data_array = data_array_get(message)
            data_array[current_field_get(message)] = message.text
            data_array_upload(message, data_array)
            current_field_increment(message)
            bsm(message, "Введите значение " + str(current_field_get(message)))
        
        
def array_send(message):
    bsm(message, "Отправляем массив")
    print("Отправляем массив")        


bot.polling()