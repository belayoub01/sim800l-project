import sqlite3

from message_handler import initialize_database
from sms_receiver import mask_number, process_inbox


def count_rows(db):
    with sqlite3.connect(db) as conn:
        return conn.execute("SELECT COUNT(*) FROM messages").fetchone()[0]


def test_process_inbox_saves_valid_file(tmp_path):
    inbox = tmp_path / "inbox"
    inbox.mkdir()
    db = str(tmp_path / "messages.db")
    initialize_database(db)

    (inbox / "IN20261115_120000_00_+213600000000_00.txt").write_text(
        "hello", encoding="utf-8"
    )

    assert process_inbox(str(inbox), db) == 1
    assert process_inbox(str(inbox), db) == 0  # لا تكرار
    assert count_rows(db) == 1


def test_process_inbox_skips_empty_and_bad_names(tmp_path):
    inbox = tmp_path / "inbox"
    inbox.mkdir()
    db = str(tmp_path / "messages.db")
    initialize_database(db)

    (inbox / "IN20261115_120000_00_+213600000000_00.txt").write_text("  ")
    (inbox / "INbadname.txt").write_text("x")

    assert process_inbox(str(inbox), db) == 0
    assert count_rows(db) == 0


def test_missing_inbox_raises(tmp_path):
    import pytest
    with pytest.raises(FileNotFoundError):
        process_inbox(str(tmp_path / "nope"), str(tmp_path / "x.db"))


def test_mask_number():
    assert mask_number("+213600000000") == "+213*******00"
    assert mask_number("123") == "****"