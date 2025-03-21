import sqlite3

def init_db():
    """Initialize the database and create the users table if it doesn't exist."""
    conn = sqlite3.connect("telegram_bot.db")
    cursor = conn.cursor()

    # Create the users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            telegram_id INTEGER PRIMARY KEY,
            fullname TEXT NOT NULL,
            nickname TEXT NOT NULL,
            group_name TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def save_user(telegram_id, fullname, nickname, group_name):
    """Save user data to the database."""
    conn = sqlite3.connect("telegram_bot.db")
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO users (telegram_id, fullname, nickname, group_name)
        VALUES (?, ?, ?, ?)
    ''', (telegram_id, fullname, nickname, group_name))

    conn.commit()
    conn.close()

def update_user(telegram_id, fullname, nickname, group_name):
    """Update user data in the database."""
    conn = sqlite3.connect("telegram_bot.db")
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE users
        SET fullname = ?, nickname = ?, group_name = ?
        WHERE telegram_id = ?
    ''', (fullname, nickname, group_name, telegram_id))

    conn.commit()
    conn.close()

def user_exists(telegram_id):
    """Check if user already exists in the database."""
    conn = sqlite3.connect("telegram_bot.db")
    cursor = conn.cursor()

    cursor.execute('SELECT 1 FROM users WHERE telegram_id = ?', (telegram_id,))
    result = cursor.fetchone()

    conn.close()
    return result is not None

def get_user_by_telegram_id(telegram_id):
    """Get user data by telegram_id."""
    conn = sqlite3.connect("telegram_bot.db")
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE telegram_id = ?', (telegram_id,))
    user = cursor.fetchone()

    conn.close()

    if user:
        return {
            'telegram_id': user[0],
            'fullname': user[1],
            'nickname': user[2],
            'group': user[3]
        }
    return None
