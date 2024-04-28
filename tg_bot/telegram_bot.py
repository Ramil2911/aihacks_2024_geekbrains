import telebot
import requests
from telebot import types

flag = 0
NOW_ID = -1
classes = ['Позитивные комментарии',
            'Негативные комментарии',
            'Отношение позитивных комментариев к негативным',
            'Отношение количества сообщений за урок к среднему количеству сообщений',
            'Наиболее встречаемый класс сообщений',
            'Количество сообщений в чате']

# возвращает json чат по id 
def json_find_id(file, id):
    dl = len(file)
    for i in range(dl):
        if(file[i]['id'] == id):
            return i
    return -1

# Токен бота
TOKEN = '6542939962:AAGiQ0PGdH2tQjTVlCXccooWPuOV5Ab9I1A'

# URL вашего бэкенда
BACKEND_URL = '' # добавим позже 

# Создание экземпляра бота
bot = telebot.TeleBot(TOKEN)

# Функция для получения чатов из бэкенда
def get_backend_vebs():
    try:
        response = requests.get(f"{BACKEND_URL}/chats")
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except Exception as e:
        print(f"Ошибка при запросе к бэкенду: {e}")
        return []

# Функция для получения информации о конкретном чате из бэкенда
def get_backend_veb_from_id(chat_id):
    try:
        response = requests.get(f"{BACKEND_URL}/chats/{chat_id}")
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"Ошибка при запросе к бэкенду: {e}")
        return None
    
# получение метрики с бэка
def get_backend_metric(chat_id):
    veb = get_backend_veb_from_id(chat_id)
    if (veb != None):
        return veb["metrics"]
    else:
        return None

# ---------------------------------------------------------------------------------------------------------------------------------------------

# Показываем метрики
@bot.message_handler(func=lambda message: message.text == 'Показать метрики')
def handle_show_backend_chats(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    tmp_json = get_backend_veb_from_id[NOW_ID]['metrics']
    for i in range(len(tmp_json)):
        bot.send_message(message.chat.id, f"{classes[i]}: {tmp_json[i]}", reply_markup=set_action())
    return markup
# Меню выхода
def exit():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('В главное меню'))
    return markup

@bot.message_handler(func=lambda message: message.text == 'В главное меню')
def go_home(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.chat.id, "Идём в меню", reply_markup=main_menu())
    return markup

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я бот для общения в чатах. Используйте кнопки ниже для взаимодействия со мной.",
                     reply_markup=main_menu())

# Обработчик кнопки "Показать 10 интересных чатов с бэкенда"
@bot.message_handler(func=lambda message: message.text == 'Показать 10 интересных вебинаров')
def handle_show_backend_chats(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    backend_chats = get_backend_vebs()
    if backend_chats:
        bot.send_message(message.chat.id, "Список интересных вебинаров")
        for chat in backend_chats[:10]:
            bot.send_message(message.chat.id, f"ID: {chat['id']}")
        markup = choose_veb(message)
        return markup
    else:
        bot.send_message(message.chat.id, "Не удалось получить данные о вебинарах с бэкенда. Попробуйте позже.",
                         reply_markup=main_menu())
    return markup

# Обработчик кнопки "выбрать вебинар"
@bot.message_handler(func=lambda message: message.text == 'Выбрать вебинар')
def choose_veb(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Выход в меню'))
    bot.send_message(message.chat.id, 'Введите id вебинара', reply_markup = exit())
    return markup

@bot.message_handler(func=lambda message: True)
def numb(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Выход в меню'))
    
    chat_id = message.chat.id
    text = message.text
    try:
        num = int(text)
        chat = get_backend_veb_from_id(num)['data']
        NOW_ID = num
        if (chat != None):
            for i in range(0, len(chat)):
                bot.send_message(chat_id, f"\nСообщение {i} \n{str(chat[i])}", reply_markup=set_action())
        else:
            bot.send_message(message.chat.id, "Вебинар с таким id не найден.", reply_markup=set_action()) #,                       reply_markup=choose_veb())
        return markup
    except:
        return None

# Меню выбор действия
def set_action():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Показать метрики'),
               types.KeyboardButton('В главное меню'),
               )
    return markup

# Главное меню
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Выбрать вебинар'),
               types.KeyboardButton('Показать 10 интересных вебинаров'))
    return markup

#0 Запуск бота
bot.polling()

