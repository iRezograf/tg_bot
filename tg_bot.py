import calculator
import telebot

My_HTTP_API = '5832017456:AAHcjdu9neaYyKSrLEqXxqnU0PYAX8GftVU'
My_NAME = 't.me/iToora_bot'

bot = telebot.TeleBot(My_HTTP_API)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Начнем ?")


@bot.message_handler(commands=['calc'])
def start_message(message):
    result = calculator.main_calculation(message.text[5:])
    bot.send_message(message.chat.id, message.text[5:] + " = " + result)


bot.infinity_polling()
