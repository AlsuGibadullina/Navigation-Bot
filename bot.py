from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import keyboard as kb
from config import TOKEN
from parsing.header import Header
from parsing.parser import get_headings

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
stack_store = [Header()]
action_list = [Header()]


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    stack_store.clear()
    action_list.clear()
    headers = get_headings()
    stack_store.extend(headers)
    keyboard = kb.create_keyboard_start(headers)
    await message.reply("Что вас интересует?", reply_markup=keyboard)


@dp.message_handler()
async def message_catcher(message: types.Message):
    if len(action_list) > 0:
        header = action_list.pop()
        action_list.append(header)
        links = header.get_links()
        if len(links) > 0:
            await bot.send_message(message.from_user.id,
                                   "Ссылки, содержащиеся в %s:\n %s" % (header.get_name(), links))
    await original_buttons_manager(message)
    for head in stack_store:
        if head.get_name() == message.text:
            action_list.append(head)
            await generate_button(head, message)


async def generate_button(header, message: types.Message):
    subheaders = header.subheaders
    if len(subheaders) > 0:
        stack_store.clear()
        stack_store.extend(subheaders)
        keyboard = kb.create_keyboard(subheaders)
        await message.reply("Выберите из перечня нужный раздел", reply_markup=keyboard)
    else:
        action_list.pop()
        await bot.send_message(message.from_user.id,
                               "Ссылки, содержащиеся в %s:\n %s" % (header.get_name(), header.links))


async def original_buttons_manager(message: types.Message):
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


if __name__ == '__main__':
    executor.start_polling(dp)
