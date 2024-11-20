import logging
import json
from datetime import datetime


class CustomFormatter(logging.Formatter):
    def format(self, record):
        record.asctime = datetime.utcnow().isoformat()
        if isinstance(record.msg, dict):
            record.msg = json.dumps(record.msg)
        return super().format(record)


def setup_logger():
    logger = logging.getLogger("stripe_service")
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    formatter = CustomFormatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


logger = setup_logger()
