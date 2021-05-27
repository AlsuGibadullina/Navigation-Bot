from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

button_tables = KeyboardButton('Таблицы')
button_docs = KeyboardButton('Документы')
button_forms = KeyboardButton('Гугл Формы')

start_kb = ReplyKeyboardMarkup().add(button_tables).add(button_docs).add(button_forms)