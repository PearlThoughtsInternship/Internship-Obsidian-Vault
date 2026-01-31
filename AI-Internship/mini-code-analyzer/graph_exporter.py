import json
from pathlib import Path

CALL_GRAPH_FILE = "call_graph.json"
CYCLES_FILE = "cycles.json"
OUTPUT_DIR = Path("diagrams")


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_cycle_edges(cycles):
    """
    Convert cycles into a set of (src, dst) edges
    """
    cycle_edges = set()
    for cycle in cycles:
        for i in range(len(cycle) - 1):
            cycle_edges.add((cycle[i], cycle[i + 1]))
    return cycle_edges


def group_by_module(nodes):
    modules = {}
    for node in nodes:
        module = node.split(".")[0]
        modules.setdefault(module, []).append(node)
    return modules


def export_call_graph(call_graph, cycle_edges):
    lines = ["graph TD"]

    all_nodes = set(call_graph.keys())
    for callees in call_graph.values():
        all_nodes.update(callees)

    # ---- Subgraphs (module grouping) ----
    modules = group_by_module(all_nodes)
    for module, nodes in modules.items():
        lines.append(f"  subgraph {module}")
        for node in nodes:
            lines.append(f'    "{node}"')
        lines.append("  end")

    # ---- Edges ----
    for caller, callees in call_graph.items():
        for callee in callees:
            if (caller, callee) in cycle_edges:
                lines.append(
                    f'  "{caller}" -->|cycle| "{callee}":::cycleEdge'
                )
            else:
                lines.append(f'  "{caller}" --> "{callee}"')

    # ---- Styling ----
    lines.append("  classDef cycleEdge stroke:red,stroke-width:3px;")

    return "\n".join(lines)


def export_import_graph(import_graph):
    lines = ["graph TD"]
    for module, deps in import_graph.items():
        for dep in deps:
            lines.append(f'  "{module}" --> "{dep}"')
    return "\n".join(lines)


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    data = load_json(CALL_GRAPH_FILE)
    call_graph = data["call_graph"]
    import_graph = data.get("import_graph", {})

    cycles = load_json(CYCLES_FILE)
    cycle_edges = extract_cycle_edges(cycles)

    # ---- Call graph ----
    call_graph_mmd = export_call_graph(call_graph, cycle_edges)
    (OUTPUT_DIR / "call_graph.mmd").write_text(call_graph_mmd)

    # ---- Import graph ----
    if import_graph:
        import_graph_mmd = export_import_graph(import_graph)
        (OUTPUT_DIR / "import_graph.mmd").write_text(import_graph_mmd)

    print("📊 Mermaid diagrams generated (cycle-highlighted)")


if __name__ == "__main__":
    main()





