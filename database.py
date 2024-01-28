import sqlite3
# Создание таблицы для хранения счетчика пользователей, если она не существует
conn = sqlite3.connect('user_counts.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_counts (
        user_id INTEGER PRIMARY KEY,
        count INTEGER NOT NULL DEFAULT 1
    )
''')
conn.commit()



# Функция для увеличения счетчика взаимодействий пользователя
def increment_user_count(user_id):
    conn = sqlite3.connect('user_counts.db')
    cursor = conn.cursor()

    cursor.execute('SELECT count FROM user_counts WHERE user_id=?', (user_id,))
    user_record = cursor.fetchone()
    if user_record is None:
        cursor.execute('INSERT INTO user_counts (user_id, count) VALUES (?, 1)', (user_id,))
    else:
        new_count = user_record[0] + 1
        cursor.execute('UPDATE user_counts SET count=? WHERE user_id=?', (new_count, user_id))

    conn.commit()
    conn.close()



def get_all_users():
    conn = sqlite3.connect('user_counts.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM user_counts')
    users = [user_id[0] for user_id in cursor.fetchall()]  # Extracting user IDs from the list of tuples
    conn.close()
    return users


# Функция для просмотра количества пользователей
def get_user_count():
    conn = sqlite3.connect('user_counts.db')
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM user_counts')
    count = cursor.fetchone()[0]

    conn.close()
    return count
