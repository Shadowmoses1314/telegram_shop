from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


b1 = KeyboardButton('/Контакты')
b2 = KeyboardButton('/Номер_счёта')
b3 = KeyboardButton('/Информация_о_товаре')
b4 = KeyboardButton('Поделится номером', request_contact=True)
b5 = KeyboardButton('моё местоположение', request_location=True)
b6 = KeyboardButton('/Магазин')
kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(b6).add(b1).row(b2).insert(b3).row(b4).add(b5)