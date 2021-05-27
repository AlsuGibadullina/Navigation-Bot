from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import keyboard as kb

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Что вас интересует?", reply_markup=kb.start_kb)


@dp.message_handler(commands=['theme'])
async def process_example_command(message: types.Message):
    await message.reply("Список подпунктов ")

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Список команд: \n /theme  /start - старт работы \n /exit - завершение работы\n /help - помощь ")


@dp.message_handler(commands=['exit'])
async def process_exit_command(message: types.Message):
    await message.reply("Спасибо за обращение!")


@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)


if __name__ == '__main__':
    executor.start_polling(dp)
