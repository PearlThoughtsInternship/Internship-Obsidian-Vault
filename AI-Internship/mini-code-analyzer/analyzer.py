import ast
import sys
import json
from pathlib import Path
from collections import defaultdict


# -------------------------
# File discovery
# -------------------------
def get_python_files(path):
    path = Path(path)

    if path.is_file() and path.suffix == ".py":
        return [path]

    if path.is_dir():
        return list(path.rglob("*.py"))

    return []


# -------------------------
# AST Analyzer
# -------------------------
class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self, module_name):
        self.module = module_name

        self.class_stack = []
        self.function_stack = []

        self.call_graph = defaultdict(set)
        self.import_graph = defaultdict(set)

        # NEW: symbol → module mapping
        self.import_aliases = {}

    # ---- Imports ----
    def visit_Import(self, node):
        for alias in node.names:
            name = alias.asname or alias.name
            self.import_aliases[name] = alias.name
            self.import_graph[self.module].add(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if not node.module:
            return

        for alias in node.names:
            name = alias.asname or alias.name
            self.import_aliases[name] = f"{node.module}.{alias.name}"
        self.import_graph[self.module].add(node.module)

        self.generic_visit(node)

    # ---- Class ----
    def visit_ClassDef(self, node):
        self.class_stack.append(node.name)
        self.generic_visit(node)
        self.class_stack.pop()

    # ---- Function ----
    def visit_FunctionDef(self, node):
        self.function_stack.append(node.name)
        self.call_graph.setdefault(self.current_scope(), set())
        self.generic_visit(node)
        self.function_stack.pop()

    # ---- Calls ----
    def visit_Call(self, node):
        caller = self.current_scope()
        callee = self.resolve_callee(node)

        if caller and callee:
            self.call_graph[caller].add(callee)

        self.generic_visit(node)

    # ---- Helpers ----
    def current_scope(self):
        if not self.function_stack:
            return None

        return ".".join([self.module] + self.class_stack + self.function_stack)

    def resolve_callee(self, node):
        # func()
        if isinstance(node.func, ast.Name):
            name = node.func.id

            # imported symbol
            if name in self.import_aliases:
                return self.import_aliases[name]

            return f"{self.module}.{name}"

        # obj.func()
        if isinstance(node.func, ast.Attribute):
            return f"{self.module}.{node.func.attr}"

        return None


# -------------------------
# Runner
# -------------------------
def analyze(path):
    files = get_python_files(path)

    global_calls = defaultdict(set)
    global_imports = defaultdict(set)

    for file in files:
        tree = ast.parse(file.read_text(encoding="utf-8"))
        analyzer = CodeAnalyzer(file.stem)
        analyzer.visit(tree)

        for k, v in analyzer.call_graph.items():
            global_calls[k].update(v)

        for k, v in analyzer.import_graph.items():
            global_imports[k].update(v)

    output = {
        "call_graph": {k: sorted(v) for k, v in global_calls.items()},
        "import_graph": {k: sorted(v) for k, v in global_imports.items()},
    }

    with open("call_graph.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print("💾 call_graph.json generated")


# -------------------------
# Entry point
# -------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyzer.py <file_or_directory>")
        sys.exit(1)

    analyze(sys.argv[1])








