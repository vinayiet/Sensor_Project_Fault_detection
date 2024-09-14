import logging
import os
from datetime import datetime

# Log file in a directory outside of OneDrive to avoid permission issues
logs_path = os.path.join('C:\\', 'logs')  
log_file = f"{datetime.now().strftime('%Y-%m-%d')}.log"

# Ensure the directory exists
os.makedirs(logs_path, exist_ok=True)

# Set the full log file path
log_file_path = os.path.join(logs_path, log_file)

# Configure the logger
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
