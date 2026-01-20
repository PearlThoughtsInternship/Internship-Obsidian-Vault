import ast
import sys
from pathlib import Path
from collections import defaultdict
import json


# -------------------------
# File discovery
# -------------------------
def get_python_files(path: str):
    path = Path(path)

    if path.is_file() and path.suffix == ".py":
        return [path]

    if path.is_dir():
        return list(path.rglob("*.py"))

    return []


# -------------------------
# AST Analyzer
# -------------------------
class CallGraphAnalyzer(ast.NodeVisitor):
    def __init__(self, module_name: str):
        self.module = module_name
        self.class_stack = []
        self.function_stack = []
        self.call_graph = defaultdict(set)

    def visit_ClassDef(self, node):
        self.class_stack.append(node.name)
        self.generic_visit(node)
        self.class_stack.pop()

    def visit_FunctionDef(self, node):
        self.function_stack.append(node.name)

        caller = self.current_scope()
        self.call_graph.setdefault(caller, set())

        self.generic_visit(node)
        self.function_stack.pop()

    def visit_Call(self, node):
        caller = self.current_scope()
        callee = self.resolve_callee(node)

        if caller and callee:
            self.call_graph[caller].add(callee)

        self.generic_visit(node)

    def current_scope(self):
        if not self.function_stack:
            return None
        parts = [self.module] + self.class_stack + self.function_stack
        return ".".join(parts)

    def resolve_callee(self, node):
        if isinstance(node.func, ast.Name):
            return f"{self.module}.{node.func.id}"

        if isinstance(node.func, ast.Attribute):
            return f"{self.module}.{node.func.attr}"

        return None


# -------------------------
# Analyzer Runner
# -------------------------
def analyze_files(path):
    files = get_python_files(path)
    if not files:
        print("❌ No Python files found")
        return

    global_graph = defaultdict(set)

    for file in files:
        module_name = file.stem
        tree = ast.parse(file.read_text())

        analyzer = CallGraphAnalyzer(module_name)
        analyzer.visit(tree)

        for caller, callees in analyzer.call_graph.items():
            global_graph[caller].update(callees)

    print_call_graph(global_graph)
    save_call_graph(global_graph)


# -------------------------
# Output helpers
# -------------------------
def print_call_graph(call_graph):
    print("\n📊 Global Call Graph\n")
    for caller, callees in sorted(call_graph.items()):
        print(caller)
        for callee in sorted(callees):
            print(f"  └── {callee}")

    total_calls = sum(len(v) for v in call_graph.values())
    print(f"\n📊 Summary: {len(call_graph)} functions, {total_calls} calls\n")


def save_call_graph(call_graph, output_file="call_graph.json"):
    serializable_graph = {
        caller: sorted(list(callees))
        for caller, callees in call_graph.items()
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(serializable_graph, f, indent=2)

    print(f"💾 Call graph saved to {output_file}")


# -------------------------
# Entry point
# -------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyzer.py <file_or_directory>")
        sys.exit(1)

    analyze_files(sys.argv[1])





