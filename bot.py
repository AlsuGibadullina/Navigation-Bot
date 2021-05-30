from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nЭто бот для навигации по интсрументам наставничества")


@dp.message_handler(commands=['kaef'])
async def process_start_command(message: types.Message):
    await message.reply("Кааааййййффффф")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Список команд: \n /start - старт работы \n /exit - завершение работы\n /help - помощь ")


@dp.message_handler(commands=['exit'])
async def process_exit_command(message: types.Message):
    await message.reply("Спасибо за обращение!")


@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)


if __name__ == '__main__':
    executor.start_polling(dp)
