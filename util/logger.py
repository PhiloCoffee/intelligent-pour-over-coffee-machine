# File: utilities/logger.py
import logging
import os
from datetime import datetime

def setup_logger(name):
    """Setup and return a logger with the given name."""
    # Create logger
    logger = logging.getLogger(name)
    if not logger.handlers:  # Check if handlers are already set (to avoid duplication)
        logger.setLevel(logging.DEBUG)  # Set the log level to DEBUG
        
        # Create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Add formatter to ch
        ch.setFormatter(formatter)
        
        # Add ch to logger
        logger.addHandler(ch)

    return logger

def setup_file_logger(logger, name):
    """Setup a file logger with a timestamped log file."""
    # Create a new folder with current date and time
    log_dir = "logs"
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_folder = os.path.join(log_dir, current_time)
    os.makedirs(log_folder, exist_ok=True)
    
    # Create file handler and set level to debug
    log_file = os.path.join(log_folder, f"{name}.log")
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Add formatter to fh
    fh.setFormatter(formatter)
    
    # Add fh to logger
    logger.addHandler(fh)
