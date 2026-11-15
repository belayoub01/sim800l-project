# SIM800L SMS Gateway

## Project Overview

A Python-based SMS gateway running on Raspberry Pi 4.
It uses a SIM800L GSM module, Gammu SMSD, and SQLite.

The system receives SMS messages, processes them with Python,
and stores message records in an SQLite database.

## Hardware

- Raspberry Pi 4 Model B
- SIM800L HW-748 GSM module
- UART serial connection
- Suitable power supply for SIM800L

## Software

- Raspberry Pi OS / Linux
- Python
- Gammu and Gammu SMSD
- SQLite
- systemd

## Project Structure

- config/settings.json: local configuration
- data/messages.db: SQLite database
- logs/app.log: application log
- src/main.py: application entry point
- src/sms_receiver.py: SMS receiving logic
- src/sms_sender.py: SMS sending logic
- src/message_handler.py: message processing
- src/logger_config.py: logging configuration
- tests/: automated tests
- backups/: project backup archives

## Database

The database is stored at data/messages.db.
The messages table stores message details, including sender,
message text, received time, source file, and processing time.

Check database integrity with:

    sqlite3 data/messages.db "PRAGMA integrity_check;"

## Services

The project uses these systemd services:

- gammu-smsd.service
- sim800l-project.service

Check service status with:

    sudo systemctl status gammu-smsd.service --no-pager
    sudo systemctl status sim800l-project.service --no-pager

View recent application logs with:

    tail -n 50 logs/app.log

## Testing

Activate the virtual environment:

    source .venv/bin/activate

Run the existing tests:

    python -m pytest -v

## Backups

Create a compressed backup from the project directory:

    tar --exclude='./.venv' --exclude='./backups' --exclude='./.git' -czf "backups/sim800l-project-$(date +%F-%H%M%S).tar.gz" .

Check an archive with:

    tar -tzf backups/ARCHIVE_NAME.tar.gz

Keep a second backup on separate storage.
Backups may contain private messages and configuration data.

## Security

Do not publish private settings, phone numbers, message contents,
database files, or logs in a public repository.

## Current Status

The application has successfully saved multiple test SMS messages
to SQLite. The application log recorded the saved messages.

A backup archive was created and extracted into a separate
directory. SQLite integrity checking returned "ok".

Further work includes reviewing duplicate-message handling,
documenting the exact local configuration, and improving tests.
