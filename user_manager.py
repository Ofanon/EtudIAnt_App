import psycopg2
import hashlib
from datetime import datetime
import streamlit as st

conn = psycopg2.connect(st.secrets["DATABASE_URL"])
cursor = conn.cursor()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def user_exists(user_id):
    cursor.execute("SELECT user_id FROM users WHERE user_id = %s;", (user_id,))
    return cursor.fetchone() is not None

def register_user(user_id, password):
    if user_exists(user_id):
        return False
    cursor.execute("""
        INSERT INTO users (user_id, password, created_at) 
        VALUES (%s, %s, %s)
    """, (user_id, hash_password(password), datetime.now()))
    conn.commit()
    return True

def authenticate_user(user_id, password):
    cursor.execute("SELECT password FROM users WHERE user_id = %s;", (user_id,))
    result = cursor.fetchone()
    return result and result[0] == hash_password(password)

def get_xp(user_id):
    cursor.execute("SELECT xp FROM users WHERE user_id = %s;", (user_id,))
    xp = cursor.fetchone()
    return xp[0] if xp else 0

def add_xp(user_id, points):
    cursor.execute("UPDATE users SET xp = xp + %s WHERE user_id = %s;", (points, user_id))
    conn.commit()

def remove_xp(user_id, points):
    cursor.execute("UPDATE users SET xp = GREATEST(xp - %s, 0) WHERE user_id = %s;", (points, user_id))
    conn.commit()

def get_credits(user_id):
    cursor.execute("SELECT credits FROM users WHERE user_id = %s;", (user_id,))
    credits = cursor.fetchone()
    return credits[0] if credits else 0

def add_credits(user_id, xp_used, amount):
    cursor.execute("SELECT xp FROM users WHERE user_id = %s;", (user_id,))
    xp = cursor.fetchone()

    if xp and xp[0] >= xp_used:
        cursor.execute("""
            UPDATE users SET credits = credits + %s, xp = GREATEST(xp - %s, 0)
            WHERE user_id = %s;
        """, (amount, xp_used, user_id))
        conn.commit()
        return True
    return False

def use_credit(user_id, credits_to_use=1):
    cursor.execute("SELECT credits FROM users WHERE user_id = %s;", (user_id,))
    credits = cursor.fetchone()

    if credits and credits[0] >= credits_to_use:
        cursor.execute("UPDATE users SET credits = credits - %s WHERE user_id = %s;", (credits_to_use, user_id))
        conn.commit()
        return True
    return False

def can_spin_wheel(user_id):
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("SELECT last_spin_date FROM users WHERE user_id = %s;", (user_id,))
    row = cursor.fetchone()

    return not row or row[0] != today

def update_date_spin_wheel(user_id):
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("UPDATE users SET last_spin_date = %s WHERE user_id = %s;", (today, user_id))
    conn.commit()

def get_leaderboard(limit=5):
    cursor.execute("""
        SELECT user_id, xp FROM users
        ORDER BY xp DESC
        LIMIT %s
    """, (limit,))
    return cursor.fetchall()

def get_user_data(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id = %s;", (user_id,))
    return cursor.fetchone()

def get_any_user_data(user_id, column):
    cursor.execute(f"SELECT {column} FROM users WHERE user_id = %s;", (user_id,))
    data = cursor.fetchone()
    return data[0] if data else None

def is_user_profile_complete(user_id):
    cursor.execute("""
        SELECT favorite_subject, least_favorite_subject, class_level 
        FROM users WHERE user_id = %s;
    """, (user_id,))
    row = cursor.fetchone()
    return row and all(row)
