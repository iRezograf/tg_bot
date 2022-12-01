# tg_bot
Программа tg_bot, реализованная в боте iToora_bot, 
позволяет работать 
с калькулятором в боте. 
Расчет производится вызовом команды /calc  
с последущим выражением для расчета:
например, `/calc 25*4/20 +5*(2+2)`

## памятка для повторения кода в будущем
telebot & discord_bot

настройка venv. Инсталляция библиотеки telegram
PyCharm:
* Preference->Python Interpreter->Add Interpreter->
* -> Add Local Interpreter ->
* -> Virtualenv Environment (new)
* В проекте появится каталог venv
* обновить Терминал (например перезапуском проекта). 
* В коммандной строке появится префикс (venv)  

Обновляем pip python -m pip install --upgrade pip
Добавляем библиотеки:  

`pip install telebot`  
`pip install pyTelegramBotAPI` 
(это будет версия 4.7.1 С ней, пока, все работает)

Запускаем Telegram BotFather  
Создаем новый bot  
даем ему имя  
Получаем Токен
