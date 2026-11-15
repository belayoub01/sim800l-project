import json
import logging
from pathlib import Path


def setup_logger(settings_path="config/settings.json"):
    settings = json.loads(Path(settings_path).read_text(encoding="utf-8"))

    log_path = Path(settings["log_path"])
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )

    return logging.getLogger("sim800l_project")
