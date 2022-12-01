import calculator
import telebot
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime as dt

# My_HTTP_API = '5832017456:AAHcjdu9neaYyKSrLEqXxqnU0PYAX8GftVU'
My_NAME = 't.me/iRez_bot'
filename = "tg_bot_log.log"
maxBytes = 2 * 1024 * 256
backupCount = 2

with open('My_HTTP_API.token', 'r') as token_file:
    My_HTTP_API = token_file.read()

logging.handlers.RotatingFileHandler(filename, maxBytes, backupCount)
logging.basicConfig(level=logging.INFO, filename=filename, filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s")
logging.debug("A DEBUG Message")
logging.info("An INFO")
logging.warning("A WARNING")
logging.error("An ERROR")
logging.critical("A message of CRITICAL severity")

try:
    bot = telebot.TeleBot(My_HTTP_API)
    time = dt.now().strftime('%d.%m.%Y ; %H:%M:%S')
    logging.info(f" {time}: bot: {'started'}")
except:
    time = dt.now().strftime('%d.%m.%Y ; %H:%M:%S')
    logging.info(f" {time}: bot: {'not started!!!'}")


@bot.message_handler(commands=['start'])
def start_message(message):
    current_time = dt.now().strftime('%d.%m.%Y ; %H:%M:%S')
    logging.info(f" {current_time}: {message.chat.id} {message}")
    prompt = "Привет! Начнем ?"
    bot.send_message(message.chat.id, prompt)
    logging.info(f" {current_time}: {message.chat.id}: bot: {prompt}")


@bot.message_handler(commands=['help'])
def start_message(message):
    current_time = dt.now().strftime('%d.%m.%Y ; %H:%M:%S')
    logging.info(f" {current_time}: {message.chat.id} {message}")
    prompt = "\n/start\n/calc\n/calc 1+2+3 "
    bot.send_message(message.chat.id, prompt)
    logging.info(f" {current_time}: {message.chat.id}: bot: {prompt}")


@bot.message_handler(commands=['calc'])
def start_message(message):
    current_time = dt.now().strftime('%d.%m.%Y ; %H:%M:%S')
    logging.info(f" {current_time}: {message.chat.id} {message}")
    result = message.text[5:] + " = " + calculator.main_calculation(message.text[5:])
    bot.send_message(message.chat.id, result)
    logging.info(f" {current_time}: {message.chat.id}: bot: {result}")


bot.infinity_polling()
