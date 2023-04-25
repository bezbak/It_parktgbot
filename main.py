from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode
import os
import logging
from config import token

bot = Bot(token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

FILE_PATH = 'chat_ids.txt'
with open(FILE_PATH, 'r') as f:
    lines = f.readlines() 
        
list_of_groups = [line.strip() for line in lines]

async def save_chat_id(chat_id):
    """Сохранение chat_id в файл"""
    try:
        with open(FILE_PATH, 'a') as file:
            file.write(str(chat_id) + '\n')  # Записываем chat_id и добавляем символ переноса строки
        logging.info(f'Chat_id {chat_id} сохранен в файл.')
    except Exception as e:
        logging.exception('Ошибка при сохранении chat_id в файл: %s', e)
        
@dp.message_handler(content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
async def new_chat_members(message: types.Message):
    """Обработка события добавления бота в группу"""
    for member in message.new_chat_members:
        if member.id == bot.id:  # Проверяем, что добавленный участник - это наш бот
            chat_id = message.chat.id  # Получаем chat_id группы
            await save_chat_id(chat_id)  # Сохраняем chat_id в файл
   
async def send_message_to_group(chat_id, text):
    try:
        await bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.HTML)
    except Exception as e:
        logging.exception('Ошибка при отправке сообщения: %s', e)

@dp.message_handler(commands = 'start')
async def start(message: types.Message):
    if str(message.chat.id) in list_of_groups:
        pass
    else:
        await message.reply(f"Sup @{message.from_user.username} type command /help for information about functions of bot")

@dp.message_handler()
async def send_info(message:types.Message):
    for i in list_of_groups:
        if str(message.chat.id) in list_of_groups:
            pass
        else:   
            await send_message_to_group(i, message.text)

def main():
    executor.start_polling(dp, skip_updates=True) 

if __name__ == '__main__':
    main()