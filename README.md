# Telegram Shop Bot
https://t.me/soul_In_bloom_bot
This is a Telegram bot designed for managing an online shop. The bot is capable of generating a list of products, categorizing them, and providing inline buttons for user interaction. It also includes an admin section where you can create, delete, and edit products.
### Stack

- Python 3.11
- Aiogram
- bautifulsoup4 (for parsing)
- requests

### Installation
1. Create a Telegram bot using BotFather and create a group for your shop.
2. Make the bot an administrator of the group.
3. Clone this repository to your local machine.
4. In the root directory of the project, create a .env file.
5. Inside the .env file, add your Telegram bot token in the following format:
```sh
TOKEN='your_bot_token_here'
```
6. Create and activate a virtual environment
```sh
python -m venv env
source env/Scripts/activate
```
7.Upgrade pip and install the required packages
```sh
python -m pip install --upgrade pip
pip install -r requirements.txt
```
8.Run the bot:
```sh
python bot_telegram.py
```
### Usage
1. After starting the bot, if you send the command `/start`, you will enter as a client.
2. Make yourself an administrator in the group or assign someone as an administrator.
3. If you want to access the admin panel and edit the shop's product list, enter the command `/moderator`.

