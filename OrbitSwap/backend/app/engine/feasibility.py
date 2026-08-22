from dataclasses import dataclass
from typing import List, Tuple

BATTERY_RESERVE = 20.0
MIN_COMMUNICATION = 0.35
MIN_RELIABILITY = 0.60
TOP_K_DEFAULT = 3

@dataclass
class FeasibilityResult:
    feasible: bool
    reason: str = ""

def check_feasibility(task, node) -> FeasibilityResult:
    if node.battery < BATTERY_RESERVE:
        return FeasibilityResult(False,f"battery {node.battery}% is below reserve {BATTERY_RESERVE:.1f}%")

    if node.available_cpu < task.required_cpu:
        return FeasibilityResult(False,f"available CPU {node.available_cpu:.1f}% is below task requirement")

    if node.storage < task.storage_requirement:
        return FeasibilityResult(False,"Insufficient storage capacity")

    if node.communication_quality < MIN_COMMUNICATION:
        return FeasibilityResult(False,"Communication quality is below threshold")

    if node.reliability < MIN_RELIABILITY:
        return FeasibilityResult(False,"Reliability is below threshold")

    if node.visibility_window < task.expected_duration:
        return FeasibilityResult(False,"Visibility window is shorter than expected execution duration")

    return FeasibilityResult(True,"Feasible")

def filter_feasible(task, nodes):
    feasible = []
    rejected = []

    for node in nodes:
        result = check_feasibility(task, node)
        if result.feasible:
            feasible.append(node)
        else:
            rejected.append({"satellite_id": node.satellite_id, "reason": result.reason})

    return feasible, rejected

