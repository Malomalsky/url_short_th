import requests
import os
import json
import telebot

TOKEN = os.getenv('URL_SH_TOKEN')

bot = telebot.TeleBot(TOKEN)
URL = 'https://url-sh0rt.herokuapp.com'

@bot.message_handler(commands=['post_orig'], content_types=['text'])
def add_short_link(message):
    try:    
        data = json.dumps({"original_url": telebot.util.extract_arguments(message.text).split(' ')[0]})
        req = requests.post(URL+'/add_link', data=data)
        bot.reply_to(message, URL+'/'+req.json()['short_url'])
    except IndexError:
        bot.reply_to(message, 'Отправьте ссылку!')
    except KeyError:
        bot.reply_to(message, req.text)

@bot.message_handler(commands=['post_custom'], content_types=['text'])
def add_custom_link(message):
    try:
        data = json.dumps({"original_url": telebot.util.extract_arguments(message.text).split(' ')[0], "custom_url":  telebot.util.extract_arguments(message.text).split(' ')[1]})
        req = requests.post(URL+'/add_link', data=data)
        bot.reply_to(message, URL+'/'+req.json()['short_url'])
        bot.reply_to(message, URL+'/'+req.json()['custom_url'])
    except IndexError:
        bot.reply_to(message, text='Отправьте команду в формате: \ncommand original_url custom_url')
    except KeyError:
        bot.reply_to(message, req.text)

@bot.message_handler(commands=['get'])
def get_link_by_id(message):
        try:
            req = requests.get(URL+'/links/'+message.text.split(' ')[1] )
            bot.reply_to(message, req.text)

        except IndexError:
            bot.reply_to(message, text='Отправьте команду в формате: \ncommand id')
        except KeyError:
            bot.reply_to(message, req.text)




bot.polling()
