import calculator
import telebot
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime as dt
import json



def current_time():
    return dt.now().strftime('%D:%M:%Y ; %H:%M:%S')


def flags_status(message):
    global phone_flag
    global mainwin_flag
    global calc_flag
    global action_status
    global contacts
    global contact_name
    if type(message) == type('str'):
        logging.info(f" {current_time()}:"
                     f", message:'{message}'"
                     f", phone_flag: {phone_flag}"
                     f", mainwin_flag: {mainwin_flag}"
                     f", calc_flag: {calc_flag}"
                     f", action_status: {action_status}")
    else:
        logging.info(f" {current_time()}:"
                     f", message.chat.id: {message.chat.id}, "
                     f", message:'{message.text}'"
                     f", phone_flag: {phone_flag}"
                     f", mainwin_flag: {mainwin_flag}"
                     f", calc_flag: {calc_flag}"
                     f", action_status: {action_status}")


# @bot.message_handler(commands=['start'])


# @bot.message_handler(commands=['help'])
def help_executor(message):
    flags_status(message)
    if mainwin_flag:
        prompt = "/start\n" \
                 "/calc_start работа с калькулятором\n" \
                 "/phone_book работа с телефонной книгой\n" \
                 "/esc закончить работу\n\n" \
                 " сделайте ваш выбор: ..."
    if calc_flag:
        prompt = "/calc_start запустить вычисления\n" \
                 "/esc закончить работу с калькулятором\n\n" \
                 "сделайте ваш выбор: ..."
    if phone_flag:
        prompt = "выбор:-\n" \
                 "/add добавить контакт\n" \
                 "/view посмотреть контакты\n" \
                 "/contact выбрать и посмотреть контакт\n" \
                 "/edit редактировать контакт\n" \
                 "/delete удалить контакт\n " \
                 "/save сохоранить изменения\n" \
                 "/esc закончить работу с телефонным справочником\n\n" \
                 " сделайте ваш выбор: ..."
    bot.send_message(message.chat.id, prompt)
    flags_status(message)


# @bot.message_handler(commands=['calc'])
def calc_executor(message):
    global phone_flag
    global mainwin_flag
    global calc_flag
    global action_status

    phone_flag = False
    mainwin_flag = False
    flags_status(message)
    if '/calc_start' == message.text[:11]:
        calc_flag = True
        action_status = 'calc'
        # result = message.text[5:] + " = " + calculator.main_calculation(message.text[5:])
        result = 'введите выражение для вычесления: '
        bot.send_message(message.chat.id, result)
        flags_status(message)

        return
    if '/esc' == message.text[:10]:
        action_status = ''
        calc_flag = False
        mainwin_flag = True
        flags_status(message)
        return


def phone_command_executor(message):
    global phone_flag
    global mainwin_flag
    global calc_flag
    global action_status
    global contacts
    flags_status(message)

    if '/phone_book' == message.text[:11]:
        phone_flag = True
        mainwin_flag = False
        calc_flag = False
        logging.info(f" {current_time()}: {message.chat.id}: bot: 'phone_book run")
        prompt = "выбор:-\n" \
                 "/add добавить контакт\n" \
                 "/view посмотреть контакты\n" \
                 "/contact выбрать и посмотреть контакт\n" \
                 "/edit редактировать контакт\n" \
                 "/delete удалить контакт\n" \
                 "/save сохоранить изменения\n" \
                 "/esc закончить работу с телефонным справочником\n\n" \
                 " сделайте ваш выбор: ..."
        bot.send_message(message.chat.id, prompt)
        action_status = '/help'
        flags_status(message)
        return
    elif '/add' == message.text:
        action_status = 'add'
        out_message = "введите данные контакта через запятую,\n" \
                      "типа: Семенов, г.Москва, (812)-333-12-21, Семенов@почты.нет "
        bot.send_message(message.chat.id, out_message)
        flags_status(message)
        return
    elif '/view' == message.text:
        action_status = '/view'
        out_message = json.dumps(contacts, ensure_ascii=False, indent=4)
        bot.send_message(message.chat.id, out_message)
        flags_status(message)
        return
    elif '/contact' == message.text:
        action_status = 'name_contact'
        print(f'command_executor: {action_status}')
        out_message = "введите имя контакта: "
        bot.send_message(message.chat.id, out_message)
        flags_status(message)
        return
    elif '/edit' == message.text:
        action_status = '/edit'
        bot.send_message(message.chat.id, '''метод в разработке \n
        пока пользуйтесь удалением и последующим добавлением''')
        flags_status(message)
        return
    elif '/delete' == message.text:
        action_status = 'delete'
        if contact_name:
            contacts.pop(contact_name)
            bot.send_message(message.chat.id, f'{contact_name}: удален')
            save()
            action_status = ''
            flags_status(message)
        return
    elif '/save' == message.text:
        action_status = '/save'
        save()
        flags_status(message)
        return
    elif '/esc' == message.text:
        phone_flag = False
        mainwin_flag = True
        calc_flag = False
        action_status = ''
        bot.send_message(message.chat.id, 'уходим')
        flags_status(message)
        return


