import sqlite3
import hashlib
from datetime import datetime

DB_FILE = "data/users.db"

def create_db():
    """Crée ou met à jour la base de données avec les nouvelles colonnes."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            email TEXT UNIQUE,
            credits INTEGER DEFAULT 5,
            xp INTEGER DEFAULT 0,
            last_spin_date TEXT DEFAULT NULL,
            role TEXT DEFAULT 'user',
            created_at TEXT NOT NULL,
            class_level TEXT DEFAULT NULL,
            favorite_subject TEXT DEFAULT NULL,
            least_favorite_subject TEXT DEFAULT NULL
            )
    """)

    cursor.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if "xp" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN xp INTEGER DEFAULT 0")
    if "credits" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN credits INTEGER DEFAULT 5")
    if "class_level" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN class_level TEXT DEFAULT NULL")
    if "favorite_subject" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN favorite_subject TEXT DEFAULT NULL")
    if "least_favorite_subject" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN least_favorite_subject TEXT DEFAULT NULL")
    if "last_spin_date" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN last_spin_date TEXT DEFAULT NULL")
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def user_exists(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def register_user(user_id, password):
    if user_exists(user_id):
        return False
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (user_id, password, created_at) VALUES (?, ?, ?)", 
                   (user_id, hash_password(password), datetime.now()))
    conn.commit()
    conn.close()
    return True

def authenticate_user(user_id, password):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result and result[0] == hash_password(password)

def get_xp(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT xp FROM users WHERE user_id = ?", (user_id,))
    xp = cursor.fetchone()
    conn.close()
    return xp[0] if xp else 0

def add_xp(user_id, points):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET xp = xp + ? WHERE user_id = ?", (points, user_id))
    conn.commit()
    conn.close()

def remove_xp(user_id, points):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET xp = MAX(xp - ?, 0) WHERE user_id = ?", (points, user_id))
    conn.commit()
    conn.close()

def get_credits(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT credits FROM users WHERE user_id = ?", (user_id,))
    credits = cursor.fetchone()
    conn.close()
    return credits[0] if credits else 0

def add_credits(user_id, xp_used, amount):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT xp FROM users WHERE user_id = ?", (user_id,))
        xp = cursor.fetchone()
        if xp and xp[0] >= xp_used:
            cursor.execute("UPDATE users SET credits = credits + ? WHERE user_id = ?", (amount, user_id))
            cursor.execute("UPDATE users SET xp = MAX(xp - ?, 0) WHERE user_id = ?", (xp_used, user_id))
            return True
        else:
            return False
    except Exception as e:
        print(f"Erreur dans add_credits: {e}")
        return False
    finally:
        conn.commit()
        conn.close()

def use_credit(user_id, credits_to_use):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT credits FROM users WHERE user_id = ?", (user_id,))
    credits = cursor.fetchone()

    if credits and credits[0] - credits_to_use > 0:
        cursor.execute("UPDATE users SET credits = credits - ? WHERE user_id = ?", (credits_to_use, user_id))
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False
    
def reset_daily_credits(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET credits = credits + 2 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def is_user_profile_complete(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT favorite_subject, least_favorite_subject, class_level FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    if row and all(row):
        return True
    return False

def get_user_data(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    return user_data

def get_any_user_data(user_id, column):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(f"SELECT {column} FROM users WHERE user_id = ?", (user_id,))
    data = cursor.fetchone()
    conn.close()
    return data[0]

def can_spin_wheel(user_id):
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    cursor = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("SELECT last_spin_date FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    if row and row[0] == today:
        conn.close()
        return False
    conn.close()
    return True

def update_date_spin_wheel(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("UPDATE users SET last_spin_date = ? WHERE user_id = ?", (today,user_id))
    conn.commit()
    conn.close()

def get_leaderboard(limit=5):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT user_id, xp FROM users
        ORDER BY xp DESC
        LIMIT ?
    """, (limit,))
    return cursor.fetchall()
create_db()