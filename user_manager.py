import psycopg2
import hashlib
from datetime import datetime
import streamlit as st
import pandas as pd
import decimal

conn = psycopg2.connect(st.secrets["DATABASE_URL"])
cursor = conn.cursor()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def user_exists(user_id):
    cursor.execute("SELECT user_id FROM users WHERE user_id = %s;", (user_id,))
    return cursor.fetchone() is not None

cursor.execute("DELETE FROM quizs WHERE created_at < NOW() - INTERVAL '30 days';")

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
    with connection.cursor() as cursor:  # Create fresh cursor
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
    try:
        if credits and credits[0] >= credits_to_use:
            cursor.execute("UPDATE users SET credits = credits - %s WHERE user_id = %s;", (credits_to_use, user_id))
            conn.commit()
            return True
        else:
            return False
    except psycopg2.Error:
        conn.rollback()
        return False, "error"

def can_get_gift(user_id):
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("SELECT last_gift_date FROM users WHERE user_id = %s;", (user_id,))
    row = cursor.fetchone()

    return not row or row[0] != today

def update_gift_date(user_id):
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("UPDATE users SET last_gift_date = %s WHERE user_id = %s;", (today, user_id))
    conn.commit()

def get_leaderboard_answers(limit=5):
    cursor.execute("""
        SELECT user_id, corrects_answers FROM users
        ORDER BY corrects_answers DESC
        LIMIT %s
    """, (limit,))
    return cursor.fetchall()

def get_leaderboard_xp(limit=5):
    cursor.execute("""
        SELECT user_id, xp FROM users
        ORDER BY xp DESC
        LIMIT %s
    """, (limit,))
    return cursor.fetchall()

def reset_daily_credits(user_id):
    cursor.execute("UPDATE users SET credits = credits + 3 WHERE user_id = %s;", (user_id,))
    conn.commit()

def get_user_data(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id = %s;", (user_id,))
    return cursor.fetchone()

def get_any_user_data(user_id, column):
    try:
        cursor.execute(f"SELECT {column} FROM users WHERE user_id = %s;", (user_id,))
        data = cursor.fetchone()
    except psycopg2.Error:
        conn.rollback()
    return data[0] if data else None

def add_correct_incorrect_answers(user_id, number=1, correct=True):
    try:
        if correct is True:
            cursor.execute(f"UPDATE users SET corrects_answers = corrects_answers + {number} WHERE user_id = %s;", (user_id,))
            conn.commit()
        return True
    except psycopg2.Error:
        return False

def get_users_number():
    cursor.execute("SELECT COUNT(*) FROM users;")
    return cursor.fetchone()[0]

def insert_quiz(user_id, subject, correct_answers, wrong_answers):
    cursor.execute("INSERT INTO quizs (user_id, created_at, subject, correct_answers, wrong_answers) VALUES (%s, %s, %s, %s, %s)", (user_id, datetime.now(), subject, correct_answers, wrong_answers))
    conn.commit()
    return True

def get_stats(user_id, column):
    query = f"SELECT DISTINCT {column} FROM quizs WHERE user_id = %s ORDER BY subject"
    cursor.execute(query, (user_id,))
    rows = cursor.fetchall()
    return [row[0] for row in rows]

def get_stats_number(user_id, column, subject):
    query = f"SELECT SUM({column}) FROM quizs WHERE user_id = %s AND subject = %s"
    cursor.execute(query, (user_id, subject))
    result = cursor.fetchone()
    return result[0] if result[0] is not None else 0

def get_total_quiz_count(user_id):
    query = "SELECT COUNT(*) FROM quizs WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    return result[0] if result[0] is not None else 0

def progression_user(user_id, subject):

    conn = psycopg2.connect(st.secrets["DATABASE_URL"])
    cursor = conn.cursor()

    query = """
        SELECT created_at, 
               SUM(correct_answers) AS total_correct, 
               SUM(wrong_answers) AS total_wrong,
               (SUM(correct_answers) + SUM(wrong_answers)) AS total_questions,
               ROUND((SUM(correct_answers) * 20.0) / (SUM(correct_answers) + SUM(wrong_answers)), 1) AS note_sur_20
        FROM quizs
        WHERE user_id = %s
        AND subject = %s
        GROUP BY created_at
        ORDER BY created_at ASC;
    """

    cursor.execute(query, (user_id, subject))
    rows = cursor.fetchall()

    if not rows:
        return pd.DataFrame(columns=["Date", "Bonnes Réponses", "Mauvaises Réponses", "Note sur 20"])

    df = pd.DataFrame(rows, columns=["Date", "Bonnes Réponses", "Mauvaises Réponses", "Total Questions", "Note sur 20"])
    df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")

    df["Bonnes Réponses"] = df["Bonnes Réponses"].apply(lambda x: float(x) if isinstance(x, decimal.Decimal) else x)
    df["Mauvaises Réponses"] = df["Mauvaises Réponses"].apply(lambda x: float(x) if isinstance(x, decimal.Decimal) else x)
    df["Note sur 20"] = df["Note sur 20"].apply(lambda x: float(x) if isinstance(x, decimal.Decimal) else x)

    return df

def get_average_quiz_score(user_id):
    query = "SELECT ROUND(AVG((correct_answers * 20.0) / (correct_answers + wrong_answers)), 1) AS moyenne_note FROM quizs WHERE user_id = %s;"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    return round(result[0], 2) if result[0] is not None else 0.0

def gift_to_kaimana(user_id, xp,):
    cursor.execute(f"UPDATE users SET xp = xp + {xp} WHERE user_id = %s;", ("Kaimana",))
    cursor.execute(f"UPDATE users SET xp = xp - {xp} WHERE user_id = %s;", (user_id,))
    conn.commit()

def is_user_profile_complete(user_id):
    cursor.execute("""
        SELECT favorite_subject, least_favorite_subject, class_level 
        FROM users WHERE user_id = %s;
    """, (user_id,))
    row = cursor.fetchone()

    return row and all(row)
