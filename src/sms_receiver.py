import logging
import re
from datetime import datetime
from pathlib import Path

from message_handler import save_message

logger = logging.getLogger("sim800l_project.receiver")

FILENAME_PATTERN = re.compile(
    r"^IN(?P<date>\d{8}_\d{6})_\d+_"
    r"(?P<sender>.+)_\d+\.txt$"
)


def mask_number(number):
    if len(number) <= 4:
        return "****"
    return number[:4] + "*" * (len(number) - 6) + number[-2:]


def process_inbox(inbox_path, database_path):
    inbox = Path(inbox_path)
    if not inbox.is_dir():
        raise FileNotFoundError(f"Inbox directory not found: {inbox}")

    processed = 0

    for file_path in sorted(inbox.glob("IN*.txt")):
        match = FILENAME_PATTERN.match(file_path.name)

        if not match:
            logger.warning("Unrecognized message filename: %s", file_path.name)
            continue

        try:
            received_at = datetime.strptime(
                match.group("date"), "%Y%m%d_%H%M%S"
            ).isoformat(sep=" ")

            sender = match.group("sender")
            message = file_path.read_text(encoding="utf-8").strip()

            if not message:
                logger.warning("Empty message file: %s", file_path.name)
                continue

            inserted = save_message(
                database_path, sender, message, received_at, file_path.name
            )

            if inserted:
                processed += 1
                logger.info(
                    "Saved SMS from %s at %s", mask_number(sender), received_at
                )

        except (OSError, UnicodeError, ValueError):
            logger.exception("Could not read %s", file_path.name)

    return processed