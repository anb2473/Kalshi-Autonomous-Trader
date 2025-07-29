# Logging System Overview

## Quick Reference

### Log Files

- `info.log`: Contains all INFO level logs and above
- `error.log`: Contains ERROR level logs and above
- Both files rotate at 10MB with 5 backups

### Log Format

```python
%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

### Usage

```python
from utils.logger import setup_logger

logger = setup_logger(__name__)

# Example usage
logger.info("This is an info message")
logger.error("This is an error message")
```

## Key Features

1. **File Rotation**
   - 10MB max size per file
   - 5 backup files kept
   - Automatic rotation

2. **Log Levels**
   - INFO: Regular operation messages
   - ERROR: Error conditions
   - Includes traceback for errors

3. **Configuration**

```python
# Custom configuration
config = LoggerConfig(
    log_level=logging.DEBUG,
    max_bytes=10 * 1024 * 1024,
    backup_count=5
)
logger = setup_logger(__name__, config)
```

## Error Handling

- Includes full traceback in error logs
- Maintains separate error file
- Proper exception handling
