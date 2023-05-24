import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from create_bot import dp
from data_base import sql_db

from handlers import client, admin, other

logging.basicConfig(level=logging.INFO)

async def on_startup(_):
    print('Бот запущен')
    sql_db.sql_start()

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
other.register_handlers_other(dp)



executor.start_polling(dp, skip_updates=True, on_startup=on_startup)