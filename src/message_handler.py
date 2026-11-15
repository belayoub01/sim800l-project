import sqlite3
from pathlib import Path


def initialize_database(database_path):
    path = Path(database_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(path) as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT NOT NULL,
                message TEXT NOT NULL,
                received_at TEXT NOT NULL,
                source_file TEXT NOT NULL UNIQUE,
                processed_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)


def save_message(database_path, sender, message, received_at, source_file):
    with sqlite3.connect(database_path, timeout=10) as db:
        cursor = db.execute(
            """
            INSERT OR IGNORE INTO messages
                (sender, message, received_at, source_file)
            VALUES (?, ?, ?, ?)
        """,
            (sender, message, received_at, source_file),
        )

        return cursor.rowcount == 1
