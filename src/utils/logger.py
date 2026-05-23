import logging
import os
from datetime import datetime

def get_logger(name):

  log_dir = "logs"
  os.makedirs(log_dir, exist_ok=True)

  today = datetime.utcnow().strftime("%Y_%m_%d")
  log_file = f"{log_dir}/pipeline_{today}.log"

  logger = logging.getLogger(name)
  logger.setLevel(logging.DEBUG)

  if logger.handlers:
    return logger
  
  formatter = logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
  )

  file_handler = logging.FileHandler(log_file, encoding="utf-8")
  file_handler.setLevel(logging.DEBUG)
  file_handler.setFormatter(formatter)

  console_handler = logging.StreamHandler()
  console_handler.setLevel(logging.INFO)
  console_handler.setFormatter(formatter)

  logger.addHandler(file_handler)
  logger.addHandler(console_handler)

  return logger