# SIM800L SMS Gateway

A small SMS gateway built on a **Raspberry Pi 4** and a **SIM800L** GSM modem. Incoming messages are received through **Gammu SMSD**, processed by a **Python** service, and stored in **SQLite**. The Pi talks to the mobile network directly, so no smartphone is needed.

## Features

- Receive SMS through Gammu SMSD and store them in a local SQLite database
- Duplicate protection (one row per Gammu inbox file)
- Send SMS through `gammu-smsd-inject`
- Phone numbers masked in logs, rotating log file
- Runs as a `systemd` service and restarts automatically after a crash or reboot
- Automated tests with `pytest`

## How it works

```
Phone <-> Mobile network <-> SIM800L <-UART-> Raspberry Pi
                                               |
                                      Gammu SMSD (inbox files)
                                               |
                                  Python service (src/main.py)
                                               |
                                      SQLite (data/messages.db)
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for details.

## Requirements

- Raspberry Pi 4 with Raspberry Pi OS (Linux)
- SIM800L module with a **stable power supply** (see [docs/HARDWARE.md](docs/HARDWARE.md))
- Active SIM card
- Gammu and gammu-smsd, Python 3, SQLite

## Quick start

```bash
git clone git@github.com:belayoub01/sim800l-project.git
cd sim800l-project
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp config/settings.example.json config/settings.json
python src/main.py
```

Full setup (Gammu, systemd): [docs/INSTALLATION.md](docs/INSTALLATION.md)

## Configuration

`config/settings.json` (a template is provided in `config/settings.example.json`):

| Key | Meaning |
|---|---|
| `inbox_path` | Gammu SMSD inbox directory (default `/var/spool/gammu/inbox`) |
| `database_path` | SQLite file (relative paths are resolved from the project root) |
| `log_path` | Application log file |
| `poll_interval` | Seconds between inbox scans |
| `sender_command` | Path to `gammu-smsd-inject` |

## Sending an SMS

```python
from sms_sender import send_sms
send_sms("+213XXXXXXXXX", "Hello from Raspberry Pi")
```

## Running the tests

```bash
python3 -m pytest -v
```

## Project structure

```
src/        main.py, sms_receiver.py, sms_sender.py, message_handler.py, logger_config.py
tests/      pytest tests
config/     settings.example.json
data/       SQLite database (not committed)
docs/       hardware, installation, architecture, database, troubleshooting
```

## Privacy and security

- `data/*.db`, `config/settings.json`, `logs/` and `.venv/` are git-ignored.
- Never commit tokens, PINs or real message content.

## Limitations

- No web interface or API yet.
- Reliability over long periods has been tested only briefly (reboot and crash recovery).

## License

See [LICENSE](LICENSE).