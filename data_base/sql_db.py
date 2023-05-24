import sqlite3 as sq
from create_bot import bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, message

def sql_start():
    global base, cur
    base = sq.connect('shop.db')
    cur = base.cursor()
    if base:
        print('База данных подключена')
    base.execute('CREATE TABLE IF NOT EXISTS shop(img TEXT, name TEXT PRIMARY KEY, tag TEXT, description TEXT, url TEXT, price TEXT)')
    base.commit()
        
async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO shop VALUES (?, ?, ?, ?, ?, ?)', tuple(data.values()))
        base.commit()


async def sql_read(message):
    

    for returns in cur.execute('SELECT * FROM shop').fetchall():
        item_photo = returns[0]
        item_name = returns[1]
        item_category = returns[2]
        item_description = returns[3]
        item_url = returns[4]
        item_price = returns[-1]
        keyboard = InlineKeyboardMarkup()

        url_button = InlineKeyboardButton('Ссылка', url=item_url)
        keyboard.add(url_button)  # Добавляем кнопку на клавиатуру

        # Отправляем фото товара вместе с описанием и клавиатурой
        await bot.send_photo(message.chat.id, item_photo, f'Название товара: {item_name}\nКатегория товара: {item_category}\nОписание товара: {item_description}\nЦена: {item_price}', reply_markup=keyboard)

        

async def sql_read2():
    return cur.execute('SELECT * FROM shop').fetchall()

async def sql_read_tags(message):
    tags = []  # Создаем пустой список для хранения тегов
    for returns in cur.execute('SELECT DISTINCT tag FROM shop').fetchall():
        tags.append(returns[0])  # Добавляем каждый тег в список

    keyboard = InlineKeyboardMarkup()  # Создаем объект клавиатуры

    # Добавляем кнопку "Все товары"
    all_items_button = InlineKeyboardButton('Все товары', callback_data='select_tag:all')
    keyboard.add(all_items_button)

    for tag in tags:
        button = InlineKeyboardButton(tag, callback_data=f'select_tag:{tag}')  # Создаем кнопку для каждого тега
        keyboard.add(button)  # Добавляем кнопку на клавиатуру

    await bot.send_message(message.from_user.id, "Выберите тег:", reply_markup=keyboard)


# async def sql_read_tags(message):
#     tags_set = set()  # Создаем множество для хранения уникальных тегов
#     for returns in cur.execute('SELECT tag FROM shop').fetchall():
#         tags_set.add(returns[0])  # Добавляем каждый тег в множество
#     tags_list = list(tags_set)  # Преобразуем множество обратно в список
#     keyboard = InlineKeyboardMarkup()  # Создаем объект клавиатуры
#     all_items_button = InlineKeyboardButton('Все товары', callback_data='select_tag:all')
#     keyboard.add(all_items_button)
#     for tag in tags_list:
#         button = InlineKeyboardButton(tag, callback_data=f'select_tag:{tag}')  # Создаем кнопку для каждого тега
#         keyboard.add(button)  # Добавляем кнопку на клавиатуру
#     await bot.send_message(message.from_user.id, "Выберите тег:", reply_markup=keyboard)

async def get_items_by_selected_tag(message, tag: str):
    # Ваш код для запроса товаров из базы данных по выбранному тегу (используя параметр tag)
    items = cur.execute('SELECT * FROM shop WHERE tag = ?', (tag,)).fetchall()
    # Отправляем товары пользователю
    for item in items:
        caption = f'Название товара: {item[1]}\nКатегория товара: {item[2]}\nОписание товара: {item[3]}\nЦена: {item[-1]}'
        await bot.send_photo(message.chat.id, item[0], caption)


async def sql_delete_command(data):
    cur.execute('DELETE FROM shop WHERE name == ? ', (data,))
    base.commit()
