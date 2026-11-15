import sqlite3

import pytest

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


@pytest.fixture
def db_path(tmp_path):
    path = tmp_path / "messages.db"
    initialize_database(path)
    return str(path)


def count_rows(db_path):
    with sqlite3.connect(db_path) as db:
        return db.execute("SELECT COUNT(*) FROM messages").fetchone()[0]


def test_multiple_messages_saved(db_path):
    for i in range(5):
        assert save_message(db_path, "+213600000000", f"msg {i}",
                            "2026-11-14 10:00:00", f"IN_{i}.txt") is True
    assert count_rows(db_path) == 5


def test_arabic_message(db_path):
    save_message(db_path, "+213600000000", "مرحبا بالعالم",
                 "2026-11-14 10:00:00", "IN_ar.txt")
    with sqlite3.connect(db_path) as db:
        text = db.execute("SELECT message FROM messages").fetchone()[0]
    assert text == "مرحبا بالعالم"


def test_long_message(db_path):
    long_text = "a" * 500
    assert save_message(db_path, "+213600000000", long_text,
                        "2026-11-14 10:00:00", "IN_long.txt") is True


def test_empty_message_is_stored(db_path):
    # NOT NULL يقبل النص الفارغ؛ نوثّق هذا السلوك صراحةً
    assert save_message(db_path, "+213600000000", "",
                        "2026-11-14 10:00:00", "IN_empty.txt") is True


def test_null_sender_is_ignored(db_path):
    # INSERT OR IGNORE يتخطى الصف المخالف للقيد بدل رفع استثناء
    assert save_message(db_path, None, "x",
                        "2026-11-14 10:00:00", "IN_null.txt") is False
    assert count_rows(db_path) == 0


def test_initialize_creates_missing_folder(tmp_path):
    path = tmp_path / "new_folder" / "messages.db"
    initialize_database(path)
    assert path.exists()