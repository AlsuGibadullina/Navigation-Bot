from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import keyboard as kb
from config import TOKEN
from parsing.parser import get_headings

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    headers = get_headings()
    keyboard = kb.create_keyboard(headers)
    await message.reply("Что вас интересует?", reply_markup=keyboard)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply(
        "Список команд: \n/start - старт работы \n /help - помощь")


# TODO Если возможно, по этой команде останавливать работу бота
@dp.message_handler(commands=['exit'])
async def process_exit_command(message: types.Message):
    await message.reply("Спасибо за обращение!")


# TODO При получении сообщения бот должен проверять, есть ли в текущем массиве подзаголовков заголовок с таким названием
# TODO Если есть, проникнуть в него, создать клавиатуру и вывести кнопки
# TODO Если в этом заголовке есть ссылка, вывести её в чат
@dp.message_handler()
async def enter_subdirectory(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)


if __name__ == '__main__':
    executor.start_polling(dp)
