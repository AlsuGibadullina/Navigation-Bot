from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from typing import List

import keyboard as kb
from config import TOKEN
from parsing.header import Header
from parsing.parser import get_headings

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
# Очередь открытых страниц (массивов заголовков)
stack_store = [Header()]
action_list = [Header()]


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    headers = get_headings()
    stack_store.extend(headers)
    keyboard = kb.create_keyboard(headers)
    await message.reply("Что вас интересует?", reply_markup=keyboard)


@dp.message_handler()
async def message_manager(message: types.Message):
    if action_list.__sizeof__() != 0:
        await original_button_manager(action_list.pop(), message)
    for head in stack_store:
        if head.get_name() == message.text:
            action_list.append(head)
            await generate_button(head, message)


async def generate_button(header, message: types.Message):
    subheaders = header.subheaders
    if subheaders.__sizeof__() != 0:
        stack_store.clear()
        stack_store.extend(subheaders)
        keyboard = kb.create_keyboard(subheaders)
        await message.reply("Выберите из перечня нужный раздел", reply_markup=keyboard)


async def original_button_manager(header: Header, message: types.Message):
    if message.text == kb.home.text:
        stack_store.clear()
        action_list.clear()
        stack_store.extend(get_headings())
    if message.text == kb.back.text:
        h = action_list.pop()
        stack_store.clear()
        stack_store.append(h.subheaders)
        action_list.append(h)
    if message.text == kb.links.text:
        action_list.append(header)
        await bot.send_message(message.from_user.id,
                               "Ссылки, содержащиеся в %s:\n %s" % (header.get_name(), header.links))


# TODO Если возможно, по этой команде останавливать работу бота
@dp.message_handler(commands=['stop'])
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
