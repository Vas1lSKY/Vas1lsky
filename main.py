import random
import telebot
from telebot import types
import logging
import sqlite3
import os
import time  # Добавлен импорт модуля time
from flask import Flask
from threading import Thread
# Токен бота
TOKEN = '7828109094:AAH9dvP1jfeWjBPXGajs3hsYYn9kH4-7Nns'
bot = telebot.TeleBot(TOKEN)

# Инициализация Flask-приложения
app = Flask(__name__)
# Простой маршрут для проверки работоспособности
@app.route('/')
def home():
    return "Hello, your bot is running!"

# Запуск Flask-приложения в отдельном потоке
def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 4000)))
# Запуск Telegram-бота
def run_bot():
    bot.polling(none_stop=True)

if __name__ == "__main__":
    # Запускаем Flask в отдельном потоке
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Запускаем Telegram-бота
    run_bot()

# Настройка логирования
logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Установка рабочей директории
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

# Подключение к базе данных
DB_PATH = 'users.db'


def init_db():
    """Инициализация базы данных."""
    with sqlite3.connect(DB_PATH, check_same_thread=False) as conn:
        cursor = conn.cursor()
        # Включение поддержки внешних ключей
        cursor.execute("PRAGMA foreign_keys = ON")
        # Создание таблицы users
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            user_id INTEGER UNIQUE,
            name TEXT,
            phone TEXT
        )
        ''')
        # Создание таблицы orders
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            device TEXT,
            problem TEXT,
            actions_taken TEXT,
            status TEXT DEFAULT 'new',
            condition TEXT,
            diagnosis TEXT,
            work_done TEXT,
            guarantee TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        ''')
        # Создание таблицы masters
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS masters (
            username TEXT PRIMARY KEY,
            password TEXT,
            chat_id INTEGER  -- Новый столбец для chat_id
        )
        ''')
        # Добавление мастеров (если их нет)
        cursor.executemany(
            "INSERT OR IGNORE INTO masters (username, password) VALUES (?, ?)",
            [("Vas1lSKY", "1488"), ("MasterSKY", "1590")]
        )
        # Добавление новых столбцов в таблицу orders (если их нет)
        for column in ['condition', 'diagnosis', 'work_done', 'guarantee']:
            try:
                cursor.execute(f"ALTER TABLE orders ADD COLUMN {column} TEXT")
            except sqlite3.OperationalError:
                pass
            try:
                cursor.execute("ALTER TABLE orders ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
            except sqlite3.OperationalError:
                pass  # Столбец уже существует
        # Добавление нового столбца chat_id в таблицу masters
        try:
            cursor.execute("ALTER TABLE masters ADD COLUMN chat_id INTEGER")
        except sqlite3.OperationalError:
            pass  # Столбец уже существует


# Инициализация базы данных
init_db()


user_context = {}


# Главное меню с кнопками в порядке 2-1-2-1-2
def create_main_menu_markup():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_repair = types.KeyboardButton("🛠️ Ремонт")
    button_guarantee = types.KeyboardButton("🛡️ Гарантия")
    button_earn = types.KeyboardButton("💰 Заработай")
    button_working = types.KeyboardButton("⚙️ Как работаем")
    button_contact = types.KeyboardButton("📞 Связь")
    button_sale = types.KeyboardButton("📱 Продажа техники")
    button_booking = types.KeyboardButton("📅 Запись на ремонт")
    button_tic_tac_toe = types.KeyboardButton("🛡Топ VPN №1")

    # Порядок кнопок: 2-1-2-1-2
    markup.add(button_repair, button_guarantee)
    markup.add(button_earn)
    markup.add(button_working, button_contact)
    markup.add(button_sale)
    markup.add(button_booking, button_tic_tac_toe)
    return markup

from utils import create_vertical_markup, safe_handler  # Импортируем функцию

@bot.message_handler(func=lambda m: m.text == "📱 Продажа техники")
def sell_technology(message):
    buttons = [
        "🍏 Техника Apple",
        "📊 Андройд",
        "🎧 Наушники",
        "📱 Аксессуары",
        "🔙 Назад"
    ]
    chat_id = message.chat.id
    user_context[chat_id] = "sell_technology"
    markup = create_vertical_markup(buttons)  # Используем функцию
    bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=markup)


# Обработка кнопки "Техника Apple"
@bot.message_handler(func=lambda message: message.text == "🍏 Техника Apple")
def apple_technology(message):
    chat_id = message.chat.id
    user_context[chat_id] = "apple_technology"  #
    buttons = [
        "iPhone 11/12/SE",
        "iPhone 13",
        "iPhone 14/Plus/Pro Max",
        "iPhone 15/Plus/Pro/Pro Max",
        "iPhone 16/se/Plus",
        "iPhone 16Pro/Pro Max",
        "🔙 Назад"
    ]
    markup = create_vertical_markup(buttons)
    bot.send_message(
        message.chat.id,
        "Выберите модель Apple устройства:",
        reply_markup=markup
    )


# Обработка кнопки "iiPhone 11/12/SE"
@bot.message_handler(func=lambda message: message.text == "iPhone 11/12/SE")
def iphone_12_prices(message):
    bot.send_message(
        message.chat.id,
        """📱 iPhone 11/12/SE

iPhone 12 Mini

12 Mini 64 Black — 46.500 🇺🇸
12 Mini 64 Blue — 46.500 🇺🇸
12 Mini 64 White — 46.500 🇺🇸
12 Mini 64 Green — 46.500 🇺🇸
12 Mini 64 Purple — 46.500 🇺🇸

12 Mini 128 Black — 53.800 🇺🇸
12 Mini 128 Blue — 53.800 🇺🇸
12 Mini 128 White — 53.800 🇺🇸

iPhone 11

11 64 Black — 35.300 🇮🇳
11 64 White — 37.900 🇮🇳

11 128 Black — 40.900 🇮🇳
11 128 Yellow — 43.800 🇺🇸

11 256 Red — 44.000 🇺🇸
11 256 Purple — 44.000 🇺🇸
11 256 White — 44.000 🇺🇸
SE 3

SE 3 64 Black — 40.200 🇺🇸
SE 3 64 Red — 40.300 🇺🇸
SE 3 64 White — 40.500 🇺🇸

iPhone 12

12 64 Black — 38.000 🇺🇸
12 64 Blue — 40.400 🇮🇳
12 64 Purple — 40.400 🇮🇳
12 64 White — 40.400 🇮🇳
12 64 Green — 41.000 🇮🇳
12 64 Red — 41.500 🇦🇪

12 128 Black — 43.800 🇮🇳
12 128 Green — 44.000 🇮🇳
12 128 Purple — 44.000 🇮🇳
12 128 White — 44.000 🇮🇳
12 128 Blue — 44.300 🇺🇸""",
    )


# Обработка кнопки "iPhone 13"
@bot.message_handler(func=lambda message: message.text == "iPhone 13")
def iphone_13_prices(message):
    bot.send_message(
        message.chat.id,
        """📱 iPhone 13
        
13 128 Blue — 46.400 🇳🇪
13 128 Midnight — 45.000 🇮🇳
13 128 Starlight — 45.700 🇮🇳

13 256 Black — 63.300 🇺🇸
13 256 Red — 62.300 🇮🇳

13 512 Blue — 66.500 🇮🇳
13 512 Black — 67.000 🇮🇳
13 512 Green — 66.200 🇮🇳
13 512 Pink — 66.500 🇮🇳
13 512 Red — 64.000 🇮🇳
13 512 White — 66.800 🇮🇳""",
    )


# Обработка кнопки "iPhone 14"
@bot.message_handler(func=lambda message: message.text == "iPhone 14/Plus/Pro Max")
def iphone_14_prices(message):
    bot.send_message(
        message.chat.id,
        """📱 📱 iPhone 14
        
128 ГБ

14 128 Midnight — 51.800 🇮🇳
14 128 Midnight — 50.000 🇺🇸
14 128 Starlight — 51.900 🇮🇳
14 128 Blue — 52.400 🇮🇳
14 128 Blue — 50.000 🇺🇸
14 128 Yellow — 52.500 🇮🇳
14 128 Red — 50.000 🇮🇳

256 ГБ

14 256 Black — 64.500 🇮🇳
14 256 Starlight — 65.000 🇮🇳
14 256 Yellow — 66.700 🇸🇬
14 256 Red — 62.300 🇮🇳

512 ГБ

14 512 Yellow — 75.000 🇮🇳
14 512 Black — 71.200 🇺🇸
14 512 Yellow — 69.000 🇺🇸

📱 iPhone 14 Plus

128 ГБ
14 Plus 128 Yellow — 64.000 🇯🇵
14 Plus 128 Purple — 66.500 🇮🇳

512 ГБ

14 Plus 512 Red — 70.400 🇯🇵🇨🇦

📱 iPhone 14 Pro Max

256 ГБ

14 Pro 256 Purple — 92.200 🇺🇸
14 Pro Max 256 Gold — 92.200 🇺🇸
14 Pro Max 256 White — 92.200 🇺🇸

512 ГБ

14 Pro Max 512 Gold — 104.800 🇦🇪

1TB (1024 ГБ)

14 Pro Max 1TB White — 106.900 🇦🇪
14 Pro Max 1TB White — 102.200 🇺🇸
14 Pro Max 1TB Gold — 106.900 🇦🇪
14 Pro Max 1TB Black — 102.200 🇺🇸
14 Pro Max 1TB Purple — 102.200 🇺🇸""",
    )

# Обработка кнопки "iPhone 15"
@bot.message_handler(func=lambda message: message.text == "iPhone 15/Plus/Pro/Pro Max")
def iphone_15_prices(message):
    bot.send_message(
        message.chat.id,
        """📱 iPhone 15
        
128 ГБ

15 128 Black — 65.700 🇮🇳
15 128 Black — 63.000 🇺🇸
15 128 Pink — 65.600 🇮🇳
15 128 Pink — 63.000 🇺🇸
15 128 Green — 65.700 🇳🇪
15 128 Green — 63.000 🇺🇸
15 128 Blue — 64.200 🇮🇳
15 128 Blue — 63.000 🇺🇸

256 ГБ

15 256 Black — 76.000 🇮🇳
15 256 Black ASIS — 68.500 🇭🇰!
15 256 Pink — 76.000 🇮🇳
15 256 Pink — 73.200 🇺🇸
15 256 Blue — 73.800 🇮🇳
15 256 Green — 75.700 🇮🇳
15 256 Yellow — 77.000 🇮🇳
15 256 Yellow — 75.000 🇺🇸
15 256 Yellow ASIS — 68.500 🇭🇰!

512 ГБ

15 512 Blue ASIS — 71.300 🇭🇰
15 512 Black ASIS — 71.300 🇭🇰!
15 512 Green ASIS — 71.300 🇭🇰!
15 512 Yellow — 94.900 🇮🇳
15 512 Yellow — 84.000 (замена в СЦ)
15 512 Yellow ASIS — 71.300 🇭🇰
15 512 Pink ASIS — 72.000 🇭🇰

📱 iPhone 15 Plus

128 ГБ

15 Plus 128 Black — 74.400 🇦🇪
15 Plus 128 Yellow — 73.400 🇰🇼

256 ГБ

15 Plus 256 Black — 86.000 🇦🇪
15 Plus 256 Green — 86.000 🇦🇪
15 Plus 256 Yellow — 88.000 🇦🇪

📱 iPhone 15 Pro

128 / 256 / 512 / 1TB

15 Pro 128 Blue — 88.700 🇰🇼
15 Pro 128 Blue — 86.200 🇭🇰 (2Sim)
15 Pro 128 Blue — 87.000 🇺🇸*
15 Pro 128 White — 88.000 🇰🇼

📱 iPhone 15 Pro Max

256 / 512 / 1TB

15 Pro Max 256 Natural — 106.500 🇯🇵🇰🇼
15 Pro Max 256 Natural — 104.000 🇺🇸
15 Pro Max 256 Blue — 107.400 🇦🇪🇸🇬
15 Pro Max 256 White — 109.200 🇨🇳 (2 Sim)
15 Pro Max 512 Blue — 115.200 🇯🇵
15 Pro Max 512 Natural — 116.700 🇦🇪
15 Pro Max 512 White — 116.700 🇦🇪
15 Pro Max 512 Black — 113.500 🇺🇸""",
    )


# Обработка кнопки "iPhone 16"
@bot.message_handler(func=lambda message: message.text == "iPhone 16/se/Plus")
def iphone_16_prices(message):
    bot.send_message(
        message.chat.id,
        """📱 IPHONE 16/se/Plus
128 ГБ

16Е 128 Black — 56.900 🇮🇳
16E 128 White — 57.800 🇮🇳

256 ГБ

16Е 256 Black — 68.900 🇮🇳
16Е 256 Black — 65.000 🇺🇸
16E 256 White — 68.900 🇮🇳
16E 256 White — 65.000 🇺🇸

512 ГБ

16E 512 White — 🚗
16E 512 White — 76.200 🇺🇸
16Е 512 Black — 87.500 🇮🇳
16Е 512 Black — 🚗

16 128 ГБ

16 128 Teal — 71.500 🇮🇳
16 128 Teal — 69.500 🇺🇸
16 128 White — 71.300 🇮🇳
16 128 Black — 71.300 🇮🇳
16 128 Black — 69.500 🇺🇸
16 128 Pink — 71.400 🇮🇳
16 128 Pink — 69.500 🇺🇸
16 128 Ultramarine — 71.000 🇮🇳
16 128 Ultramarine — 69.500 🇺🇸

16 256 ГБ

16 256 Black — 81.500 🇮🇳
16 256 Black — 78.500 🇺🇸
16 256 White — 80.000 🇮🇳
16 256 White — 78.500 🇺🇸
16 256 Teal — 80.500 🇮🇳
16 256 Teal — 78.500 🇺🇸
16 256 Ultramarine — 81.900 🇮🇳
16 256 Ultramarine — 78.500 🇺🇸
16 256 Pink — 81.900 🇮🇳
16 256 Pink — 78.500 🇺🇸

16 512 ГБ

16 512 Black — 104.500 🇮🇳
16 512 Teal — 104.500 🇮🇳
16 512 Teal — 93.200 🇺🇸
16 512 Ultramarine — 104.500 🇮🇳
16 512 Ultramarine — 93.200 🇺🇸

📱 IPHONE 16 Plus

128 ГБ

16 Plus 128 Ultramarine — 80.500 🇮🇳
16 Plus 128 Ultramarine — 77.600 🇺🇸
16 Plus 128 Ultramarine — 74.500 🇺🇸 актив
16 Plus 128 Teal — 81.500 🇮🇳
16 Plus 128 Teal — 74.500 🇺🇸 Актив
16 plus 128 Black — 80.500 🇮🇳
16 plus 128 Black — 77.600 🇺🇸
16 plus 128 Black — 74.500 🇺🇸 актив
16 Plus 128 White — 80.800 🇮🇳
16 Plus 128 White — 78.000 🇮🇳 актив
16 Plus 128 Pink — 86.500 🇮🇳
16 Plus 128 Pink — 77.600 🇺🇸
16 Plus 128 Pink — 74.500 🇺🇸 Актив

256 ГБ

16 Plus 256 Black — 93.800 🇮🇳
16 Plus 256 Ulramarine — 94.900 🇮🇳
16 Plus 256 Teal — 96.000 🇮🇳
16 Plus 256 White — 91.000 🇮🇳
16 Plus 256 Pink — 93.300 🇮🇳

512 ГБ

16 Plus 512 Pink — 132.500 🇮🇳
16 Plus 512 Teal — 132.500 🇮🇳
16 Plus 512 Black — 132.500 🇯🇵
""",
    )


# Обработка кнопки "MacBook"
@bot.message_handler(func=lambda message: message.text == "iPhone 16Pro/Pro Max")
def macbook_prices(message):
    bot.send_message(
        message.chat.id,
        """Цены iPhone 16Pro/Pro Max
📱 IPHONE 16 Pro

128 ГБ

16 Pro 128 Natural — 94.600 🇯🇵🇪🇺
16 Pro 128 Natural — 88.000 🇺🇸 Актив
16 Pro 128 Natural — 91.000 (актив/раскрыт)
16 Pro 128 Desert — 92.800 🇯🇵🇪🇺
16 Pro 128 Desert — 96.000 🇨🇳 2 sim
16 Pro 128 Desert — 85.900 🇺🇸*
16 Pro 128 Desert — 85.000 🇺🇸 актив *
16 Pro 128 Desert — 85.000 (замена в СЦ)
16 Pro 128 White — 93.600 🇯🇵🇪🇺
16 Pro 128 White — 96.200 🇭🇰 2sim
16 Pro 128 Black — 94.600 🇯🇵🇪🇺
16 Pro 128 Black — 88.000 🇺🇸
16 Pro 128 Black — 96.200 🇨🇳 2 sim

256 ГБ

16 Pro 256 Natural — 103.500 🇯🇵🇰🇼
16 Pro 256 Desert — 98.500 🇯🇵🇰🇼
16 Pro 256 Desert — 95.100 🇺🇸
16 Pro 256 Desert — 92.000 (замена платы в ОСЦ) 🇪🇺
16 Pro 256 White — 101.900 🇯🇵🇦🇪
16 Pro 256 White — 94.500 🇺🇸*
16 Pro 256 Black — 101.600 🇪🇺🇯🇵
16 Pro 256 Black — 97.600 🇺🇸

512 ГБ

16 Pro 512 Natural — 129.200 🇯🇵
16 Pro 512 Desert — 127.500 🇰🇼🇯🇵
16 Pro 512 Desert — 120.900 🇺🇸*
16 Pro 512 Desert — 111.000 🇰🇷 ASIS*
16 Pro 512 White — 125.500 🇯🇵🇰🇼
16 Pro 512 White — 111.000 🇰🇷 ASIS*
16 Pro 512 White — 120.900 🇺🇸*
16 Pro 512 Black — 129.400 🇰🇼🇯🇵
16 Pro 512 Black — 118.300 🇺🇸
16 Pro 512 Black — 118.000 🇺🇸 актив *

1TB

16 Pro 1TB Black — 145.900 🇰🇼🇯🇵
16 Pro 1TB Black — 136.300 🇺🇸
16 Pro 1TB White — 144.900 🇰🇼🇯🇵
16 Pro 1TB White — 137.000 🇺🇸*
16 Pro 1TB Natural — 145.700 🇯🇵
16 Pro 1TB Natural — 136.300 🇺🇸
16 Pro 1TB Desert — 144.900 🇰🇼🇯🇵

📱 IPHONE 16 Pro Max

256 ГБ

16 Pro Max 256 Black — 110.800 🇯🇵🇰🇼
16 Pro Max 256 Black — 105.800 🇺🇸
16 Pro Max 256 Black — 103.000 🇺🇸 актив
16 Pro Max 256 White — 111.300 🇯🇵🇰🇼
16 Pro Max 256 White — 107.000 🇺🇸*
16 Pro Max 256 Natural — 111.300 🇰🇼🇯🇵🇸🇬
16 Pro Max 256 Natural — 104.000 🇺🇸 Актив
16 Pro Max 256 Desert — 110.300 🇻🇳🇯🇵
16 Pro Max 256 Desert — 107.000 🇺🇸
16 Pro Max 256 Desert — 104.000 🇺🇸 актив

512 ГБ

16 Pro Max 512 Black — 126.900 🇯🇵
16 Pro Max 512 Black — 124.200 🇺🇸
16 Pro Max 512 White — 126.600 🇯🇵
16 Pro Max 512 White — 124.900 ASIS 🇯🇵!
16 Pro Max 512 White — 124.20 🇺🇸
16 Pro Max 512 Natural — 126.900 🇯🇵
16 Pro Max 512 Natural — 123.000 🇺🇸 Актив
16 Pro Max 512 Desert — 126.000 🇯🇵🇰🇼
16 Pro Max 512 Desert — 124.200 🇺🇸
16 Pro Max 512 Desert — 123.000 (замена в СЦ)

1TB

16 Pro Max 1TB Black — 156.900 🇯🇵
16 Pro Max 1TB Black — 136.300 🇺🇸
16 Pro Max 1TB Black — 131.500 🇺🇸 актив
16 Pro Max 1TB White — 153.500 🇯🇵
16 Pro Max 1TB White — 138.000 🇯🇵 (актив до 2 мес)
16 Pro Max 1TB White — 139.200 🇺🇸
16 Pro Max 1TB Natural — 153.900 🇯🇵
16 Pro Max 1TB Natural — 152.000 🇰🇼 (микро скол на камере)
16 Pro Max 1TB Desert — 151.500 🇯🇵
16 Pro Max 1TB Desert — 134.800 🇺🇸""",
    )


# Обработка кнопки "Техника Андройд"
@bot.message_handler(func=lambda message: message.text == "📊 Андройд")
def android_technology(message):
    buttons = [
        "Samsung",
        "Xiaomi/Redmi/Note",
        "POCO",
        "HUAWEI/HONOR",
        "PIXEL/ONE PLUS",
        "🔙 Назад"
    ]
    chat_id = message.chat.id
    user_context[chat_id] = "android"
    markup = create_vertical_markup(buttons)
    bot.send_message(
        message.chat.id,
        "Выберите бренд устройства:",
        reply_markup=markup
    )


@bot.message_handler(func=lambda message: message.text == "Samsung")
def samsung_prices(message):
    bot.send_message(
        message.chat.id,
        """Цены на Samsung:

🎧A06 4/64 Black — 12.800 🇰🇿
🎧A06 4/64 Gold — 12.800 🇰🇿
🎧A06 4/64 Light Blue — 12.800 🇰🇿
🎧A06 4/128 Black — 13.500 🇦🇪
🎧A06 4/128 Gold — 13.500 🇦🇪
🎧A06 4/128 Light Blue — 13.500 🇦🇪
🎧A06 6/128 Black — 14.300 🇦🇪
🎧A06 6/128 Gold — 14.300 🇦🇪
🎧A06 6/128 Light Blue — 14.300 🇦🇪

🎧A16 4/128 Black — 16.300 🇦🇪
🎧A16 4/128 Gray — 16.200 🇦🇪
🎧A16 4/128 Green — 16.200 🇦🇪
🎧A16 6/128 Black — 17.000 🇦🇪
🎧A16 6/128 Gray — 17.000 🇦🇪
🎧A16 6/128 Green — 17.000 🇦🇪
🎧A16 8/256 Black — 20.300 🇦🇪
🎧A16 8/256 Gray — 20.300 🇦🇪
🎧A16 8/256 Green — 20.300 🇦🇪

🎧A25 8/256 Yellow — 24.000 🇦🇪

🎧A26 6/128 Black — 23.100 🇦🇪
🎧A26 6/128 Pink — 23.100 🇦🇪
🎧A26 8/256 Pink — 24.700 🇦🇪
🎧A26 8/256 White — 24.700 🇦🇪

🎧A36 8/128 Black — 30.300 🇦🇪
🎧A36 8/128 Lavender — 30.300 🇦🇪
🎧A36 8/128 Lime — 30.300 🇦🇪
🎧A36 8/128 White — 30.300 🇦🇪
🎧A36 8/256 Black — 32.200 🇦🇪
🎧A36 8/256 Lavender — 32.200 🇰🇿
🎧A36 8/256 Lime — 32.200 🇦🇪
🎧A36 8/256 White — 29.000 🇰🇿

🎧A55 8/256 Icyblue — 36.600 🇨🇱
🎧A55 8/256 Navy — 36.600 🇨🇱
🎧A55 12/256 Navy — 37.500 🇪🇺

🎧A56 8/128 Graphite — 34.700 🇪🇺
🎧A56 8/128 Lightgray — 34.700 🇦🇪
🎧A56 8/128 Olive — 34.700 🇦🇪
🎧A56 8/128 Pink — 34.700 🇦🇪
🎧A56 8/256 Graphite — 37.100 🇰🇿
🎧A56 8/256 Olive — 37.100 🇦🇪
🎧A56 12/256 Graphite — 39.400 🇸🇬
🎧A56 12/256 Lightgray — 39.400 🇦🇪
🎧A56 12/256 Olive — 39.400 🇦🇪
🎧A56 12/256 Pink — 36.700 🇦🇪 (без изменений)

🎧S23 8/128 S911B Black — 44.600 🇮🇳
🎧S23 8/128 S911B Cream — 44.600 🇮🇳
🎧S23 8/128 S911B Green — 44.600 🇮🇳
🎧S23 8/128 S911B Lavender — 44.600 🇮🇳
🎧S23 8/256 S911B Cream — 49.000 🇮🇳

🎧S24 FE 8/256 S721B Gray — 44.900 🇦🇪
🎧S24 FE 8/256 S721B Mint — 44.900 🇦🇪
🎧S24 FE 8/512 S721B Gray — 50.900 🇨🇱

🎧S24 8/128 S921B Black — 48.200 🇮🇳
🎧S24 8/256 S921B Gray — 60.900 🇨🇱
🎧S24 8/256 S921B Yellow — 53.000 🇨🇱
🎧S24 8/512 S921B Black — 61.800 🇨🇱

🎧S24+ 12/256 S926B Black — 62.000 🇮🇳
🎧S24+ 12/256 S926B Violet — 62.000 🇮🇳
🎧S24+ 12/256 S926B Yellow — 54.900 🇨🇱

🎧S24 Ultra 12/256 S928B Black — 78.900 🇨🇱
🎧S24 Ultra 12/256 S928B Gray — 71.700 🇦🇪
🎧S24 Ultra 12/256 S928B Violet — 71.700 🇨🇱
🎧S24 Ultra 12/256 S928B Yellow — 78.900 🇨🇱
🎧S24 Ultra 12/512 S928B Black — 74.900 🇨🇱
🎧S24 Ultra 12/512 S928B Gray — 82.200 🇨🇱

🎧S25 Ultra 12/256 S938B Black — 82.000 🇦🇪*
🎧S25 Ultra 12/256 S938B Grey — 80.600 🇦🇪
🎧S25 Ultra 12/256 S938B Blue — 80.200 🇦🇪
🎧S25 Ultra 12/256 S938B White — 80.600 🇰🇿
🎧S25 Ultra 12/512 S938B Grey — 93.000 🇨🇱
🎧S25 Ultra 12/512 S938B Blue — 91.000 🇨🇱
🎧S25 Ultra 12/512 S938B White — 91.000 🇨🇱

🎧S25 Ultra 12/1Tb S938B Gray — 123.000 🇦🇪

🎧Z Fold6 12/256 F956B Navy — 115.000 🇦🇪
""",
    )


@bot.message_handler(func=lambda message: message.text == "Xiaomi/Redmi/Note")
def samsung_prices(message):
    bot.send_message(
        message.chat.id,
        """Цены на Xiaomi:
        
📱 Redmi / Note / Xiaomi

🎧Redmi A3X 3/64 Green — 10.300 🇷🇺
🎧Redmi 13 6/128 NFC Black — 14.900 🇷🇺
🎧Redmi 13 6/128 NFC Gold — 14.900 🇷🇺
🎧Redmi 13 8/256 NFC Black — 16.700 🇷🇺

🎧Redmi 14C 4/128 NFC Black — 13.200 🇷🇺
🎧Redmi 14C 4/128 NFC Blue — 13.000 🇷🇺
🎧Redmi 14C 4/128 NFC Green — 13.000 🇷🇺

🎧Note 13 Pro+ 5G 8/256 Purple — 32.000 🇪🇺
🎧Note 13 Pro+ 5G 12/512 Black — 33.800 🇪🇺
🎧Note 13 Pro+ 5G 12/512 Purple — 33.800 🇪🇺
🎧Note 13 Pro+ 5G 12/512 White — 33.800 🇪🇺

🎧Note 14 4G 6/128 NFC Black — 17.400 🇷🇺
🎧Note 14 4G 6/128 NFC Blue — 17.400 🇷🇺
🎧Note 14 4G 6/128 NFC Green — 17.400 🇷🇺
🎧Note 14 4G 8/128 NFC Blue — 18.400 🇷🇺
🎧Note 14 4G 8/128 NFC Green — 18.400 🇷🇺
🎧Note 14 4G 8/256 NFC Black — 20.000 🇪🇺
🎧Note 14 4G 8/256 NFC Blue — 20.000 🇪🇺
🎧Note 14 4G 8/256 NFC Green — 20.000 🇪🇺
🎧Note 14 4G 8/256 NFC Purple — 20.000 🇪🇺

🎧Note 14S 4G 8/256 NFC Blue — 22.600 🇪🇺
🎧Note 14S 4G 8/256 NFC Purple — 22.600 🇪🇺

🎧Note 14 Pro 4G 8/256 Black — 23.800 🇪🇺
🎧Note 14 Pro 4G 8/256 Blue — 23.800 🇪🇺
🎧Note 14 Pro 4G 8/256 Purple — 23.800 🇪🇺
🎧Note 14 Pro 4G 12/256 Black — 29.200 🇪🇺
🎧Note 14 Pro 4G 12/256 Blue — 29.200 🇪🇺
🎧Note 14 Pro 4G 12/512 Black — 30.400 🇪🇺
🎧Note 14 Pro 4G 12/512 Blue — 30.400 🇪🇺
🎧Note 14 Pro 4G 12/512 Purple — 30.400 🇪🇺

🎧Note 14 Pro 5G 8/256 Black — 29.900 🇪🇺
🎧Note 14 Pro 5G 8/256 Green — 29.900 🇪🇺
🎧Note 14 Pro 5G 8/256 Purple — 29.900 🇪🇺
🎧Note 14 Pro 5G 12/512 Black — 33.300 🇪🇺
🎧Note 14 Pro 5G 12/512 Green — 33.300 🇪🇺
🎧Note 14 Pro 5G 12/512 Purple — 33.300 🇪🇺

🎧Note 14 Pro+ 5G 8/256 Black — 34.600 🇪🇺
🎧Note 14 Pro+ 5G 8/256 Blue — 34.600 🇷🇺
🎧Note 14 Pro+ 5G 8/256 Purple — 34.600 🇪🇺
🎧Note 14 Pro+ 5G 12/512 Black — 38.300 🇪🇺
🎧Note 14 Pro+ 5G 12/512 Blue — 38.300 🇪🇺

🎧Xiaomi 12 5G 8/256 Blue — 31.200 🇪🇺
🎧Xiaomi 12 5G 8/256 Purple — 31.200 🇪🇺

🎧Xiaomi 13T Pro 5G 12/512 Black — 46.700 🇪🇺
🎧Xiaomi 13T Pro 5G 12/512 Green — 46.500 🇬🇧

🎧Xiaomi 14T 5G 12/256 Black — 40.300 🇪🇺
🎧Xiaomi 14T 5G 12/256 Blue — 40.300 🇪🇺
🎧Xiaomi 14T 5G 12/256 Green — 40.300 🇪🇺
🎧Xiaomi 14T 5G 12/256 Gray — 40.300 🇪🇺
🎧Xiaomi 14T 5G 12/512 Black — 41.700 🇪🇺

🎧Xiaomi 14T Pro 5G 12/512 Black — 52.600 🇪🇺
🎧Xiaomi 14T Pro 5G 12/512 Blue — 52.600 🇪🇺
🎧Xiaomi 14T Pro 5G 12/512 Gray — 52.600 🇪🇺
🎧Xiaomi 14T Pro 5G 12/1024 Black — 57.500 🇪🇺
🎧Xiaomi 14T Pro 5G 12/1024 Blue — 57.500 🇪🇺
🎧Xiaomi 14T Pro 5G 12/1024 Gray — 57.300 🇬🇧
🎧Xiaomi 14T Pro 5G 12/1024 Gray — 57.500 🇪🇺

🎧Xiaomi 15 5G 12/256 Black — 71.500 🇪🇺
🎧Xiaomi 15 5G 12/256 Green — 71.500 🇪🇺
🎧Xiaomi 15 5G 12/256 White — 71.500 🇪🇺
🎧Xiaomi 15 5G 12/512 Black — 75.400 🇪🇺
🎧Xiaomi 15 5G 12/512 Green — 75.400 🇪🇺
🎧Xiaomi 15 5G 12/512 White — 75.400 🇪🇺

🎧Xiaomi 15 Ultra 5G 16/512 Black — 108.500 🇬🇧
🎧Xiaomi 15 Ultra 5G 16/512 Black — 109.500 🇷🇺
🎧Xiaomi 15 Ultra 5G 16/512 Silver — 109.500 🇪🇺
🎧Xiaomi 15 Ultra 5G 16/512 White — 109.500 🇬🇧
🎧Xiaomi 15 Ultra 5G 16/512 White — 109.900 🇪🇺
""",
    )


@bot.message_handler(func=lambda message: message.text == "POCO")
def samsung_prices(message):
    bot.send_message(
        message.chat.id,
        """
        📱 Poco 
        
🎧Poco M5s 4G 8/256 Grey — 16.600 🇪🇺
🎧Poco M6 4G 6/128 Purple — 15.400 🇪🇺
🎧Poco M6 4G 8/256 Black — 17.400 🇪🇺
🎧Poco M6 Pro 4G 12/512 Black — 21.800 🇪🇺
🎧Poco M6 Pro 4G 12/512 Blue — 21.800 🇪🇺
🎧Poco M6 Pro 4G 12/512 Purple — 21.800 🇪🇺
🎧Poco M7 Pro 8/256 Green — 21.700 🇪🇺
🎧Poco M7 Pro 8/256 Silver — 21.700 🇪🇺
🎧Poco X6 Pro 5G 12/512 Grey — 31.500 🇪🇺
🎧Poco X6 Pro 5G 12/512 Yellow — 31.500 🇪🇺
🎧Poco X7 5G 8/256 Black — 24.800 🇪🇺
🎧Poco X7 5G 8/256 Green — 24.800 🇪🇺
🎧Poco X7 5G 8/256 Silver — 24.800 🇪🇺
🎧Poco X7 5G 12/512 Black — 30.300 🇪🇺
🎧Poco X7 5G 12/512 Green — 30.200 🇪🇺
🎧Poco X7 5G 12/512 Silver — 30.300 🇪🇺
🎧Poco X7 Pro 5G 8/256 Black — 32.300 🇪🇺
🎧Poco X7 Pro 5G 8/256 Green — 32.300 🇪🇺
🎧Poco X7 Pro 5G 8/256 Yellow — 32.300 🇪🇺
🎧Poco X7 Pro 5G 12/256 Black — 34.200 🇪🇺
🎧Poco X7 Pro 5G 12/256 Green — 34.000 🇪🇺
🎧Poco X7 Pro 5G 12/256 Yellow — 34.200 🇪🇺
🎧Poco X7 Pro 5G 12/512 Black — 36.100 🇪🇺
🎧Poco X7 Pro 5G 12/512 Green — 36.100 🇪🇺

🎧Poco F6 5G 8/256 Black — 31.600 🇪🇺
🎧Poco F6 5G 8/256 Green — 31.600 🇪🇺
🎧Poco F6 5G 8/256 Titanium — 31.600 🇪🇺
🎧Poco F6 5G 12/512 Black — 33.600 🇪🇺
🎧Poco F6 5G 12/512 Green — 33.600 🇪🇺
🎧Poco F6 5G 12/512 Titanium — 33.600 🇪🇺

🎧Poco F6 Pro 5G 12/512 Black — 43.000 🇪🇺
🎧Poco F6 Pro 5G 12/512 White — 43.000 🇪🇺
🎧Poco F6 Pro 5G 16/1024 Black — 46.000 🇬🇧

🎧Poco F7 Pro 5G 12/256 Black — 45.500 🇪🇺
🎧Poco F7 Pro 5G 12/256 Blue — 45.500 🇪🇺
🎧Poco F7 Pro 5G 12/256 Silver — 45.500 🇪🇺
🎧Poco F7 Pro 5G 12/512 Black — 47.500 🇪🇺

🎧Poco F7 Ultra 5G 12/256 Black — 62.000 🇪🇺
🎧Poco F7 Ultra 5G 12/256 Yellow — 62.000 🇪🇺
🎧Poco F7 Ultra 5G 16/512 Black — 65.000 🇪🇺
🎧Poco F7 Ultra 5G 16/512 Yellow — 65.300 🇪🇺
        """,
    )
@bot.message_handler(func=lambda message: message.text == "HUAWEI/HONOR")
def samsung_prices(message):
    bot.send_message(
        message.chat.id,
        """
📱 Honor

🎧Honor X7c 6/128 Black — 16.300 🇷🇺
🎧Honor X7c 6/128 Green — 16.300 🇷🇺
🎧Honor X7c 6/128 White — 16.300 🇷🇺

🎧Honor X8b 8/256 Black — 20.500 🇷🇺
🎧Honor X8b 8/256 Green — 20.500 🇷🇺
🎧Honor X8b 8/256 Silver — 20.500 🇷🇺

🎧Honor X8c 8/128 Black — 20.300 🇷🇺
🎧Honor X8c 8/128 Green — 20.300 🇷🇺
🎧Honor X8c 8/128 White — 20.300 🇷🇺

🎧Honor X9c 8/256 Blue — 32.000 🇷🇺
🎧Honor X9c 8/256 Violet — 32.000 🇷🇺
🎧Honor X9c 12/256 Black — 34.300 🇷🇺
🎧Honor X9c 12/256 Blue — 34.300 🇷🇺

🎧Honor 200 8/256 Black — 37.400 🇷🇺
🎧Honor 200 8/256 Green — 37.200 🇷🇺
🎧Honor 200 8/256 White — 37.200 🇷🇺
🎧Honor 200 12/512 Black — 41.500 🇷🇺
🎧Honor 200 12/512 Green — 41.500 🇷🇺
🎧Honor 200 12/512 White — 41.500 🇷🇺

🎧Honor 200 Pro 12/512 Black — 48.500 🇪🇺
🎧Honor 200 Pro 12/512 Ocean Cyan — 48.500 🇪🇺

🎧Honor Magic 7 12/256 Black — 72.500 🇷🇺
🎧Honor Magic 7 12/256 Grey — 72.500 🇷🇺
🎧Honor Magic 7 12/256 White — 72.500 🇷🇺

🎧Honor Magic 7 Pro 12/512 Black — 84.000 🇪🇺
🎧Honor Magic 7 Pro 12/512 Blue — 84.000 🇪🇺

📱 Huawei

🎧Huawei Mate 70 Pro 12/512 Black — 79.900 🇷🇺
🎧Huawei Mate 70 Pro 12/512 Green — 79.900 🇷🇺

🎧Huawei Pura 70 12/256 Black — 51.000 🇷🇺
🎧Huawei Pura 70 12/256 Pink — 51.000 🇷🇺
🎧Huawei Pura 70 12/256 White — 51.000 🇷🇺

🎧Huawei Pura 70 Pro 12/512 Black — 67.000 🇷🇺
🎧Huawei Pura 70 Pro 12/512 White — 67.000 🇷🇺*        
        """,
    )
@bot.message_handler(func=lambda message: message.text == "PIXEL/ONE PLUS")
def samsung_prices(message):
    bot.send_message(
        message.chat.id,
        """
 
🎧Pixel 7 8/128 Obsidian — 38.300 🇺🇸
🎧Pixel 7 8/128 Snow — 38.300 🇺🇸

🎧Pixel 7 8/256 Obsidian — 41.500 🇺🇸

🎧Pixel 7 Pro 12/128 Obsidian — 42.500 🇨🇦
🎧Pixel 7 Pro 12/128 Snow — 42.500 🇺🇸
🎧Pixel 7 Pro 12/128 Hazel — 42.500 🇺🇸

🎧Pixel 7 Pro 12/512 Obsidian — 48.500 🇺🇸

🎧Pixel 8 128 Obsidian — 53.500 🇬🇧

🎧Pixel 8 Pro 12/256Gb Obsidian — 67.500 🇬🇧
🎧Pixel 8 Pro 12/512Gb Obsidian — 92.500 🇬🇧

🎧Pixel 9 12/128 Wintergreen — 64.500 🇨🇦
🎧Pixel 9 12/128 Obsidian — 64.500 🇨🇦
🎧Pixel 9 12/128 Porcelain — 64.500 🇨🇦

🎧Pixel 9 Pro 16/512 Obsidian — 102.500 🇨🇦

🎧Pixel 9 Pro XL 16/256 Obsidian — 92.500 🇨🇦
🎧Pixel 9 Pro XL 16/256 Rose Quartz — 95.500 🇨🇦
🎧Pixel 9 Pro XL 16/256 Hazel — 93.500 🇨🇦
🎧Pixel 9 Pro XL 16/256 Porcelain — 93.500 🇨🇦

🎧Pixel 9 Pro XL 512 Porcelain — 105.500 🇯🇵
🎧Pixel 9 Pro XL 16/1 TB Obsidian — 120.000 🇨🇦



🎧OnePlus Pad Pro OPD2404 16/512 Gray — 55.000 🇨🇳
🎧OnePlus Pad Pro OPD2404 16/512 Green — 55.000 🇨🇳

🎧OnePlus 12 5G 16/512 Black — 71.500 🇺🇸 CPH2583
🎧OnePlus 13 5G 12/512 Black Eclipse — 73.500 🇨🇳 PJZ110 (Oxygen OS)
🎧OnePlus 13 5G 16/512 Arctic Dawn — 73.500 🇨🇳 PJZ110 (Oxygen OS)
🎧OnePlus 13 5G 16/512 Midnight Ocean — 73.500 🇨🇳 PJZ110 (Oxygen OS)
🎧OnePlus 13 5G 24/1024 Midnight Ocean — 80.500 🇨🇳 PJZ110 (Oxygen OS)

🎧OnePlus 13 16/512 Black Eclipse — 76.000 🇮🇳 CPH2649
🎧OnePlus 13 16/512 Arctic Dawn — 76.000 🇮🇳 CPH2649
🎧OnePlus 13R 5G 16/256 Astral Trail — 50.500 🇮🇳 CPH2691
🎧OnePlus 13R 5G 16/256 Nebula Noir — 48.000 🇮🇳 CPH2691
🎧OnePlus 13R 5G 16/512 Astral Trail — 52.000 🇮🇳 CPH2691
🎧OnePlus 13R 5G 16/512 Nebula Noir — 52.000 🇮🇳 CPH2691
🎧OnePlus Nord 4 5G 16/512 Mercurial Silver — 43.000 🇪🇺 CPH2663
🎧OnePlus Nord 4 5G 16/512 Obsidian Midnight — 43.000 🇪🇺 CPH2663
        """,
    )

# Обработка кнопки "Наушники"
@bot.message_handler(func=lambda message: message.text == "🎧 Наушники")
def headphones_prices(message):
    bot.send_message(
        message.chat.id,
        """Цены на наушники:
        
🎧AirPods (3rd Gen) with Lightning Case — 14.400 🇪🇺
🎧AirPods 4 (2024) — 14.900
🎧AirPods 4 (2024) с шумоподавлением — 18.800
🎧AirPods Pro 2 USB-C Case (2023) 🆕 — 20.900

Так же можно по отдельности ухо и кейс!


🆕 AirPods Max 2024 🆕

🎧AirPods Max Midnight — 49.900
🎧AirPods Max Starlight — 52.300
🎧AirPods Max Blue — 51.900
🎧AirPods Max Purple — 51.700
🎧AirPods Max Orange — 50.100

🎧 AirPods Max DEPPO

AirPods Pro 2 DEPPO — 8.500 (с шумоподавлением)
AirPods NEO DEPPO — 7.500
AirPods STEREO MAX DEPPO — 9.500

🎧 Marshall

Marshall Major 5 Black — 12.800 🇪🇺
Marshall Major 5 Brown — 13.800 🇪🇺
Marshall Major 5 Cream — 13.800 🇪🇺
Marshall Acton 3 Black — 34.500 🇪🇺
Marshall Acton 3 Cream — 34.500 🇪🇺
Marshall Acton 3 Brown — 34.500 🇪🇺
Marshall Stanmore 3 Black — 41.000 🇪🇺
Marshall Stanmore 3 Cream — 41.000 🇪🇺
Marshall Stanmore 3 Brown — 41.000 🇪🇺

🎶 Sony

Sony WH-1000XM5 Black — 31.500

🎧 Galaxy Buds

Galaxy Buds 3 Silver — 12.000 🇦🇪
Galaxy Buds 3 White — 12.000 🇦🇪
Galaxy Buds 3 Pro Silver — 15.700 🇦🇪
Galaxy Buds 3 Pro White — 15.700 🇰🇼

🎧 OnePlus Buds

OnePlus Buds 3 (E509A) Metallic Blue — 11.200 🇨🇳
OnePlus Buds Pro 2 (E507A) Black — 14.800 🇨🇳
OnePlus Buds Pro 2 (E507A) Green — 14.800 🇨🇳
OnePlus Buds Pro 3 (E512A) Lunar Radiance — 17.000 🇪🇺

🎧 Nothing Ear

Nothing Ear (a) B162 Black — 14.000

🎧 Redmi Buds

Redmi Buds 6 Pro Black — 12.200 🇷🇺
Redmi Buds 6 Pro Purple — 12.200 🇷🇺
Redmi Buds 6 Pro White — 12.200 🇷🇺

🎧 Pixel Buds
Pixel Buds Pro Coral — 17.000 🇺🇸
Pixel Buds Pro Porcelain — 17.000 🇺🇸""",
    )


@bot.message_handler(func=lambda message: message.text == "📱 Аксессуары")
def accessories_menu(message):
    buttons = ["🛡️ Защита экрана ",
               "🔌 Провода ",
               "⚡️ Зарядки",
               "🔙 Назад"
               ]
    chat_id = message.chat.id
    user_context[chat_id] = "accessory"
    markup = create_vertical_markup(buttons)
    bot.send_message(
        message.chat.id,
        "Выберите категорию аксессуаров:",
        reply_markup=markup
    )


@bot.message_handler(func=lambda message: message.text == "🛡️ Защита экрана")
def screen_protectors_prices(message):
    bot.send_message(
        message.chat.id,
        """Цены на защиту экрана:

- Стекло 0.33мм для любого  iPhone: 1000 ₽ 📱
- Стекло 0.4мм для любого  iPhone: 1500 ₽ 📱
- Органический пластик для Android: 600 ₽ 📱
""",
    )


@bot.message_handler(func=lambda message: message.text == "🔌 Провода")
def cables_prices(message):
    bot.send_message(
        message.chat.id,
        """Цены на провода:

Apple 

Apple Lightning OR 1м (в коробке) 1440
Apple Lightning OR 2м (в коробке) 1550
Apple Lightning Тайвань OR (в коробке) 1240
Apple USB - C / Lightning 1м Тайвань OR (в коробке) 1380
Apple USB - C / USB - C 1м OR (в коробке) 1580
Apple USB - C / USB - C 240W 2м OR (в коробке) 2030
Apple USB - C / USB - C 2м OR (в коробке) 1700
Apple USB - C / USB - C 60W 1м OR (в коробке) 1610
Apple USB‑C / Lightning 1м OR (в коробке) 1700
Apple USB‑C / Lightning 2м OR (в коробке) 1740

Samsung

Samsung USB‑C / USB - C OR (1м) Белый 1350
Samsung USB‑C / USB - C OR (1м) Черный 1420

Аналоги 

Apple Lightning Hi - Copy (в коробке) 630
Apple USB‑C / Lightning 1м Hi Copy (в коробке) 650
""",
    )


@bot.message_handler(func=lambda message: message.text == "⚡️ Зарядки")
def chargers_prices(message):
    bot.send_message(
        message.chat.id,
        """Цены на зарядки:

Apple

iPhone A1400 (5W) OR (в коробке) 1410
Apple USB‑C 20W OR 2160
Apple USB‑C 20W Taiwan OR 1790


Samsung

Samsung 25W USB-C (Белый) Service Pack 100% OR 1790
Samsung 25W USB-C (Черный) Service Pack 100% OR 1790
Samsung 45W USB - C (Белый) Service Pack 100% OR 2250
Samsung 45W USB - C (Черный) Service Pack 100% OR 2250

Аналоги

iPhone A1400 (5W) Копия (в коробке) 770
Apple USB‑C 20W Hi - Copy 1320
Samsung 25W USB - C (Белый) 980
Samsung 25W USB - C (Черный) 980
Samsung 45W USB - C (Белый) 1160
Samsung 45W USB - C (Черный)1160""",
    )


# Логика записи на ремонт
@bot.message_handler(func=lambda message: message.text == "📅 Запись на ремонт")
def booking(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    with sqlite3.connect(DB_PATH, check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        user = cursor.fetchone()
    if not user:
        msg = bot.send_message(chat_id, "Для продолжения нужно зарегистрироваться. Введите ваше имя:")
        bot.register_next_step_handler(msg, process_name_step)
    else:
        show_booking_menu(chat_id)


def process_name_step(message):
    chat_id = message.chat.id
    name = message.text
    msg = bot.send_message(chat_id, "Введите номер телефона по которому можно связаться:")
    bot.register_next_step_handler(msg, process_phone_step, name)


def process_phone_step(message, name):
    chat_id = message.chat.id
    phone = message.text
    user_id = message.from_user.id
    try:
        with sqlite3.connect(DB_PATH, check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (user_id, name, phone) VALUES (?, ?, ?)", (user_id, name, phone))
            conn.commit()
        bot.send_message(chat_id, "Регистрация завершена успешно!")
    except sqlite3.IntegrityError:
        bot.send_message(chat_id, "Вы уже зарегистрированы.")
    finally:
        show_booking_menu(chat_id)


def show_booking_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add(
        types.KeyboardButton("📝 Новая заявка"),
        types.KeyboardButton("📜 История обращений"),
        types.KeyboardButton("🔙 Назад")
    )
    bot.send_message(chat_id, "Выберите действие:", reply_markup=markup)


# Логика новой заявки
@bot.message_handler(func=lambda message: message.text == "📝 Новая заявка")
def new_request(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    with sqlite3.connect(DB_PATH, check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        if not cursor.fetchone():
            bot.send_message(chat_id, "Сначала выполните регистрацию.")
            return
    msg = bot.send_message(chat_id, "Укажите модель устройства:")
    bot.register_next_step_handler(msg, process_device_step)


def process_device_step(message):
    chat_id = message.chat.id
    device = message.text
    msg = bot.send_message(chat_id, "Опишите проблему:")
    bot.register_next_step_handler(msg, process_problem_step, device)


def process_problem_step(message, device):
    chat_id = message.chat.id
    problem = message.text
    msg = bot.send_message(chat_id, "Что вы уже пробовали предпринять?")
    bot.register_next_step_handler(msg, process_actions_step, device, problem)


from datetime import datetime

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def process_actions_step(message, device, problem):
    chat_id = message.chat.id
    actions_taken = message.text
    user_id = message.from_user.id

    from datetime import datetime

    # Создаем новый заказ
    with sqlite3.connect(DB_PATH, check_same_thread=False) as conn:
        cursor = conn.cursor()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Текущая дата и время
        cursor.execute(
            "INSERT INTO orders (user_id, device, problem, actions_taken, created_at) VALUES (?, ?, ?, ?, ?)",
            (user_id, device, problem, actions_taken, current_time)
        )
        order_id = cursor.lastrowid
        conn.commit()

        # Получаем данные пользователя
        cursor.execute("SELECT name, phone FROM users WHERE user_id=?", (user_id,))
        user_data = cursor.fetchone()
        if user_data:
            user_name, user_phone = user_data
        else:
            user_name, user_phone = "Неизвестно", "Не указан"

    # Формируем уведомление для мастера
    notification_message = (
        f"🔔 Новая заявка!\n"
        f"Номер заказа: #{order_id}\n"
        f"Устройство: {device}\n"
        f"Проблема: {problem}\n"
        f"Предпринятые действия: {actions_taken}\n"
        f"Контакты клиента:\n"
        f"  Имя: {user_name}\n"
        f"  Телефон: {user_phone}"
    )

    # Отправляем уведомление мастеру через chat_id или username
    with sqlite3.connect(DB_PATH, check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT chat_id FROM masters WHERE username='303058948'")
        master_chat_id = cursor.fetchone()

    if master_chat_id and master_chat_id[0]:
        try:
            bot.send_message(master_chat_id[0], notification_message)
            logging.info(f"Уведомление успешно отправлено мастеру с chat_id: {master_chat_id[0]}")
        except Exception as e:
            logging.error(f"Не удалось отправить уведомление мастеру через chat_id: {e}")
    else:
        try:
            bot.send_message("303058948", notification_message)
            logging.info("Уведомление успешно отправлено мастеру через username.")
        except Exception as e:
            logging.error(f"Не удалось отправить уведомление мастеру через username: {e}")
            logging.error("Chat ID мастера не найден.")

    # Отправляем подтверждение пользователю, создавшему заявку
    bot.send_message(chat_id, f"Ваша заявка успешно создана! Номер заказа: #{order_id}")
    show_booking_menu(chat_id)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    data = call.data.split(":")
    action, order_id = data[0], int(data[1])

    if action == "close_order":
        # Закрываем заказ
        with sqlite3.connect(DB_PATH, check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE orders SET status='closed' WHERE order_id=?", (order_id,))
            conn.commit()
        bot.answer_callback_query(call.id, "Заказ успешно закрыт.")
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"Заказ #{order_id} закрыт."
        )

    elif action == "reject_order":
        # Запрашиваем причину отказа
        msg = bot.send_message(call.message.chat.id, "Введите причину отказа:")
        bot.register_next_step_handler(msg, process_rejection_reason, order_id)


def process_rejection_reason(message, order_id):
    chat_id = message.chat.id
    reason = message.text

    # Обновляем заказ в базе данных
    with sqlite3.connect(DB_PATH, check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE orders SET status='rejected', diagnosis=? WHERE order_id=?", (reason, order_id))
        conn.commit()

    # Уведомляем мастера
    bot.send_message(chat_id, f"Заказ #{order_id} отклонен. Причина: {reason}")


@bot.message_handler(func=lambda message: message.text == "📜 История обращений")
def history(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    # Получаем историю заказов пользователя
    with sqlite3.connect(DB_PATH, check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT order_id, device, problem, status, guarantee, created_at 
            FROM orders 
            WHERE user_id=? 
            ORDER BY order_id DESC
        """, (user_id,))
        orders = cursor.fetchall()
    if not orders:
        bot.send_message(chat_id, "У вас нет истории обращений.")
    else:
        response = "История ваших обращений:\n"
        for order in orders:
            order_id, device, problem, status, guarantee, created_at = order
            response += (
                f"Заказ #{order_id}\n"
                f"  Устройство: {device}\n"
                f"  Проблема: {problem}\n"
                f"  Статус: {status}\n"
                f"  Гарантия: {guarantee or 'Не указано'}\n"
                f"  Дата обращения: {created_at or 'Не указана'}\n\n"
            )
        bot.send_message(chat_id, response)


@bot.message_handler(commands=['start'])
@safe_handler(bot)
def start(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username

    # Проверяем, является ли пользователь мастером
    with sqlite3.connect(DB_PATH, check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM masters WHERE username=?", (username,))
        master = cursor.fetchone()

        if master:
            # Обновляем chat_id мастера
            cursor.execute("UPDATE masters SET chat_id=? WHERE username=?", (chat_id, username))
            conn.commit()
            logging.info(f"Chat ID мастера {username} успешно обновлен: {chat_id}")

    bot.send_message(
        chat_id,
        """Vas1lSKY Repair — это место, где ваш смартфон получает [новую жизнь](https://t.me/vas1lsky_shiza/231).

Ваши заботы — моя работа!

- 🚀 Быстрое восстановление.
- 💰 Прозрачные сроки и цены.
- 👨‍💻 Индивидуальный подход к каждому клиенту.

Доверьте мне свой смартфон, и я верну его в рабочее состояние!""",
        reply_markup=create_main_menu_markup(),
        parse_mode='Markdown'
    )


# Обработка кнопки "Назад"
@bot.message_handler(func=lambda message: message.text == "🔙 Назад")
def back_to_previous_menu(message):
    chat_id = message.chat.id

    if chat_id in user_context:
        current_state = user_context[chat_id]

        if current_state == "sell_technology":
            del user_context[chat_id]  # Очищаем контекст
            bot.send_message(chat_id, "Выберите опцию:", reply_markup=create_main_menu_markup())
        elif current_state == "apple_technology":
            user_context[chat_id] = "sell_technology"  # Обновляем контекст
            sell_technology(message)
        elif current_state == "android":
            user_context[chat_id] = "sell_technology"  # Обновляем контекст
            sell_technology(message)
        elif current_state == "accessory":
            user_context[chat_id] = "sell_technology"  # Обновляем контекст
            sell_technology(message)
        elif current_state == "android_technology":
            user_context[chat_id] = "sell_technology"  # Обновляем контекст
            sell_technology(message)
        elif current_state == "headphones_prices":
            user_context[chat_id] = "sell_technology"  # Обновляем контекст
            sell_technology(message)
        elif current_state == "chargers_cables":
            user_context[chat_id] = "sell_technology"  # Обновляем контекст
            sell_technology(message)
        else:
            del user_context[chat_id]
            bot.send_message(chat_id, "Выберите опцию:", reply_markup=create_main_menu_markup())
    else:
        bot.send_message(chat_id, "Выберите опцию:", reply_markup=create_main_menu_markup())


# Обработка команды /orders (скрытая кнопка для мастеров)
@bot.message_handler(commands=['orders'])
def master_orders(message):
    chat_id = message.chat.id
    username = message.from_user.username  # Получаем username пользователя

    # Проверяем, является ли пользователь @Vas1lSKY
    if username == "303058948Y":
        # Показываем список открытых заказов без авторизации
        with sqlite3.connect(DB_PATH, check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT order_id, user_id, device, problem FROM orders WHERE status='new'")
            orders = cursor.fetchall()

        if not orders:
            bot.send_message(chat_id, "Нет открытых заказов.")
        else:
            response = "Открытые заказы:\n"
            for order in orders:
                order_id, user_id, device, problem = order
                response += (
                    f"#{order_id} - Клиент ID: {user_id}\n"
                    f"    Устройство: {device}\n"
                    f"    Проблема: {problem}\n\n"
                )
            bot.send_message(chat_id, response, reply_markup=create_orders_menu_markup(orders))
    else:
        # Для других пользователей требуется авторизация
        msg = bot.send_message(chat_id, "Введите логин:")
        bot.register_next_step_handler(msg, process_master_login)


def process_master_login(message):
    chat_id = message.chat.id
    username = message.text
    msg = bot.send_message(chat_id, "Введите пароль:")
    bot.register_next_step_handler(msg, process_master_password, username)


def process_master_password(message, username):
    chat_id = message.chat.id
    password = message.text

    # Проверяем логин и пароль
    with sqlite3.connect(DB_PATH, check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM masters WHERE username=? AND password=?", (username, password))
        if not cursor.fetchone():
            bot.send_message(chat_id, "Неверный логин или пароль.")
            return

    # Показываем список открытых заказов
    with sqlite3.connect(DB_PATH, check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT order_id, user_id, device, problem FROM orders WHERE status='new'")
        orders = cursor.fetchall()

    if not orders:
        bot.send_message(chat_id, "Нет открытых заказов.")
    else:
        response = "Открытые заказы:\n"
        for order in orders:
            order_id, user_id, device, problem = order
            # Формируем каждый заказ с новой строки для каждой детали
            response += (
                f"#{order_id} - Клиент ID: {user_id}\n"
                f"       Устройство: {device}\n"
                f"       Проблема: {problem}\n\n"
            )
        bot.send_message(chat_id, response, reply_markup=create_orders_menu_markup(orders))


def create_orders_menu_markup(orders):
    """Создает клавиатуру с номерами заказов."""
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for order in orders:
        markup.add(types.KeyboardButton(f"#{order[0]}"))
    markup.add(types.KeyboardButton("🔙 Назад"))
    return markup


# Обработка выбора заказа мастером
@bot.message_handler(func=lambda message: message.text.startswith("#"))
def process_order(message):
    chat_id = message.chat.id
    order_id = int(message.text[1:])  # Извлекаем ID заказа из текста

    # Проверяем, существует ли заказ
    with sqlite3.connect(DB_PATH, check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE order_id=?", (order_id,))
        order = cursor.fetchone()

    if not order:
        bot.send_message(chat_id, "Заказ не найден.")
        return

    # Открываем форму для мастера
    msg = bot.send_message(chat_id, "В каком состоянии принят телефон? (опишите)")
    bot.register_next_step_handler(msg, process_condition_step, order_id)


def process_condition_step(message, order_id):
    chat_id = message.chat.id
    condition = message.text
    msg = bot.send_message(chat_id, "Результат диагностики:")
    bot.register_next_step_handler(msg, process_diagnosis_step, order_id, condition)


def process_diagnosis_step(message, order_id, condition):
    chat_id = message.chat.id
    diagnosis = message.text
    msg = bot.send_message(chat_id, "Что было сделано с устройством?")
    bot.register_next_step_handler(msg, process_work_done_step, order_id, condition, diagnosis)


def process_work_done_step(message, order_id, condition, diagnosis):
    chat_id = message.chat.id
    work_done = message.text
    msg = bot.send_message(chat_id, "Гарантия (опишите):")
    bot.register_next_step_handler(msg, process_guarantee_step, order_id, condition, diagnosis, work_done)


def process_guarantee_step(message, order_id, condition, diagnosis, work_done):
    chat_id = message.chat.id
    guarantee = message.text
    # Обновляем заказ
    with sqlite3.connect(DB_PATH, check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE orders 
            SET status='Выдан', condition=?, diagnosis=?, work_done=?, guarantee=?
            WHERE order_id=?
        """, (condition, diagnosis, work_done, guarantee, order_id))
        conn.commit()
    bot.send_message(chat_id, f"Заказ #{order_id} успешно выдан клиенту.")




def create_back_and_contact_markup():
    """
    Создает клавиатуру с кнопками 'Назад' и 'Связь со мной'.
    Используется для возврата к предыдущему меню или связи с мастером.
    """
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_back = types.KeyboardButton("🔙 Назад")
    button_contact = types.KeyboardButton("📞 Связь со мной")
    markup.add(button_back, button_contact)
    return markup

@bot.message_handler(func=lambda message: message.text == "🛡Топ VPN №1")
def tic_tac_toe_start(message):
    bot.send_message(
        message.chat.id,
        """Сам пользуюсь Sota VPN и вам рекомендую 
        
        t.me/sotavpnbot?start=303058948
        
буду благодарен если подключите по моей рефералочке )""",
    )
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    """Функция для обработки нажатий на кнопки"""
    if message.text == "🛠️ Ремонт":
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        button_consultation = types.KeyboardButton("💬 Онлайн консультация")
        button_typical_issues = types.KeyboardButton("🔧 Типичные поломки")
        button_back = types.KeyboardButton("🔙 Назад")
        markup.add(button_consultation, button_typical_issues, button_back)
        bot.send_message(
            message.chat.id,
            """
[Прайс](https://docs.google.com/spreadsheets/d/19Cf7Lq0v87tlYAN-m1o0Jcbrpn4iV6Or/edit?usp=sharing&ouid=104291932038055353547&rtpof=true&sd=true) для ориентира

Как рассчитать САМОМУ стоимость ремонта устройства:

1. Определение цены устройства:

-Перейдите на [Яндекс Маркет](https://market.yandex.ru/).
-Введите модель вашего устройства.
-Запишите цену из первой строки результатов. 📊

2. Заказ запчастей:

-Определите необходимые запчасти для ремонта.
-Закупите запчасти у [MOBA](https://moba.ru/catalog/?q=&s=%D0%9F%D0%BE%D0%B8%D1%81%D0%BA) или [MASTER MOBILE](https://master-mobile.ru/catalog/?q=), или у других поставщиков, если это необходимо. 🛍️

3. Доставка запчастей:

-Используйте сервис Dostavista.ru для заказа курьера.
-Учтите стоимость доставки будет добавлена к итоговой цене. 🚚

Дополнительные условия:

-Цена указана без стоимости запчастей, только за услугу. 💰

-Если устройство пострадало от воды, чистка будет оплачена в любом случае, даже если не даст результата. 💧

-КОМПЛЕКСНЫЙ РЕМОНТ = ОСНОВНОЙ РЕМОНТ + 1000р + зап часть 

-При ремонте дисплейного модуля защитное стекло предоставляется в подарок. 🎁

Итоговая стоимость:

-Сложите стоимость услуги, стоимость запчастей и стоимость доставки. 🧮

-Если применимы скидки, вычтите их из общей суммы. 💲

-Таким образом, вы получите полную стоимость ремонта вашего устройства. 🎯

Если у вас есть вопросы, пожалуйста, используйте Онлайн консультацию. 📞""",
            reply_markup=markup,
            parse_mode='Markdown'
        )

    elif message.text == "💬 Онлайн консультация":
        bot.send_message(
            message.chat.id,
            """Свяжитесь с @Vas1lSKY для обсуждения деталей.

            В одно сообщение напишите:

-Устройство: укажите модель.
-Что случилось: опишите проблему.
-Что пробовали предпринять: укажите действия, которые были сделаны.

Буду благодарен за обратную связь и готов помочь разобраться с возникшими трудностями. 

Жду вашего ответа, чтобы мы могли оперативно найти оптимальное решение.
            """
        )
    elif message.text == "🔧 Типичные поломки":
        bot.send_message(
            message.chat.id,
            """Типичные проблемы:
🖥 Не работает дисплей.
🔋 Быстро разряжается батарея.
⚡️ Не заряжается устройство.
📱 Разбит корпус или стекло.
🔘 Не работают кнопки.
📸 Не работает камера.
🔊 Плохо слышно.
⚙️ Проблемы с внутренними компонентами.
💻 Проблемы с программным обеспечением.
🔧 Пайка микросхем.
🔑 Забыт пароль.
💧 Устройство попало в воду."""
        )
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        buttons = [
            "🖥 Не работает дисплей",
            "🔋 Быстро разряжается батарея",
            "⚡️ Не заряжается устройство",
            "📱 Разбит корпус или стекло",
            "🔘 Не работают кнопки",
            "📸 Не работает камера",
            "📢 Плохо слышно",
            "⚙️ Проблемы с внутренними компонентами",
            "💻 Проблемы с программным обеспечением",
            "🔧 Пайка микросхем",
            "🔑 Забыт пароль",
            "💧 Устройство попало в воду"
        ]
        for button_text in buttons:
            markup.add(types.KeyboardButton(button_text))

        button_back = types.KeyboardButton("🔙 Назад")

        markup.add(button_back)

        bot.send_message(

            message.chat.id,

            "Выберите одну из типичных проблем:",

            reply_markup=markup

        )


    elif message.text == "🖥 Не работает дисплей":

        bot.send_message(

            message.chat.id,

            """Проблема: Не работает дисплей 🖥️❌

Возможные причины:

- [Повреждение](https://t.me/vas1lsky_shiza/476) или износ экрана.

- Проблемы с [матрицей](https://t.me/vas1lsky_shiza/268?single) или [шлейфами](https://t.me/vas1lsky_shiza/518).

- Программные ошибки или сбои в системе.""",
            parse_mode='Markdown'

        )

    elif message.text == "🔋 Быстро разряжается батарея":

        bot.send_message(

            message.chat.id,

            """Проблема: Быстро разряжается батарея 🔋⚡

Возможные причины:

- [Старение](https://t.me/vas1lsky_shiza/299) и [износ](https://t.me/vas1lsky_shiza/232?single) аккумулятора.

- Программные сбои или ошибки в операционной системе.

- Нарушение работы датчиков питания.""",

            parse_mode='Markdown'

        )

    elif message.text == "⚡️ Не заряжается устройство":

        bot.send_message(

            message.chat.id,

            """Проблема: Не заряжается устройство 🔌❌

Возможные причины:

- Повреждение или износ разъема зарядки.

- [Отстегнулся шлейф](https://t.me/vas1lsky_shiza/450).

- Проблемы с внутренней платой (например, микросхема питания).

- Нарушение работы контроллера зарядки.

- Повреждение кабеля или адаптера питания.""",

            parse_mode='Markdown'

        )

    elif message.text == "📱 Разбит корпус или стекло":

        bot.send_message(

            message.chat.id,

            """Проблема: Разбит корпус или стекло 📱💥

Возможные причины:

- Падение устройства или [удар](https://t.me/vas1lsky_shiza/224).

- Износ материала корпуса.

- Проблемы с герметичностью корпуса.

[Замена крышки на iPhone](https://t.me/vas1lsky_shiza/522)

Мы предлагаем полный разбор устройства для восстановления корпуса. Этот метод является наиболее адекватным среди нескольких возможных вариантов.

### Процедура Восстановления Корпуса:
- **Полный Разбор Устройства**:
 Мы будем восстанавливать корпус с использованием колхозного метода.
  Минусы данной процедуры включают:
  - Телефон становится хрупким, так как он больше не в первоначальном виде.
  - Потеря заводской герметичности.

- **Замена Корпуса с Донора**: 
  - Самый идеальный вариант — замена корпуса снятого с нового устройства (донора).

- **Замена Стекла**:
  - Для замены стекла телефон нагревается до 240 градусов.
  - Полный разбор необходим для предотвращения повреждений платы, камер и микрофонов.
  - Без разбора есть риск попадания осколков внутрь телефона или на линзы камер, что может потребовать дополнительного ремонта.
  - Основной риск — осколок может проткнуть аккумулятор, вызывая пожар.
  - После зачистки стекла телефон полностью очищается от осколков.
  - Устанавливается новая крышка (оргстекло или каленое стекло). Я использую второй вариант, так как разница в цене минимальна, а качество значительно лучше.
  - Для успешного ремонта важно, чтобы геометрия корпуса не была нарушена, иначе крышка ляжет неравномерно.
  - Если есть сильные внешние повреждения, необходимо уточнять отдельно!

### Проверка перед Ремонтом:
Перед началом ремонта обязательно проверяем все функции устройства:
- **Мобильная связь**: Набираем 112 для проверки динамика, громкой связи, датчиков приближения и автояркости.
- **Wi-Fi**: Проверяем работоспособность.
- **Bluetooth**: Проверяем соединение.
- **Face ID**: Убедимся в его корректной работе.
- **Трутон**: Проверяем работу модуля.
- **Камеры**: Проверяем все камеры на всех режимах работы, включая вспышку.
- **Микрофоны**: Записываем видео на основную и фронтальную камеры, проверяем запись голоса на диктофон.
- **Сенсор**: Проверяем работоспособность.
- **Зарядка**: Проверяем обычную зарядку (5В), быструю зарядку (20В) и беспроводную.
- **NFC**: Хотя в РФ он не работает, проверяем его работоспособность.

### Проверка после Ремонта:
После завершения ремонта также тщательно проверяем все функции устройства и выдаём готовый аппарат.

### Гарантия:
- **Гарантия 6 месяцев на проверку** всех функций устройства после ремонта.

Для качественного и надёжного ремонта доверьте ваш смартфон нам! 🛠️📱
""",

            parse_mode='Markdown'

        )

    elif message.text == "🔘 Не работают кнопки":

        bot.send_message(

            message.chat.id,

            """Проблема: Не работают кнопки 🔘❌

Возможные причины:

- [Грязь](https://t.me/vas1lsky_shiza/495)

- Износ механической части кнопок.

- Повреждение контактов кнопок внутри устройства.

- Программные сбои.""",

            parse_mode='Markdown'

        )

    elif message.text == "📸 Не работает камера":

        bot.send_message(

            message.chat.id,

            """Проблема: Не работает камера 📸❌

Возможные причины:

- Повреждение линзы камеры.

- Проблемы с внутренними компонентами камеры.

- Программные сбои или ошибки.""",


        )

    elif message.text == "📢 Плохо слышно":

        bot.send_message(

            message.chat.id,

            """Проблема: Плохо слышно 🔊❌

Возможные причины:

- Загрязнение или повреждение динамика.

- Проблемы с программным обеспечением (настройки громкости или системные ошибки).""",


        )

    elif message.text == "⚙️ Проблемы с внутренними компонентами":

        bot.send_message(

            message.chat.id,

            """Проблема: Проблемы с внутренними компонентами ⚙️🔍

Возможные причины:

- Повреждение внутренних компонентов.

- Коррозия после попадания влаги.

- Программные сбои или ошибки.""",


        )

    elif message.text == "💻 Проблемы с программным обеспечением":

        bot.send_message(

            message.chat.id,

            """Проблема: Проблемы с программным обеспечением 💻❌

Возможные причины:

- Устаревшая прошивка.

- [Программные ошибки или сбои](https://t.me/vas1lsky_shiza/431).

- Вирусное или вредоносное ПО.""",

            parse_mode='Markdown'

        )

    elif message.text == "🔧 Пайка микросхем":

        bot.send_message(

            message.chat.id,

            """Проблема: Пайка микросхем 🔧💡

Возможные причины:

- Повреждение микросхем или проводников.

- Проблемы с контактами.

- Воздействие влаги или перегрев.""",


        )

    elif message.text == "🔑 Забыт пароль":

        bot.send_message(

            message.chat.id,

            """Проблема: Забыт пароль 🔑🔒

Возможные причины:

- Забытые учетные данные.

- Проблемы с блокировкой устройства.

- Программные сбои или ошибки.""",


        )

    elif message.text == "💧 Устройство попало в воду":

        bot.send_message(

            message.chat.id,

            """Проблема: Устройство попало в воду 💧💦

Возможные причины:

- [Прямой контакт с водой.](https://t.me/vas1lsky_shiza/138)

- Воздействие влаги.

- Коррозия внутренних компонентов.""",

            parse_mode='Markdown'

        )
    elif message.text == "🛡️ Гарантия":
        bot.send_message(
            message.chat.id,
            """🛡️ Наша гарантия на ремонт:

• 12 месяцев на ремонт iPhone и iPad
• 6 месяца на ремонт Android и других устройств

✅ Гарантия распространяется только на выполненные работы и установленные запчасти.

❌ Гарантия не распространяется:
• При наличии механических повреждений
• При  залитии устройства
• При самостоятельном вмешательстве

""",
        )

    elif message.text == "💰 Заработай":
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_contact = types.KeyboardButton("📞 Связь со мной")
        button_back = types.KeyboardButton("🔙 Назад")
        markup.add(button_contact, button_back)
        bot.send_message(
            message.chat.id,
            """Стань частью Vas1lSKY Repair и начни получать пассивный доход уже сегодня! 💰✨

💰 Заработай с нами!

Мы предлагаем партнерскую программу для всех желающих:

1️⃣ Приводите к нам клиентов на ремонт
2️⃣ Получайте до 20% от стоимости ремонта

🔍 Как это работает?
• Рассказывайте друзьям и знакомым о нашем сервисе
• Присылайте к нам клиентов с вашей рекомендацией
• При оформлении заказа клиент указывает ваш номер телефона
• Мы фиксируем ваше участие и начисляем вознаграждение

💸 Выплаты:
• Производятся после завершения ремонта и полной оплаты клиентом
• Возможны переводы на карту или мобильный телефон

Просто свяжись со мной и узнай больше о деталях партнерской программы. 📞✉️.""",
            reply_markup=markup
        )
    elif message.text == "📞 Связь со мной":
        bot.send_message(
            message.chat.id,
            "Свяжитесь с @Vas1lSKY для обсуждения деталей."
        )
    elif message.text == "⚙️ Как работаем":
        bot.send_message(
            message.chat.id,
            """⚙️ Как мы работаем:

1️⃣ Диагностика
• Бесплатная при согласии на ремонт
• 400-1000 ₽ если ремонт не требуется
• Занимает от 15 минут до 2 часов

2️⃣ Ремонт [Прайс для ориентира](https://docs.google.com/spreadsheets/d/19Cf7Lq0v87tlYAN-m1o0Jcbrpn4iV6Or/edit?usp=sharing&ouid=104291932038055353547&rtpof=true&sd=true) 
• Выполняется только после вашего согласия с ценой 
• Срок ремонта от 1 часа до 3 дней в зависимости от сложности
• Используем только качественные запчасти или аналоги премиум класса

3️⃣ Гарантия
• Предоставляем гарантию до 12 месяцев

4️⃣ Оплата
• Наличные
• Перевод СБП

🕒 График работы:
Ежедневно с 10:00 до 20:00

📍 Адрес:
г. Москва, ул. Зеленодольская, д. 16""",
            parse_mode='Markdown'
        )
    elif message.text == "📞 Связь":
        bot.send_message(
            message.chat.id,
            "✉️Контактная информация ✉️:\n📲Телеграм: @Vas1lSKY\n🎥YouTube: [Momsengineer](https://www.youtube.com/@Momsengineer)\n📢Канал: [vas1lsky_shiza](https://t.me/vas1lsky_shiza)",
            parse_mode='Markdown'
        )


# Игровое состояние
game_state = {}


# Функция для создания игрового поля с кнопками 3x3
def create_game_board_markup(board):
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    buttons = []
    for i in range(9):
        if board[i] == ' ':
            buttons.append(types.KeyboardButton(f"{i + 1}"))
        elif board[i] == 'X':
            buttons.append(types.KeyboardButton("❌"))  # Используем смайлик для крестика
        else:
            buttons.append(types.KeyboardButton("⭕"))  # Используем смайлик для нолика
    for i in range(0, 9, 3):
        markup.row(buttons[i], buttons[i + 1], buttons[i + 2])
    markup.add(types.KeyboardButton("🔄 Начать заново"), types.KeyboardButton("🔙 Назад"))
    return markup


# Проверка победы
def check_winner(board, player):
    win_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for combo in win_combinations:
        if all(board[i] == player for i in combo):
            return True
    return False


# Проверка ничьи
def is_draw(board):
    return ' ' not in board


# Ход бота
def bot_move(board, player):
    empty_cells = [i for i, cell in enumerate(board) if cell == ' ']
    if empty_cells:
        move = random.choice(empty_cells)
        board[move] = player
        return move
    return None


# Вывод текущего состояния игрового поля с использованием смайликов
def print_board(board):
    board_with_symbols = ['❌' if cell == 'X' else '⭕' if cell == 'O' else '🔲' for cell in board]
    return f"""
{board_with_symbols[0]} | {board_with_symbols[1]} | {board_with_symbols[2]}
{board_with_symbols[3]} | {board_with_symbols[4]} | {board_with_symbols[5]}
{board_with_symbols[6]} | {board_with_symbols[7]} | {board_with_symbols[8]}
"""


# Запуск бота
if __name__ == "__main__":
    print("Я сказала стартуем...")
    while True:
        try:
            bot.polling(none_stop=True, timeout=60, skip_pending=True)
        except Exception as e:
            logging.error(f"Ошибка в работе бота: {e}")
            print(f"Перезапуск бота через 5 секунд...")
            time.sleep(5)
