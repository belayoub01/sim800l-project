import json
import logging
import time
from pathlib import Path

from logger_config import setup_logger
from message_handler import initialize_database
from sms_receiver import process_inbox


def main():
    settings_path = Path(__file__).resolve().parent.parent / "config/settings.json"
    settings = json.loads(settings_path.read_text(encoding="utf-8"))

    logger = setup_logger(str(settings_path))
    database_path = Path(settings["database_path"])

    if not database_path.is_absolute():
        database_path = settings_path.parent.parent / database_path

    initialize_database(str(database_path))
    logger.info("SMS project started")

    while True:
        try:
            count = process_inbox(settings["inbox_path"], str(database_path))
            if count:
                logger.info("New messages saved: %d", count)

        except Exception:
            logger.exception("Inbox processing failed")

        time.sleep(max(1, int(settings["poll_interval"])))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.getLogger("sim800l_project").info("Program stopped")
