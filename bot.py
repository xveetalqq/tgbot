import requests
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import random
import nest_asyncio

# Для підтримки асинхронності в середовищі Jupyter або інших
nest_asyncio.apply()

# Встановлення рівня логування
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен бота
TOKEN = "8142156002:AAEEV7pyWecJmZbbaW9AgVmRynzRP7YH6dM"

# API ключ для погоди (Заміни на свій API ключ)
WEATHER_API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

# Функція отримання погоди
def get_weather(city: str) -> str:
    try:
        response = requests.get(WEATHER_API_URL, params={
            'q': city,
            'appid': WEATHER_API_KEY,
            'units': 'metric',
            'lang': 'uk'
        })
        data = response.json()
        if data.get('cod') != 200:
            return "Не вдалося отримати погоду. Спробуйте ще раз."
        main = data['main']
        weather = data['weather'][0]
        temperature = main['temp']
        description = weather['description']
        return f"Погода в місті {city}: {temperature}°C, {description}."
    except Exception as e:
        return f"Сталася помилка при отриманні погоди: {e}"

# Функція отримання часу
def get_current_time() -> str:
    now = datetime.now()
    return now.strftime("%H:%M:%S, %d-%m-%Y")

# Випадкові жарти
jokes = [
    "Чому програмісти не можуть грати в хованки? Тому що вони завжди знаходять помилки!",
    "Якщо комп'ютер зависає, спробуйте вимкнути його і вмикнути знову... інакше просто почекайте, це питання до алгоритмів.",
    "Чому банани ніколи не можуть приховувати свої емоції? Тому що вони завжди виявляються в шкурці.",
    "Прокачав інтернет до 1 Гб/с, але коли заглянув у витрати, зрозумів, що таке швидкість зовсім не допомогла."
]

# Отримуємо випадковий жарт
def get_random_joke() -> str:
    return random.choice(jokes)

# Функція отримання випадкової новини
def get_random_news():
    news_list = [
        "Світовий ринок нафти стабільно зростає: аналітики прогнозують подальше збільшення попиту.",
        "Україна планує збільшити експорт агропродукції на 10% до кінця року.",
        "Новий смартфон від Apple: революційний дизайн та поліпшена камера.",
        "Європейські країни анонсували нові санкції проти Росії через порушення прав людини.",
        "Вчені виявили новий вид бактерій, які можуть допомогти в лікуванні раку."
    ]
    return random.choice(news_list)

# Функція отримання випадкової смішної картинки (мем)
def get_random_funny_image() -> str:
    try:
        # API для мемів
        url = "https://api.imgflip.com/get_memes"
        response = requests.get(url)
        data = response.json()
        if data["success"]:
            memes = data["data"]["memes"]
            random_meme = random.choice(memes)
            return random_meme["url"]
        else:
            return "Не вдалося отримати картинку."
    except Exception as e:
        return f"Сталася помилка при отриманні картинки: {e}"

# Функція старту
async def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    await update.message.reply_text(
        f"Привіт, {user.first_name}! Я бот, і готовий допомогти. Для вибору, натискай кнопки.",
        reply_markup=ReplyKeyboardMarkup(
            [['Погода', 'Час'], ['Переклад', 'Жарт'], ['Новина', 'Картинка']], resize_keyboard=True
        )
    )

# Обробка повідомлення
async def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text

    # Перевірка, чи користувач хоче дізнатися погоду чи переклад
    if text == "Погода":
        await update.message.reply_text("Введіть місто, щоб дізнатися погоду:")
        # Додамо стан, щоб бот чекав місто
        context.user_data['action'] = 'weather'
    elif text == "Час":
        current_time = get_current_time()
        await update.message.reply_text(f"Поточний час: {current_time}")
    elif text == "Переклад":
        await update.message.reply_text("Введіть текст для перекладу:")
        # Додамо стан, щоб бот чекав текст для перекладу
        context.user_data['action'] = 'translate'
    elif text == "Жарт":
        joke = get_random_joke()
        await update.message.reply_text(f"Ось жарт: {joke}")
    elif text == "Новина":
        news = get_random_news()
        await update.message.reply_text(f"Ось новина: {news}")
    elif text == "Картинка":
        image_url = get_random_funny_image()
        await update.message.reply_photo(image_url)
    else:
        # Якщо бот чекає введення міста чи тексту, обробимо це
        action = context.user_data.get('action')
        if action == 'weather':
            city = update.message.text
            weather_info = get_weather(city)
            await update.message.reply_text(weather_info)
            context.user_data['action'] = None  # Скидаємо стан після обробки
        elif action == 'translate':
            text_to_translate = update.message.text
            # Переклад (потрібна реальна логіка перекладу)
            translated_text = text_to_translate  # Замість цього має бути функція перекладу
            await update.message.reply_text(f"Переклад: {translated_text}")
            context.user_data['action'] = None  # Скидаємо стан після обробки
        else:
            await update.message.reply_text("Я не розумію це повідомлення. Спробуйте ще раз!")

# Обробка помилок
def error(update: Update, context: CallbackContext) -> None:
    logger.warning('Помилка: "%s" при обробці запиту "%s"', context.error, update)

# Основна функція запуску бота
async def main() -> None:
    """Запуск бота."""
    # Створення об'єкта додатка
    application = Application.builder().token(TOKEN).build()

    # Реєстрація обробників
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Логування помилок
    application.add_error_handler(error)

    # Запуск бота в режимі polling
    await application.run_polling()

# Запуск основної функції
if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