def text_executor(message):
    global phone_flag
    global mainwin_flag
    global calc_flag
    global action_status
    global contacts
    global contact_name
    print(f'text_executor: {action_status} , {message.text}')
    print(f'contact_name: {contact_name}')
    flags_status(message)
    if 'calc' == action_status:
        result = message.text + " = " + calculator.main_calculation(message.text)
        bot.send_message(message.chat.id, result)
        flags_status(result)
        return

    if '/view' == action_status:
        load()
        out_message = json.dumps(contacts, ensure_ascii=False, indent=4)
        bot.send_message(message.chat.id, out_message)
        flags_status(message)
        return

    if 'name_contact' == action_status:
        name = message.text
        if name in contacts:
            contact_name = name
            prompt = name + ' :\n'
            data = contacts[name]
            for k, v in data.items():
                prompt += (k + " : " + v)
            bot.send_message(message.chat.id, prompt)
            action_status = ''
            flags_status(message)
        return
    elif 'add' == action_status:
        message.text.replace(" ", "")
        data = message.text.split(',')
        print(data)
        name = data[0]
        details = {'address': data[1],
                   'phone': data[2],
                   'email': data[3]}
        prompt = ",".join(data) + " добавлен"
        contacts[name] = details
        bot.send_message(message.chat.id, prompt)
        save()
        action_status = ''
        flags_status(message)
        return
    elif '/edit' == message.text:
        bot.send_message(message.chat.id, '''метод в разработке \n/
                                          '(пока пользуйтесь удалением и последующим добавлением''')
        flags_status(message)
        return
    elif 'delete' == message.text:
        if contacts == {}:
            out_message = "телефонный справочник пуст ..."
            action_status = ''
            flags_status(message)
            return
        if contact_name == '':
            action_status = 'contact'  # delete
            out_message = "введите имя контакта: "
            bot.send_message(message.chat.id, out_message)
            flags_status(message)
            return
    elif '/save' == message.text:
        bot.send_message(message.chat.id, 'сохраняем')
        flags_status(message)
        return
    elif '/esc' == message.text:
        phone_flag = False
        mainwin_flag = True
        calc_flag = False
        bot.send_message(message.chat.id, 'уходим')
        flags_status(message)
        return


def save():
    global contacts
    global action_status
    action_status = 'save'

    with open("phone_book.json", 'w') as outfile:
        json.dump(contacts, outfile, ensure_ascii=False)
    flags_status('')


def load():
    global contacts
    global action_status
    action_status = 'load'

    with open("phone_book.json") as infile:
        contacts = json.load(infile)
    flags_status('')


# My_HTTP_API = '5832017456:AAHcjdu9neaYyKSrLEqXxqnU0PYAX8GftVU'
My_NAME = '@iRez_bot'
filename = "tg_bot_log.log"
maxBytes = 2 * 1024 * 256
backupCount = 2
contacts = {}
calc_flag = False
phone_flag = False
mainwin_flag = True
action_status = ''
contact_name = ''

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
    flags_status('')
except:
    flags_status('')

# bot.register_message_handler(start_executor, commands=['start'])
bot.register_message_handler(help_executor, commands=['start',
                                                      'hi',
                                                      'help'])
bot.register_message_handler(calc_executor, commands=['calc_start',
                                                      'esc'])
bot.register_message_handler(phone_command_executor, commands=['phone_book',
                                                               'add',
                                                               'view',
                                                               'contact',
                                                               'edit',
                                                               'delete',
                                                               'save',
                                                               'esc'])
bot.register_message_handler(text_executor)
# bot.register_message_handler(phone_text_executor, regexp=r'.+')

load()
bot.infinity_polling()
