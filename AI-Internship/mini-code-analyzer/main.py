import sys
import subprocess
from pathlib import Path
import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Mini Code Analyzer — Architecture Intelligence CLI"
    )

    parser.add_argument("path", help="File or directory to analyze")

    parser.add_argument("--cycles", action="store_true", help="Detect cycles")
    parser.add_argument("--risk", action="store_true", help="Architecture risk analysis")
    parser.add_argument("--gate", action="store_true", help="Architecture quality gate")
    parser.add_argument("--diagrams", action="store_true", help="Generate Mermaid diagrams")
    parser.add_argument("--llm", action="store_true", help="Generate LLM context")
    parser.add_argument("--all", action="store_true", help="Run full pipeline")

    return parser.parse_args()


def resolve_flags(args):
    if args.all:
        return {
            "cycles": True,
            "risk": True,
            "gate": True,
            "diagrams": True,
            "llm": True,
        }

    return {
        "cycles": args.cycles,
        "risk": args.risk,
        "gate": args.gate,
        "diagrams": args.diagrams,
        "llm": args.llm,
    }


def run(cmd, label):
    print(f"▶ {label}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"❌ Failed: {label}")
        sys.exit(1)
    print(f"✔ Done: {label}\n")


def main():
    args = parse_args()
    flags = resolve_flags(args)

    if not Path(args.path).exists():
        print(f"❌ Path not found: {args.path}")
        sys.exit(1)

    if not any(flags.values()):
        print("ℹ️ No flags provided — running full analysis (--all)\n")
        flags = {k: True for k in flags}

    # 1️⃣ Static analysis (always)
    run(
        f"python analyzer.py {args.path}",
        "Static analysis (call graph + import graph)"
    )

    # 2️⃣ Optional stages
    if flags["cycles"]:
        run("python cycle_detector.py", "Cycle detection")

    if flags["risk"]:
        run("python architecture_insights.py", "Architecture risk analysis")

    if flags["gate"]:
        run("python architecture_gate.py", "Architecture quality gate")

    if flags["diagrams"]:
        run("python graph_exporter.py", "Mermaid diagram generation")

    if flags["llm"]:
        run("python llm_context_builder.py", "LLM context generation")

    print("🎉 Analysis complete")
    print("Artifacts generated:")
    print("  - call_graph.json")
    print("  - cycles.json")
    print("  - architecture_insights.json")
    print("  - diagrams/*.mmd")
    print("  - llm_context.txt")


if __name__ == "__main__":
    main()


