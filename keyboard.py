from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


def create_keyboard(headings):
    keyboard = ReplyKeyboardMarkup()
    for header in headings:
        button = KeyboardButton(header.get_name())
        keyboard.add(button)
    return keyboard
