from telebot import types

def create_vertical_markup(buttons):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for btn_text in buttons:
        markup.add(types.KeyboardButton(btn_text))
    return markup

import logging
from functools import wraps
from telebot import TeleBot

def safe_handler(bot: TeleBot):
    def decorator(func):
        @wraps(func)
        def wrapper(message, *args, **kwargs):
            try:
                return func(message, *args, **kwargs)
            except Exception as e:
                error_msg = f"Ошибка в {func.__name__}: {str(e)}"
                logging.error(error_msg, exc_info=True)
                bot.reply_to(message, "Произошла ошибка. Попробуйте позже или свяжитесь с поддержкой.")
        return wrapper
    return decorator
