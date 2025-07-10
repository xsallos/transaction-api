__all__ = ("logger",)

import json
import logging
from datetime import datetime


class CustomFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "location": f"{record.module}:{record.lineno}",
        }

        if hasattr(record, "extra") and isinstance(record.extra, dict):
            log_record.update(record.extra)

        return json.dumps(log_record)


logger = logging.getLogger("eventLogger")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setFormatter(CustomFormatter())

logger.addHandler(handler)
