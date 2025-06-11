import logging
import os
import sys
from enum import Enum

# Define a custom OFF level (higher than CRITICAL to disable all logging)
logging.OFF = 100
logging.addLevelName(logging.OFF, "OFF")

# Default logging level - DEBUG by default
DEFAULT_LEVEL = logging.OFF 

class LogLevel(Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL
    OFF = logging.OFF

# Configure the logger
def configure_logger(level=None):
    """Configure the root logger with the specified log level."""
    if level is None:
        # Check for environment variable to set log level
        env_level = os.environ.get("MINT_LOG_LEVEL", "").upper()
        if env_level == "DEBUG":
            level = LogLevel.DEBUG.value
        elif env_level == "INFO":
            level = LogLevel.INFO.value
        elif env_level == "WARNING":
            level = LogLevel.WARNING.value
        elif env_level == "ERROR":
            level = LogLevel.ERROR.value
        elif env_level == "CRITICAL":
            level = LogLevel.CRITICAL.value
        elif env_level == "OFF":
            level = LogLevel.OFF.value
        else:
            level = DEFAULT_LEVEL
    
    # Configure root logger
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

def get_logger(name):
    """Get a logger with the specified name."""
    return logging.getLogger(name)

# Initialize logger configuration when module is imported
configure_logger()