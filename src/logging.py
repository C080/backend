import sys
from src.envs import API

class Logger:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "a+")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        
    def flush(self):
        self.terminal.flush()
        self.log.flush()
        
    def isatty(self):
        return False    

def read_logs():
    sys.stdout.flush()
    #API.upload_file(
    #    path_or_fileobj="output.log",
    #    path_in_repo="demo-backend.log",
    #    repo_id="demo-leaderboard-backend/logs",
    #    repo_type="dataset",
    #)

    with open("output.log", "r") as f:
        return f.read()

LOGGER =  Logger("output.log")
