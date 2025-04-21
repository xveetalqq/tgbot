import telebot
import requests
from datetime import datetime
import pytz

# Введи свій токен
bot = telebot.TeleBot('8142156002:AAEEV7pyWecJmZbbaW9AgVmRynzRP7YH6dM')

# Список для адаптації під людину
user_data = {}

# Обробка команди "/start"
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привіт! Я твій новинний бот. Я можу показати час і новини. Просто напиши 'час' або 'новини'!")

# Обробка команди "/time"
@bot.message_handler(commands=['time'])
def send_time(message):
    tz = pytz.timezone('Europe/Kiev')  # зміни на свою зону, якщо треба
    now = datetime.now(tz)
    time_str = now.strftime("%H:%M:%S")
    bot.reply_to(message, f"Поточний час: {time_str}")

# Обробка команди "/news"
@bot.message_handler(commands=['news'])
def send_news(message):
    # Встав свій API ключ для новин
    api_key = 'ТВОЙ_API_KEY'
    url = f'http://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'
    response = requests.get(url)
    news_data = response.json()

    if news_data['status'] == 'ok':
        articles = news_data['articles']
        top_news = "\n".join([f"{i+1}. {article['title']}" for i, article in enumerate(articles[:5])])
        bot.reply_to(message, f"Ось топ 5 новин:\n{top_news}")
    else:
        bot.reply_to(message, "Не вдалося отримати новини. Спробуйте ще раз пізніше.")

# Обробка повідомлень для адаптації
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {
            'name': message.from_user.first_name
        }

    # Адаптація під користувача
    bot.reply_to(message, f"Привіт, {user_data[user_id]['name']}! Якщо хочеш дізнатися час, надішли команду 'час'. Якщо хочеш новини — 'новини'.")

# Запуск бота
bot.polling()
