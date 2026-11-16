# Installation

## 1. System packages

```bash
sudo apt update
sudo apt install -y gammu gammu-smsd python3 python3-venv sqlite3 git
```

## 2. Enable the serial port

See [HARDWARE.md](HARDWARE.md). Reboot, then check:

```bash
ls -l /dev/serial0
gammu identify
```

## 3. Configure Gammu

Edit `/etc/gammu-smsdrc`. Example (adjust to your setup, leave the PIN out of any public copy):

```ini
[gammu]
port = /dev/serial0
connection = at

[smsd]
service = files
inboxpath = /var/spool/gammu/inbox/
outboxpath = /var/spool/gammu/outbox/
sentsmspath = /var/spool/gammu/sent/
errorsmspath = /var/spool/gammu/error/
logfile = syslog
debuglevel = 0
```

Enable and start:

```bash
sudo systemctl enable --now gammu-smsd
systemctl status gammu-smsd --no-pager
```

Send a test message:

```bash
sudo gammu-smsd-inject TEXT +213XXXXXXXXX -text "Test"
```

## 4. Get the project

```bash
git clone git@github.com:belayoub01/sim800l-project.git
cd sim800l-project
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp config/settings.example.json config/settings.json
```

Make sure your user can read the inbox:

```bash
ls -ld /var/spool/gammu/inbox
```

## 5. Run the tests

```bash
python3 -m pytest -v
```

## 6. Run manually

```bash
python src/main.py
```

## 7. Run as a service

Create `/etc/systemd/system/sim800l-project.service`:

```ini
[Unit]
Description=SIM800L SMS Processor
After=gammu-smsd.service
Wants=gammu-smsd.service

[Service]
Type=simple
User=fateh
WorkingDirectory=/home/fateh/sim800l-project
ExecStart=/home/fateh/sim800l-project/.venv/bin/python src/main.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

(Replace `fateh` and the paths with your own.)

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now sim800l-project
systemctl status sim800l-project --no-pager
```

## 8. Check it works

Send an SMS to the SIM, wait a few seconds, then:

```bash
tail -5 logs/app.log
sqlite3 data/messages.db "SELECT COUNT(*) FROM messages;"
```