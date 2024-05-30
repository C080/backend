import json
import os
import logging
from datetime import datetime

from lm_eval import tasks, evaluator, utils

from src.envs import RESULTS_REPO, API
from src.backend.manage_requests import EvalRequest
from src.logging import setup_logger

logging.getLogger("openai").setLevel(logging.WARNING)
logger = setup_logger(__name__)

def run_evaluation(eval_request: EvalRequest, task_names: list, num_fewshot: int, batch_size: int, device: str, local_dir: str, results_repo: str, no_cache: bool =True, limit: int =None):
    """Runs one evaluation for the current evaluation request file, then pushes the results to the hub.

    Args:
        eval_request (EvalRequest): Input evaluation request file representation
        task_names (list): Tasks to launch
        num_fewshot (int): Number of few shots to use
        batch_size (int): Selected batch size
        device (str): "cpu" or "gpu:0", depending on what you assigned to the space
        local_dir (str): Where to save the results locally
        results_repo (str): To which repository to upload the results
        no_cache (bool, optional): Whether to use a cache or not.
        limit (int, optional): Whether to use a number of samples only for the evaluation - only for debugging

    Returns:
        _type_: _description_
    """
    if limit:
        logger.info(
            "WARNING: --limit SHOULD ONLY BE USED FOR TESTING. REAL METRICS SHOULD NOT BE COMPUTED USING LIMIT."
        )

    #task_names = utils.pattern_match(task_names, tasks.ALL_TASKS)

    logger.info(f"Selected Tasks: {task_names}")

    results_1 = evaluator.simple_evaluate(
        model= 'huggingface', #"hf-causal-experimental", # "hf-causal"
        model_args=eval_request.get_model_args()+",trust_remote_code=True",
        tasks=task_names[0:2],
        num_fewshot=num_fewshot,
        batch_size=batch_size,
        device=device,
        # no_cache=no_cache,
        limit=limit,
        write_out=False,
        #output_base_path="logs"
    )

    results_2 = evaluator.simple_evaluate(
        model= 'huggingface', #"hf-causal-experimental", # "hf-causal"
        model_args=eval_request.get_model_args()+",trust_remote_code=True",
        tasks=task_names[2],
        num_fewshot=5,
        # batch_size=batch_size,
        device=device,
        # no_cache=no_cache,
        limit=limit,
        write_out=False,
        #output_base_path="logs"
    )

    results_1["config"]["model_dtype"] = eval_request.precision
    results_1["config"]["model_name"] = eval_request.model
    results_1["config"]["model_sha"] = eval_request.revision

    # Prepare the results in the desired JSON structure
    formatted_results = {
        "config": {
            "model_dtype": eval_request.precision,
            "model_name": eval_request.model,
            "model_sha": eval_request.revision
        },
        "results": {
            "mmlu_it": {
                "acc": results_2['results'].get('m_mmlu_it', {}).get('acc,none')
            },
            "hellaswag_it": {
                "acc_norm": results_1['results'].get('hellaswag_it', {}).get('acc_norm,none')
            },
            "arc_it": {
                "acc_norm": results_1['results'].get('arc_it', {}).get('acc_norm,none')
            }
        },
        "versions": None  # Assuming version detail is not provided
    }
    dump = json.dumps(formatted_results, indent=2)
    logger.info(dump)

    output_path = os.path.join(local_dir, *eval_request.model.split("/"), f"results_{datetime.now()}.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write(dump)

    # logger.info(evaluator.make_table(results))

    API.upload_file(
        path_or_fileobj=output_path,
        path_in_repo=f"{eval_request.model}.json",
        repo_id=results_repo,
        repo_type="dataset",
    )

    return dump #results
