from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()


load_dotenv()

bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot, storage=storage)
