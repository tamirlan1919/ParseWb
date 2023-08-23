import telebot
from config import BOT_TOKEN
import logging
import pandas as pd
from index import yes

bot = telebot.TeleBot(BOT_TOKEN)

# Use a dictionary to store user data
user_data = {}
text = ''
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Welcome! Please enter your email address:')
    bot.register_next_step_handler(message, get_email)

def get_email(message):
    email = message.text
    user_data[message.chat.id] = {'email': email}
    bot.send_message(message.chat.id, 'Thank you! Now, please enter the URL JSON:')
    bot.register_next_step_handler(message, get_message)

def get_message(message):

    message_text = message.text
    user_data[message.chat.id]['message'] = message_text
    bot.send_message(message.chat.id, 'Great! Finally, enter the URL you want to scrape:')
    bot.register_next_step_handler(message, get_url)

def get_url(message):
    url = message.text
    user_data[message.chat.id]['url'] = url
    print(user_data)
    # Now that we have all the user data, let's process it
    if message.chat.id in user_data:
        data = user_data[message.chat.id]
        texttt = user_data[message.chat.id]['message']
        bot.send_message(message.chat.id, f'Your input:\nEmail: {data["email"]}\nMessage: {data["message"]}\nURL: {data["url"]}')
        yes(url=url,text=texttt)
        document_path = 'products.csv'
            
            # Send the document
        with open(document_path, 'rb') as document:
            bot.send_document(message.chat.id, document)

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
