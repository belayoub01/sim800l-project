import logging
import subprocess

logger = logging.getLogger("sim800l_project.sender")


def send_sms(number, message, command="/usr/bin/gammu-smsd-inject"):
    if not number or not message.strip():
        raise ValueError("Phone number and message are required")

    result = subprocess.run(
        [command, "TEXT", number, "-text", message],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )

    if result.returncode != 0:
        logger.error("SMS injection failed: %s", result.stderr.strip())
        raise RuntimeError(f"gammu-smsd-inject failed: {result.stderr.strip()}")

    logger.info("SMS queued for %s: %s", number, result.stdout.strip())
    return result.stdout.strip()
