from loguru import logger

def setup_logger(log_file_path):
    """
    Set up a logger to log messages to a file and the console.
    Uses the loguru library for advanced logging features.
    """
    logger.add(log_file_path, rotation="1 MB", compression="gz")
    logger.add(sys.stderr, level="INFO")
    return logger