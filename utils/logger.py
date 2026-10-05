"""Small rotating project log stored locally under logs/."""
import logging
import json
from logging.handlers import RotatingFileHandler
from pathlib import Path

class JsonLineFormatter(logging.Formatter):
    def format(self, record):
        payload = {"timestamp": self.formatTime(record), "level": record.levelname, "logger": record.name, "message": record.getMessage()}
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)

def get_logger(name="teleguard"):
    logger=logging.getLogger(name)
    if not logger.handlers:
        folder=Path(__file__).resolve().parents[1]/"logs";folder.mkdir(exist_ok=True)
        handler=RotatingFileHandler(folder/"system.log",maxBytes=500_000,backupCount=2,encoding="utf-8")
        handler.setFormatter(JsonLineFormatter())
        logger.addHandler(handler);logger.setLevel(logging.INFO)
    return logger
