from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_client
from data_base import sql_db
import data_base.sql_db as sql_db





async def command_start(message: types.Message):
    try:
        await bot.send_message(
            message.from_user.id,
            'Добро пожаловать в наш магазин',
            reply_markup=kb_client)
        await message.delete()
    except Exception:
        await message.reply(
            'Общение с ботом через ЛС, напишите ему: \
            \nhttps://t.me/soul_In_bloom_bot')
        # You can also log the exception if needed: print(e)

@dp.message_handler(lambda message: 'связаться' in message.text)
async def command_contacts(message: types.Message):
    await bot.send_message(
        message.from_user.id, 'telegram производителя: \
        \nhttps://t.me/anastasiya_shabalkina')


async def command_number(message: types.Message):
    await bot.send_message(
        message.from_user.id, 'Номер счёта:\n0000 0000 0000 0007')

@dp.message_handler(lambda message: 'информация' in message.text)
async def info_product(message: types.Message):
    await bot.send_message(
        message.from_user.id, 'Soul in Bloom - украшения из сухоцветов')
    
#@dp.message_handler(lambda message: 'товар' in message.text)
async def command_shop(message: types.Message):
    #await sql_db.sql_read(message)
    await sql_db.sql_read_tags(message)

#@dp.callback_query_handler(lambda query: query.data.startswith('select_tag:'))

async def handle_select_tag(callback_query: types.CallbackQuery):
    selected_tag = callback_query.data.split(':')[1]  # Получаем выбранный тег

    if selected_tag == 'all':
        await sql_db.sql_read(callback_query.message)
    else:
        await sql_db.get_items_by_selected_tag(callback_query.message, selected_tag)

    await callback_query.answer()

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(command_contacts, commands=['Контакты'])
    dp.register_message_handler(command_number, commands=['Номер_счёта'])
    dp.register_message_handler(
        info_product, commands=['Информация_о_товаре'])
    dp.register_message_handler(command_shop, commands=['Магазин'])
    dp.register_callback_query_handler(handle_select_tag, lambda c: c.data == 'sql_read')
    dp.register_callback_query_handler(handle_select_tag, lambda query: query.data.startswith('select_tag:'))
