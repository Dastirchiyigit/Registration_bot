from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text='11'),
            KeyboardButton(text='222'),
        ],
    ],
    resize_keyboard=True
)
