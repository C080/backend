import sys
from pathlib import Path

proj_dir = Path(__file__).parents[1]

log_file = proj_dir/"output.log"


import logging


def setup_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create a file handler to write logs to a file
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

# class Logger:
#     def __init__(self):
#         self.terminal = sys.stdout
#         self.log = open(log_file, "a+")
#
#     def write(self, message):
#         self.terminal.write(message)
#         self.log.write(message)
#
#     def flush(self):
#         self.terminal.flush()
#         self.log.flush()
#
#     def isatty(self):
#         return False
#
# def read_logs():
#     sys.stdout.flush()
#     #API.upload_file(
#     #    path_or_fileobj="output.log",
#     #    path_in_repo="demo-backend.log",
#     #    repo_id="demo-leaderboard-backend/logs",
#     #    repo_type="dataset",
#     #)
#
#     with open(log_file, "r") as f:
#         return f.read()
#
# LOGGER =  Logger()
