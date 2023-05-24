import requests
from bs4 import BeautifulSoup

# Функция для получения HTML-кода страницы по ссылке
def get_html(url):
    response = requests.get(url)
    return response.text

# Функция для парсинга цены товара
def parse_price(html):
    soup = BeautifulSoup(html, 'html.parser')
    price_element = soup.find('span', {'class': 'product-price'})  # Здесь необходимо указать правильный селектор для цены товара
    price = price_element.text.strip() if price_element else 'Цена не найдена'
    return price

# URL-адрес страницы с товаром
url = 'https://www.wildberries.ru/catalog/21209499/detail.aspx'  # Здесь укажите ссылку на конкретный товар

# Получаем HTML-код страницы
html = get_html(url)

# Парсим цену товара
price = parse_price(html)

# Выводим цену товара
print(f'Цена товара: {price}')