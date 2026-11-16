# Database

SQLite file: `data/messages.db` (not committed to Git).

## Table `messages`

| Column | Type | Notes |
|---|---|---|
| `id` | INTEGER | Primary key, autoincrement |
| `sender` | TEXT NOT NULL | Sender phone number |
| `message` | TEXT NOT NULL | Message text (UTF-8, Arabic supported) |
| `received_at` | TEXT NOT NULL | Reception time taken from the Gammu filename |
| `source_file` | TEXT NOT NULL UNIQUE | Gammu inbox filename, used to prevent duplicates |
| `processed_at` | TEXT | Defaults to `CURRENT_TIMESTAMP` |

## Useful queries

```bash
sqlite3 data/messages.db "SELECT COUNT(*) FROM messages;"
sqlite3 data/messages.db "SELECT id, received_at, substr(message,1,40) FROM messages ORDER BY id DESC LIMIT 5;"
sqlite3 data/messages.db "PRAGMA integrity_check;"
```

## Backup

```bash
sqlite3 data/messages.db ".backup data/messages-backup.db"
```

Messages contain personal data. Keep backups out of the repository.