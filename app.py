import logging
import sys

import gradio as gr
from main_backend_lighteval import run_auto_eval
from src.display.log_visualizer import log_file_to_html_string
from src.display.css_html_js import dark_mode_gradio_js
from src.envs import REFRESH_RATE

logging.basicConfig(level=logging.INFO)


intro_md = f"""
# Intro
This is just a visual for the auto evaluator. Note that the lines of the log visual are reversed.
# Logs
"""

with gr.Blocks(js=dark_mode_gradio_js) as demo:
    with gr.Tab("Application"):
        gr.Markdown(intro_md)
        dummy = gr.Markdown(run_auto_eval, every=REFRESH_RATE, visible=False)
        output = gr.HTML(log_file_to_html_string, every=10)

if __name__ == '__main__':
    demo.queue(default_concurrency_limit=40).launch(server_name="0.0.0.0", show_error=True, server_port=7860)