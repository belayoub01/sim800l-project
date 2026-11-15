import sqlite3

from message_handler import initialize_database, save_message


def test_message_saved_once(tmp_path):
    database_path = tmp_path / "messages.db"

    initialize_database(database_path)

    arguments = (
        str(database_path),
        "+213600000000",
        "Test message",
        "2026-11-14 10:00:00",
        "IN_test.txt",
    )

    assert save_message(*arguments) is True
    assert save_message(*arguments) is False

    with sqlite3.connect(database_path) as db:
        count = db.execute("SELECT COUNT(*) FROM messages").fetchone()[0]

    assert count == 1
