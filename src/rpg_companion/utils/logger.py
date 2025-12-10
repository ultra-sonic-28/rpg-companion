# utils/logger.py
import logging
from pathlib import Path

from rpg_companion.config.config_manager import ConfigManager


def setup_logging(config: ConfigManager) -> None:
    log = config.logging()
    enabled = bool(log.get("enabled", True))
    level = log.get("level", "INFO")
    log_file = log.get("file", "./rpg-companion.log")
    mode = log.get("mode", "write")

    if not enabled:
        logging.disable(logging.CRITICAL)
        return

    # Normalise le chemin
    log_path = Path(log_file).expanduser().resolve()
    log_path.parent.mkdir(parents=True, exist_ok=True)

    file_mode = "w" if mode == "write" else "a"

    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        encoding="utf-8",
        handlers=[
            logging.FileHandler(log_path, mode=file_mode, encoding="utf-8"),
            logging.StreamHandler(),  # console
        ]
    )

    logger = logging.getLogger("rpg_companion")
    logger.info("Logging initialized")
