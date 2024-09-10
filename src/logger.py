# A logging is crucial for tracking events that happens when application run which helps in debugging and monitoring the application behavior.

import logging
import os
from datetime import datetime

log_file = f"{datetime.now().strftime('%Y-%m-%d')}.log"
logs_path = os.path.join(os.getcwd(), 'logs', log_file)


os.makedirs(logs_path,exist_ok=True)

Log_file_path = os.path.join(logs_path, log_file)

logging.basicConfig(
    filename=Log_file_path,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)