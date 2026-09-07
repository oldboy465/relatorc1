import sqlite3
from config import DATABASE_PATH
from database.models import CREATE_TABLES_SQL

def get_db_connection():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    with get_db_connection() as conn:
        conn.executescript(CREATE_TABLES_SQL)
        conn.commit()

if __name__ == "__main__":
    init_db()
    print(f"Banco SQLite inicializado em: {DATABASE_PATH}")