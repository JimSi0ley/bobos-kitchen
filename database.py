import sqlite3
from functions import connect_to_db, get_database_path

def create_database():
    connection = sqlite3.connect(get_database_path())

    cursor = connection.cursor()

    cursor.execute("""
   CREATE TABLE IF NOT EXISTS recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    category TEXT,
    cook_time INTEGER,
    ingredients TEXT,
    instructions TEXT
    )
    """)

    connection.commit()

    connection.close()

def add_favorite_column():
    connection, cursor = connect_to_db()

    try:
        cursor.execute("""
            ALTER TABLE recipes
            ADD COLUMN favorite INTEGER NOT NULL DEFAULT 0
        """)

        connection.commit()

    except Exception:
        # Column already exists
        pass

    connection.close()

def add_photo_column():
    connection, cursor = connect_to_db()

    try:
        cursor.execute("""
            ALTER TABLE recipes
            ADD COLUMN photo_filename TEXT
        """)

        connection.commit()

    except Exception:
        # The column already exists
        pass

    connection.close()

def add_rating_column():
    connection, cursor = connect_to_db()

    try:
        cursor.execute("""
            ALTER TABLE recipes
            ADD COLUMN rating INTEGER NOT NULL DEFAULT 0
        """)

        connection.commit()

    except Exception:
        pass

    finally:
        connection.close()
