from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import keyboard as kb
from config import TOKEN
from parsing.parser import get_headings

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
# Очередь открытых страниц (массивов заголовков)
pages_queue = []


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    headers = get_headings()
    pages_queue.clear()
    pages_queue.append(headers)
    keyboard = kb.create_keyboard(headers)
    await message.reply("Что вас интересует?", reply_markup=keyboard)


# TODO Если возможно, по этой команде останавливать работу бота
@dp.message_handler(commands=['stop'])
async def process_exit_command(message: types.Message):
    await message.reply("Спасибо за обращение!")


@dp.message_handler()
async def process_home_command(msg: types.Message):
    if msg.text == 'На главную':
        kb.ReplyKeyboardRemove()
        await process_start_command(msg)


@dp.message_handler()
async def process_back_command(msg: types.Message):
    if msg.text == 'Назад':
        kb.ReplyKeyboardRemove()
        pages_queue.pop()
        await enter_subdirectory(msg)


# TODO При получении сообщения бот должен проверять, есть ли в текущем массиве подзаголовков заголовок с таким названием
# TODO Если есть, проникнуть в него, создать клавиатуру и вывести кнопки
# TODO Если в этом заголовке есть ссылка, вывести её в чат
@dp.message_handler()
async def enter_subdirectory(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)


if __name__ == '__main__':
    executor.start_polling(dp)
