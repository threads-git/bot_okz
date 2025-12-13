from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.all_kb import main_kb, register_kb

from utils.database import Database
from aiogram.utils.chat_action import ChatActionSender
import os

db = Database(os.getenv('DATABASE_NAME'))
start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message, bot: Bot):
    # create_db=db.create_db()
    # create_db
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        users = db.select_user_id(message.from_user.id)
    if users:
        await message.answer( f'Приветствую тебя мой дорогой друг!\n'
                              f'Если ты сюда зашел, видимо, что-то пошло не так...\n'
                              f'Не переживай, завтра будет лучше...', reply_markup=main_kb(message.from_user.id))
    else:
        await bot.send_message(message.from_user.id, f'Здравствуйте, рад видеть Вас!\nНужна регистрация', reply_markup=register_kb())
