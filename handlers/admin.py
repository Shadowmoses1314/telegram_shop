from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from data_base import sql_db
from keyboards import admin_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from bs4 import BeautifulSoup

ID = None

class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    tag = State()
    description = State()
    url = State()
    price = State()

# Поучаем ID модератора
# @dp.message_handler(commands=['moderator'], is_chat_admin=True)


async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Вы успешно зарегистрированы', reply_markup=admin_kb.button_case_admin)
    await message.delete()  

# Начало загрузки нового товара
# @dp.message_handler(state=None, commands='Загрузить')

async def cm_start(message: types.Message):
    if message.from_user.id == ID:   
        await FSMAdmin.photo.set()
        await message.reply('Загрузить фото')


# выход из состояний
# @dp.message_handler(commands='Выход', state='*')
# @dp.message_handler(Text(equote='Выход',ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('До свидания!')

# ловим фото и пишем в словарь 
# @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('Введите название товара')

# ловим название
# @dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        available_tags = ['Тег1', 'Тег2', 'Тег3']

        # Создайте Inline клавиатуру с кнопками тегов
        keyboard = InlineKeyboardMarkup(row_width=2)
        for tag in available_tags:
            keyboard.add(InlineKeyboardButton(tag, callback_data=tag))
        global available_tags_keyboard
        available_tags_keyboard = keyboard

        # Сохраните состояние и отправьте сообщение с клавиатурой
        await FSMAdmin.tag.set()
        await message.reply('Выберите тег:', reply_markup=keyboard)
        



@dp.callback_query_handler(state=FSMAdmin.tag)
async def process_tag_selection(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.from_user.id == ID:
        # Получите выбранный тег из callback_data
        selected_tag = callback_query.data

        # Сохраните выбранный тег в состоянии
        async with state.proxy() as data:
            data['tag'] = selected_tag

        # Переходите к следующему состоянию или выполняйте необходимые действия
        await FSMAdmin.next()

        # Отправьте сообщение с просьбой ввести описание товара
        await callback_query.message.reply('Введите описание товара')

# ловим описание
# @dp.message_handler(state=FSMAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply('Введите ссылку на товар')

async def load_url(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['url'] = message.text
        await FSMAdmin.next()
      
        await message.reply('Введите цену товара')       

# ловим цену
# @dp.message_handler(state=FSMAdmin.price)
async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        price_text = message.text
        try:
            price = float(price_text)
        except ValueError:
            await message.reply("Некорректное значение цены. Пожалуйста, введите числовое значение.")
            return
        
        async with state.proxy() as data:
            data['price'] = price
        await sql_db.sql_add_command(state)
        await state.finish()

@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del'))
async def delete_callback_run(callback_query: types.CallbackQuery):
    await sql_db.sql_delete_command(callback_query.data.replace('del', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удален.', show_alert=True)


@dp.message_handler(commands='Удалить')
async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        read = await sql_db.sql_read2()
        for returns in read:
            await bot.send_photo(message.from_user.id, returns[0], f'{returns[1]} \n Описание: {returns[2]} \n Цена: {returns[-1]}')
            await bot.send_message(
                message.from_user.id, text='-> X',
                reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(f'Удалить {returns[1]}',
                                                                             callback_data=f'del {ret[1]}')))


# Регистрируем хендлеры
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands='Загрузить', state=None)
    dp.register_message_handler(cancel_handler, Text(equals='Выход', ignore_case=True), state='*')
    dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin=True)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    #dp.register_message_handler(load_tag, state=FSMAdmin.tag)
    dp.register_callback_query_handler(process_tag_selection, state=FSMAdmin.description)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_url, state=FSMAdmin.url)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(cancel_handler, commands='Выход', state='*')
    dp.register_callback_query_handler(delete_callback_run, lambda x: x.data and x.data.startswith('del'))

