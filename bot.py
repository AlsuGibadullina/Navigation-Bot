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
    stack_store.clear()
    action_list.clear()
    headers = get_headings()
    stack_store.extend(headers)
    keyboard = kb.create_keyboard(headers)
    await message.reply("Что вас интересует?", reply_markup=keyboard)


@dp.message_handler()
async def message_manager(message: types.Message):
    await original_button_manager(message)
    for head in stack_store:
        if head.get_name() == message.text:
            await generate_button(head, message)


async def generate_button(header, message: types.Message):
    subheaders = header.subheaders
    if len(subheaders) != 0:
        action_list.append(header)
        stack_store.clear()
        stack_store.extend(subheaders)
        keyboard = kb.create_keyboard(subheaders)
        await message.reply("Выберите из перечня нужный раздел", reply_markup=keyboard)
    else:
        await bot.send_message(message.from_user.id,
                               "Ссылки, содержащиеся в %s:\n %s" % (header.get_name(), header.links))


async def original_button_manager(message: types.Message):
    if message.text == kb.home.text:
        await process_start_command(message)
    if message.text == kb.back.text:
        if len(action_list) > 1:
            action_list.pop()
            h = action_list.pop()
            stack_store.clear()
            stack_store.extend(h.subheaders)
            action_list.append(h)
            await generate_button(h, message)
        else:
            await process_start_command(message)
    if message.text == kb.links.text:
        header = action_list.pop()
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
