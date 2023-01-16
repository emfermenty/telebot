import telebot
import json
import requests
from config import *
from extensions import *

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты цену которой вы хотите узнать> \
<имя валюты в которой надо узнать цену первой валюты> \
<количество первой валюты>\nУвидить список всех доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def handle_value(message: telebot.types.Message):
    text_1 = 'Доступные валюты:'
    for key in keys.keys():
        text_1 = '\n'.join((text_1, key, ))
    bot.reply_to(message, text_1)

@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    values = message.text.split(" ")
    quote, base, amount = values
    r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={keys[quote]}&tsyms={keys[base]}')
    total_base = json.loads(r.content)[keys[base]]
    text = f'Цена {amount} {quote} в {base} - {total_base}'
    bot.send_message(message.chat.id, text)


bot.polling()