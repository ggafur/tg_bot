import telebot
from telebot import types
from random import randint
token = '5682877056:AAE6Chk2o7cXoEzeEZ-LR05_aLpki22qPeQ'
bot = telebot.TeleBot(token)
name = ''
surname = ''
age = 0


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/reg':
        bot.send_message(message.from_user.id, "Как тебя зовут?")
        bot.register_next_step_handler(message, get_name) #следующий шаг – функция get_name
    elif message.text == '/button':
        button_message(message)
    elif message.text == 'Кубик':
        x = randint(1, 6)
        bot.send_message(message.chat.id, str(x))
    elif message.text == 'Монетка':
        x = randint(1, 2)
        if x == 1:
            bot.send_message(message.chat.id, 'Решка')
        else:
            bot.send_message(message.chat.id, 'Орёл')
    elif message.text == '/weather':
        bot.send_message(message.chat.id, 'https://yandex.ru/pogoda/dmitrov?lat=56.342906&lon=37.517611')


def get_name(message): #получаем фамилию
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?')
    bot.register_next_step_handler(message, get_surname)


def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, 'Сколько тебе лет?')
    bot.register_next_step_handler(message, get_age)


def get_age(message):
    global age
    try:
        age = int(message.text) #проверяем, что возраст введен корректно
    except Exception:
        bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
    bot.send_message(message.from_user.id, 'Тебе '+str(age)+' лет, тебя зовут '+name+' '+surname+'?')
    with open('log.txt', 'a') as f:
        f.writelines(name+' '+surname+' '+str(age)+'\n')


@bot.message_handler(commands=['button'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Кубик")
    item2 = types.KeyboardButton("Монетка")
    markup.add(item1)
    markup.add(item2)
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)


bot.infinity_polling()