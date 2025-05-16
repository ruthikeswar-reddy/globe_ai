import logging
import os
import sys
from dotenv import load_dotenv

load_dotenv()

LOGGING_STR = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
if os.getenv("DEVELOPMENT") == "True":
    LOG_DIR = "./logs"
    log_filepath = os.path.join(LOG_DIR, "running_logs.log")
    os.makedirs(LOG_DIR, exist_ok=True)
    handlers = [
            logging.FileHandler(log_filepath),
            logging.StreamHandler(sys.stdout),
        ]
else: 
    handlers = [
            logging.StreamHandler(sys.stdout),
        ]

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

if LOG_LEVEL == 'DEBUG':
    logging.basicConfig(
        level=logging.DEBUG,
        format=LOGGING_STR,
        handlers=handlers,
    )
else:
    logging.basicConfig(
        level=logging.INFO,
        format=LOGGING_STR,
        handlers=handlers,
    )

logger = logging.getLogger("chatbot_service")