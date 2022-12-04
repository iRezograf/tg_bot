import calculator
import telebot
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime as dt
import re


def current_time():
    return dt.now().strftime('%D:%M:%Y ; %H:%M:%S')


# @bot.message_handler(commands=['start'])
def start_executor(message):
    logging.info(f" {current_time()}: {message.chat.id} {message}")
    prompt = "Привет! Начнем ?"
    bot.send_message(message.chat.id, prompt)
    logging.info(f" {current_time}: {message.chat.id}: bot: {prompt}")


# @bot.message_handler(commands=['help'])
def help_executor(message):
    logging.info(f" {current_time()}: {message.chat.id} {message}")
    prompt = "\n/start\n/calc\n/calc start\n/calc stop"
    bot.send_message(message.chat.id, prompt)
    logging.info(f" {current_time()}: {message.chat.id}: bot: {prompt}")

def regexp_executor(message):
    logging.info(f" {current_time()}: {message.chat.id} {message.text}")
    if re.findall(r"[-+*\/0-9]+", message.text):
        if calc_flag:
            result = message.text + " = " + calculator.main_calculation(message.text)
            bot.send_message(message.chat.id, result)
            logging.info(f" {current_time()}: {message.chat.id}: bot: {result}")
            # calc_flag = False
            return
    else:
        result = 'введите выражение для вычесления: '


# @bot.message_handler(commands=['calc'])
def calc_executor(message):
    logging.info(f" {current_time()}: {message.chat.id} {message.text}")
    global calc_flag
    if '/calc_start' == message.text[:11]:
        calc_flag = True
        # result = message.text[5:] + " = " + calculator.main_calculation(message.text[5:])
        result = 'введите выражение для вычесления: '
        bot.send_message(message.chat.id, result)
        logging.info(f" {current_time()}: {message.chat.id}: bot: {result}")
        return
    if '/calc_stop' == message.text[:10]:
        calc_flag = False
        logging.info(f" {current_time()}: {message.chat.id}: bot: 'calc stop'")
        return


# My_HTTP_API = '5832017456:AAHcjdu9neaYyKSrLEqXxqnU0PYAX8GftVU'
My_NAME = 't.me/iRez_bot'
filename = "tg_bot_log.log"
maxBytes = 2 * 1024 * 256
backupCount = 2
calc_flag = False

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
    logging.info(f" {current_time()}: bot: {'started'}")
except:
    logging.info(f" {current_time()}: bot: {'not started!!!'}")

bot.register_message_handler(start_executor, commands=['start'])
bot.register_message_handler(help_executor, commands=['help'])
bot.register_message_handler(calc_executor, commands=['calc_start', 'calc_stop'])
bot.register_message_handler(regexp_executor, regexp="")

bot.infinity_polling()
