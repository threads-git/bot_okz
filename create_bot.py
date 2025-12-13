import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import os
load_dotenv()

token = os.getenv('TOKEN')
admins = [int(admin_id) for admin_id in os.getenv('ADMINS').split(',')]

# настраиваем логирование и выводим в переменную для отдельного использования в нужных местах
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# инициируем объект, который будет отвечать за взаимодействие с базой данных
# db_manager = DatabaseManager(dsn=config('PG_LINK'), deletion_password=config('ROOT_PASS'))

# инициируем объект бота, передавая ему parse_mode=ParseMode.HTML по умолчанию
bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
# bot = Bot(token=config('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# инициируем объект бота
dp = Dispatcher(storage=MemoryStorage())