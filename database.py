import sqlite3
import hashlib
from datetime import datetime

DB_NAME = "duriasense.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'Farmer'
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            image_name TEXT,
            disease_result TEXT NOT NULL,
            confidence REAL NOT NULL,
            risk_level TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()

def add_user(full_name, username, password, role="Farmer"):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (full_name, username, password, role)
            VALUES (?, ?, ?, ?)
        """, (
            str(full_name),
            str(username),
            hash_password(password),
            str(role)
        ))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()

def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, full_name, username, role
        FROM users
        WHERE username = ? AND password = ?
    """, (
        str(username),
        hash_password(password)
    ))

    user = cursor.fetchone()
    conn.close()
    return user

def save_prediction(user_id, image_name, disease_result, confidence, risk_level):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predictions
        (user_id, image_name, disease_result, confidence, risk_level, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        int(user_id),
        str(image_name),
        str(disease_result),
        float(confidence),
        str(risk_level),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

def get_user_predictions(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT image_name, disease_result, confidence, risk_level, created_at
        FROM predictions
        WHERE user_id = ?
        ORDER BY id DESC
    """, (int(user_id),))

    records = cursor.fetchall()
    conn.close()
    return records

def get_all_predictions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            predictions.id,
            users.full_name,
            users.username,
            predictions.image_name,
            predictions.disease_result,
            predictions.confidence,
            predictions.risk_level,
            predictions.created_at
        FROM predictions
        JOIN users ON predictions.user_id = users.id
        ORDER BY predictions.id DESC
    """)

    records = cursor.fetchall()
    conn.close()
    return records

def change_password(user_id, old_password, new_password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT password FROM users
        WHERE id = ?
    """, (int(user_id),))

    user = cursor.fetchone()

    if not user:
        conn.close()
        return "User not found."

    old_hashed = hash_password(old_password)

    if user[0] != old_hashed:
        conn.close()
        return "Old password is incorrect."

    cursor.execute("""
        UPDATE users
        SET password = ?
        WHERE id = ?
    """, (hash_password(new_password), int(user_id)))

    conn.commit()
    conn.close()

    return "success"

def get_user_predictions_with_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, image_name, disease_result, confidence, risk_level, created_at
        FROM predictions
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,))

    records = cursor.fetchall()
    conn.close()
    return records


def delete_prediction(prediction_id, user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM predictions
        WHERE id = ? AND user_id = ?
    """, (prediction_id, user_id))

    conn.commit()
    conn.close()


def reset_password_by_username(username, new_password):
    conn = get_connection()
    cursor = conn.cursor()

    hashed_password = hash_password(new_password)

    cursor.execute("""
        UPDATE users
        SET password = ?
        WHERE username = ?
    """, (hashed_password, username))

    conn.commit()
    affected_rows = cursor.rowcount
    conn.close()

    if affected_rows > 0:
        return "success"
    else:
        return "Username not found."