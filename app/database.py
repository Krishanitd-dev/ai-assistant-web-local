import sqlite3

DATABASE = "conversations.db"


def get_connection():
    return sqlite3.connect(DATABASE)

def create_table():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            answer TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

def save_conversation(question, answer):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO conversations(question, answer)
        VALUES(?, ?)
    """, (question, answer))

    conn.commit()

    conn.close()


def get_all_conversations():

    conn = get_connection()

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM conversations
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows

def delete_conversation(id):
    conn = get_connection()
    conn.row_factory =sqlite3.Row

    cursor =conn.cursor()
    cursor.execute("""
    DELETE FROM conversations
    WHERE id = ?
    """,(id,))
    conn.commit()
    conn.close()
