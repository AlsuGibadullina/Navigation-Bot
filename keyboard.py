from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


def create_keyboard_start(headings):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for header in headings:
        button = KeyboardButton(header.get_name())
        keyboard.add(button)
    return keyboard


def create_keyboard(headings):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for header in headings:
        button = KeyboardButton(header.get_name())
        keyboard.add(button)
    back = KeyboardButton('Назад')
    home = KeyboardButton('На главную')
    keyboard.row(back, home)
    return keyboard
