import json
from typing import Dict, List


def detect_cycles(graph: Dict[str, List[str]]):
    visited = set()
    stack = []
    cycles = []

    def dfs(node):
        if node in stack:
            idx = stack.index(node)
            cycles.append(stack[idx:] + [node])
            return

        if node in visited:
            return

        visited.add(node)
        stack.append(node)

        for neighbor in graph.get(node, []):
            dfs(neighbor)

        stack.pop()

    for node in graph:
        dfs(node)

    return cycles


def load_call_graph(path="call_graph.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)["call_graph"]


if __name__ == "__main__":
    graph = load_call_graph()
    cycles = detect_cycles(graph)

    if not cycles:
        print("✅ No cycles detected")
    else:
        print("🔁 Detected Cycles\n")
        for i, cycle in enumerate(cycles, 1):
            print(f"Cycle {i}:")
            print("  " + " → ".join(cycle))

    # 🔥 NEW: save cycles for visualization
    with open("cycles.json", "w", encoding="utf-8") as f:
        json.dump(cycles, f, indent=2)










