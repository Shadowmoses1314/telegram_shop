from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# кнопки для админа
button_load = KeyboardButton('/Загрузить')
button_delete = KeyboardButton('/Удалить')
button_exit = KeyboardButton('/Выход')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(button_load).add(button_delete).add(button_exit)