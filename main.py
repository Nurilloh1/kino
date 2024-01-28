import logging
import telebot
import sqlite3
from telebot import types
from database import increment_user_count, get_user_count, get_all_users
# Замените 'YOUR_BOT_TOKEN' на ваш токен бота
TOKEN = '6971328805:AAGku1ZPWp5djRgwfggjRIWIh0tA2ti8iPM'
logging.basicConfig(level=logging.INFO)

bot = telebot.TeleBot(TOKEN)

admin = 717474239
channel_id = '-1002046764189'

@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    increment_user_count(user_id)
    file_path = './user_counts.db'
    descr = f"Users {get_user_count()}"
    with open(file_path, 'rb') as file:
        bot.send_document(chat_id='-1001977096417', document=file, caption=descr)
    bot.send_message(admin, f"Ism: {message.from_user.first_name}\nFamiliya: {message.from_user.last_name}\nUsername: @{message.from_user.username}\nStart bosdi")
    bot.reply_to(message, "Salom, kormoqchi bolgan filmingiz ID'sini yuboring")


@bot.message_handler(commands=['users'])
def start_command(message):
    user_id = message.from_user.id
    if user_id == admin:
      bot.reply_to(message, f"Users {get_user_count()}")


# Создаем словарь для хранения сообщений пользователей
message_to_send = {}

# При получении команды /rek бот запрашивает у пользователя сообщение для отправки
@bot.message_handler(commands=['rek'])
def request_message_for_broadcast(message):
    user_id = message.from_user.id
    if user_id == admin:
        bot.send_message(user_id, "Yubormoqchi bolgan habaringizni yuboring.")
        bot.register_next_step_handler(message, send_message_to_all)

# Обработчик для отправки сообщения всем пользователям
def send_message_to_all(message):
    global message_to_send
    message_to_send = message.text

    # Отправляем сообщение другим пользователям
    for user_id in get_all_users():
        try:
            bot.forward_message(user_id, admin, message.message_id)
        except Exception as e:
            # Если не удалось отправить сообщение, удаляем пользователя
            delete_user(user_id)
    
    # Отправляем администратору количество пользователей
    bot.send_message(admin, f"Habar {get_user_count()} ta userga yuborildi.")

# Функция для удаления пользователя из базы данных
def delete_user(user_id):
    conn = sqlite3.connect('user_counts.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM user_counts WHERE user_id=?', (user_id,))

    conn.commit()
    conn.close()

@bot.message_handler(func=lambda message: message.text.isdigit())
def handle_number_message(message):
    user_id = message.from_user.id
    increment_user_count(user_id)
    # Проверяем, было ли сообщение переслано
    if message.forward_from_chat and message.forward_from_chat.type == 'channel':
        # Не обрабатываем пересланные сообщения, чтобы избежать циклов
        return

    channel_id = '-1002046764189'  # Замените '-1002046764189' на актуальный ID вашего канала
    message_id = int(message.text)

    try:
        channel_message = bot.forward_message(message.chat.id, channel_id, message_id)
        if channel_message.text:
            bot.send_message(message.chat.id, channel_message.text)                
    except telebot.apihelper.ApiException as e:
        bot.reply_to(message, f"{message_id}-ID bilan hech qanday film topilmadi!")



def main():
    bot.polling(none_stop=True)



def main():
    bot.polling(none_stop=True)

if __name__ == '__main__':
    main()

