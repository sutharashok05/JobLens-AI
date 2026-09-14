from pathlib import Path

ROOT = Path(".")
OUTPUT = "project-structure.txt"

IGNORE = {
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    ".env",
    ".pytest_cache",
    "dist",
    "build",
}

def print_tree(path: Path, prefix=""):
    entries = sorted(
        [p for p in path.iterdir() if p.name not in IGNORE],
        key=lambda p: (p.is_file(), p.name.lower())
    )

    lines = []

    for index, entry in enumerate(entries):
        is_last = index == len(entries) - 1
        connector = "└── " if is_last else "├── "

        lines.append(prefix + connector + entry.name)

        if entry.is_dir():
            extension = "    " if is_last else "│   "
            lines.extend(print_tree(entry, prefix + extension))

    return lines


structure = [ROOT.name + "/"]
structure.extend(print_tree(ROOT))

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("\n".join(structure))

print(f"Structure saved to: {OUTPUT}")