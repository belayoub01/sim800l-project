# Architecture

## Message flow (incoming)

1. The phone sends an SMS to the SIM.
2. SIM800L receives it and Gammu SMSD (talking over UART) writes it as a file in `/var/spool/gammu/inbox`.
3. `main.py` scans the inbox every `poll_interval` seconds using `process_inbox()`.
4. Each file is parsed (date and sender come from the filename, text from the content) and saved with `save_message()`.
5. The filename is stored in a `UNIQUE` column, so the same file is never saved twice.

Gammu inbox filename format: `IN<YYYYMMDD>_<HHMMSS>_<n>_<sender>_<n>.txt`

## Message flow (outgoing)

`send_sms(number, message)` calls `gammu-smsd-inject TEXT <number> -text <message>`, which queues the message in the Gammu outbox. Gammu then sends it through the modem. The sender is a library function and is not called by `main.py`.

## Files

| File | Responsibility |
|---|---|
| `src/main.py` | Loads settings, starts logging, polling loop with error handling |
| `src/sms_receiver.py` | Reads inbox files, validates names and content, masks numbers in logs |
| `src/sms_sender.py` | Queues outgoing SMS via `gammu-smsd-inject` (no shell, with timeout) |
| `src/message_handler.py` | SQLite initialization and `save_message()` |
| `src/logger_config.py` | Logging to a rotating file and to the console |

## Services

- `gammu-smsd.service`: modem communication.
- `sim800l-project.service`: the Python processor, starts after Gammu, restarts on failure.

## Known behavior

- `save_message()` uses `INSERT OR IGNORE`: it returns `False` both for duplicates and for rows violating a constraint, so rejected rows are skipped silently.
- Empty message files are skipped and logged as warnings.