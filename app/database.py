import sqlite3
import os
from pwdlib import PasswordHash
password_hasher = PasswordHash.recommended()

DATABASE = os.getenv("DATABASE", "conversation.db")


def get_connection():
    return sqlite3.connect(DATABASE)

def create_table():

    conn = get_connection()
    cursor = conn.cursor()



    cursor.execute("""
        CREATE TABLE IF NOT EXISTS userdata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            answer TEXT,
            email TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)


    conn.commit()
    conn.close()


def create_user(email, password_hash, created_at):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO userdata (email, password_hash, created_at)
        VALUES (?, ?, ?)
        """, (email, password_hash, created_at))
    conn.commit()
    conn.close()
    

def get_user(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, email, password_hash, created_at
        FROM userdata 
        WHERE email = ?
        """, (email,))
    user = cursor.fetchone()
    conn.close()
    return user

def save_conversation(email, question, answer):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO conversations(email, question, answer)
        VALUES(?, ?, ? )
    """, (email, question, answer))

    conn.commit()

    conn.close()


def get_all_conversations(email):

    conn = get_connection()

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM conversations
        WHERE email = ? ORDER BY id DESC
    """, (email,))

    rows = cursor.fetchall()

    conn.close()

    return rows

def delete_conversation(id, email):
    conn = get_connection()
    conn.row_factory =sqlite3.Row

    cursor =conn.cursor()
    cursor.execute("""
    DELETE FROM conversations
    WHERE id = ? AND email = ?
    """,(id, email))
    conn.commit()
    conn.close()
