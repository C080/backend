import sys
import logging
import subprocess
import gradio as gr
from apscheduler.schedulers.background import BackgroundScheduler

logging.basicConfig(level=logging.ERROR)

from src.logging import LOGGER, read_logs

sys.stdout = LOGGER
sys.stderr = LOGGER

#subprocess.run(["python", "scripts/fix_harness_import.py"])

def launch_backend():
    _ = subprocess.run(["python", "main_backend_lighteval.py"])

demo = gr.Blocks()
with demo:
    logs = gr.Code(interactive=False)
    demo.load(read_logs, None, logs, every=1)
    
scheduler = BackgroundScheduler()
scheduler.add_job(launch_backend, "interval", seconds=60) # will only allow one job to be run at the same time
scheduler.start()
demo.queue(default_concurrency_limit=40).launch()