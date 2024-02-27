import json
import os
import logging
from datetime import datetime

from lighteval.main_accelerate import main

from src.envs import RESULTS_REPO, CACHE_PATH
from src.backend.manage_requests import EvalRequest

logging.getLogger("openai").setLevel(logging.WARNING)

def run_evaluation(eval_request: EvalRequest, task_names: str, batch_size: int, local_dir: str, accelerator: str, region: str, vendor: str, instance_size: str, instance_type: str, limit=None):
    if limit:
        print("WARNING: --limit SHOULD ONLY BE USED FOR TESTING. REAL METRICS SHOULD NOT BE COMPUTED USING LIMIT.")

    results = main(
        endpoint_model_name=f"{eval_request.model}_{eval_request.precision}".lower(),
        accelerator= accelerator,
        vendor= vendor,
        region= region,
        instance_size= instance_size,
        instance_type= instance_type,
        max_samples= limit,
        job_id= str(datetime.now()),
        push_results_to_hub= True,
        save_details= True,
        push_details_to_hub= True,
        public_run= False,
        cache_dir= CACHE_PATH,
        results_org= RESULTS_REPO,
        output_dir= local_dir,
        override_batch_size= batch_size,
        custom_tasks= "custom_tasks.py",
        tasks= task_names
    )

    results["config"]["model_dtype"] = eval_request.precision
    results["config"]["model_name"] = eval_request.model
    results["config"]["model_sha"] = eval_request.revision

    dumped = json.dumps(results, indent=2)
    print(dumped)

    return results
