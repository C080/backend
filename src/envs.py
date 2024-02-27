import os

from huggingface_hub import HfApi

# Info to change for your repository
# ----------------------------------
TOKEN = os.environ.get("TOKEN") # A read/write token for your org

OWNER = "demo-leaderboard-backend" # Change to your org - don't forget to create a results and request file

# For harness evaluations
DEVICE = "cpu" # "cuda:0" if you add compute, for harness evaluations
LIMIT = 20 # !!!! Should be None for actual evaluations!!!

# For lighteval evaluations
ACCELERATOR = "gpu"
REGION = "us-east-1"
VENDOR = "aws"
# ----------------------------------

REPO_ID = f"{OWNER}/leaderboard-backend"
QUEUE_REPO = f"{OWNER}/requests"
RESULTS_REPO = f"{OWNER}/results"

# If you setup a cache later, just change HF_HOME
CACHE_PATH=os.getenv("HF_HOME", ".")

# Local caches
EVAL_REQUESTS_PATH = os.path.join(CACHE_PATH, "eval-queue")
EVAL_RESULTS_PATH = os.path.join(CACHE_PATH, "eval-results")
EVAL_REQUESTS_PATH_BACKEND = os.path.join(CACHE_PATH, "eval-queue-bk")
EVAL_RESULTS_PATH_BACKEND = os.path.join(CACHE_PATH, "eval-results-bk")

API = HfApi(token=TOKEN)

