WEIGHTS = {
    "battery" : 0.20,
    "cpu" : 0.25,
    "communication" : 0.15,
    "reliability" : 0.20,
    "storage" : 0.10,
    "visibility" : 0.10,
}

def clamp(value, low = 0.0, high = 1.0):
    return max(low, min(value, high))

def rule_score(task, node):
    battery_score = clamp(node.battery / 100.0)

    cpu_headroom = (node.available_cpu - task.required_cpu) / max(1.0, 100.0 - task.required_cpu)
    cpu_score = clamp(cpu_headroom)

    communication_score = clamp(node.communication_quality)
    reliability_score = clamp(node.reliability)

    storage_headroom = (node.storage - task.storage_requirement) / max(1.0, node.storage)
    storage_score = clamp(storage_headroom)

    visibility_score = clamp(node.visibility_window / max(task.expected_duration, 1.0), 0.0, 1.0)

    return (
        WEIGHTS["battery"] * battery_score
        + WEIGHTS["cpu"] * cpu_score
        + WEIGHTS["communication"] * communication_score
        + WEIGHTS["reliability"] * reliability_score
        + WEIGHTS["storage"] * storage_score
        + WEIGHTS["visibility"] * visibility_score
    )

def rank_candidates(task, nodes):
    ranked = [
        {
            "node": node,
            "rule_score": rule_score(task, node)
        }
        for node in nodes
    ]

    return sorted(ranked, key=lambda item: item["rule_score"],reverse=True)