import telebot
import requests
from datetime import datetime
import pytz

bot = telebot.TeleBot('8142156002:AAEEV7pyWecJmZbbaW9AgVmRynzRP7YH6dM')

user_data = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привіт! Я твій новинний бот. Напиши 'час' або 'новини'!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    text = message.text.lower()

    if user_id not in user_data:
        user_data[user_id] = {'name': message.from_user.first_name}

    if text == "час":
        tz = pytz.timezone('Europe/Kiev')
        now = datetime.now(tz).strftime("%H:%M:%S")
        bot.reply_to(message, f"Поточний час: {now}")

    elif text == "новини":
        api_key = 'ТВОЙ_API_KEY'  # Замінити на справжній API ключ
        url = f'http://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'
        response = requests.get(url).json()

        if response['status'] == 'ok':
            articles = response['articles']
            top_news = "\n".join([f"{i+1}. {article['title']}" for i, article in enumerate(articles[:5])])
            bot.reply_to(message, f"📰 Ось топ 5 новин:\n{top_news}")
        else:
            bot.reply_to(message, "Не вдалося отримати новини. Спробуй пізніше.")

    else:
        bot.reply_to(message, f"Привіт, {user_data[user_id]['name']}! Напиши 'час' або 'новини'.")

bot.polling()
