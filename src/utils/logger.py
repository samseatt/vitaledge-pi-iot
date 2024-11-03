"""
logger.py
Adds structured logging across the application.
"""
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def log_info(message):
    logging.info(message)

def log_error(message):
    logging.error(message)
