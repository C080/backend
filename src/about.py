from dataclasses import dataclass
from enum import Enum

@dataclass
class Task:
    benchmark: str
    metric: str
    col_name: str


# Change for your tasks here
# ---------------------------------------------------
class Tasks(Enum):
    # task_key in the json file, metric_key in the json file, name to display in the leaderboard 
    task0 = Task("anli_r1", "acc", "ANLI")
    task1 = Task("logiqa", "acc_norm", "LogiQA")

NUM_FEWSHOT = 0 # Change with your few shot

TASKS_HARNESS = [task.value.benchmark for task in Tasks]
# ---------------------------------------------------

TASKS_LIGHTEVAL = "lighteval|anli:r1|0|0,lighteval|logiqa|0|0" 
#custom|myothertask|0|0