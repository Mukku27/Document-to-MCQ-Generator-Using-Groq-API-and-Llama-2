import logging
import os
from datetime import datetime

# Generate a log file name with the current timestamp
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Create a directory for logs if it doesn't exist
log_path = os.path.join(os.getcwd(), 'logs')
os.makedirs(log_path, exist_ok=True)

# Full path for the log file
LOG_FILEPATH = os.path.join(log_path, LOG_FILE)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    filename=LOG_FILEPATH,
    format='[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s'
)