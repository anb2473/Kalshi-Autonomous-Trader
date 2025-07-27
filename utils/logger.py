import logging
import logging.handlers
import traceback
from typing import Optional

class LoggerConfig:
    """Configuration for the logger."""
    def __init__(
        self,
        log_format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        date_format: str = '%Y-%m-%d %H:%M:%S',
        max_bytes: int = 10 * 1024 * 1024,  # 10MB
        backup_count: int = 5,
        log_level: int = logging.INFO
    ):
        self.log_format = log_format
        self.date_format = date_format
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self.log_level = log_level

def setup_logger(
    name: str,
    log_config: Optional[LoggerConfig] = None
) -> logging.Logger:
    """
    Set up a logger with file and console handlers.
    
    Args:
        name: Name of the logger
        log_config: Optional LoggerConfig object to customize logging
    
    Returns:
        logging.Logger: Configured logger instance
    """
    if log_config is None:
        log_config = LoggerConfig()

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_config.log_level)

    # Create handlers with rotation
    info_handler = logging.handlers.RotatingFileHandler(
        'info.log',
        maxBytes=log_config.max_bytes,
        backupCount=log_config.backup_count
    )
    info_handler.setLevel(logging.INFO)

    error_handler = logging.handlers.RotatingFileHandler(
        'error.log',
        maxBytes=log_config.max_bytes,
        backupCount=log_config.backup_count
    )
    error_handler.setLevel(logging.ERROR)

    # Create formatter
    formatter = logging.Formatter(
        log_config.log_format,
        datefmt=log_config.date_format
    )

    # Set formatter for handlers
    info_handler.setFormatter(formatter)
    error_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(info_handler)
    logger.addHandler(error_handler)

    # Add console handler for development
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Add custom error handler that includes traceback
    class ErrorFilter(logging.Filter):
        def filter(self, record):
            if record.levelno >= logging.ERROR:
                record.msg = f"{record.getMessage()}\nTraceback:\n{traceback.format_exc()}"
            return True

    error_handler.addFilter(ErrorFilter())
    console_handler.addFilter(ErrorFilter())

    return logger
