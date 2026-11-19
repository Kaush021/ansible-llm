from pathlib import Path
from collections import Counter
import hashlib
import csv
import yaml

ROOT = Path("data/raw/galaxy-roles")
OUT = Path("data/metadata")
OUT.mkdir(parents=True, exist_ok=True)

files = sorted(
    p for p in ROOT.rglob("*")
    if p.is_file()
    and p.suffix.lower() in {".yml", ".yaml"}
    and "tasks" in p.parts
)

seen_hashes = {}
rows = []
stats = Counter()

for path in files:
    relative_path = str(path)
    role = path.relative_to(ROOT).parts[0]
    status = "valid"
    task_count = 0
    named_tasks = 0
    modules = set()
    duplicate_of = ""
    error = ""

    try:
        content = path.read_text(encoding="utf-8")
        data = yaml.safe_load(content)

        if not isinstance(data, list):
            status = "not_a_task_list"
        else:
            task_count = len(data)

            for item in data:
                if not isinstance(item, dict):
                    continue

                if "name" in item:
                    named_tasks += 1

                action = item.get("action")
                if isinstance(action, dict) and action.get("module"):
                    modules.add(str(action["module"]))

                common_modules = {
                    "apt", "yum", "dnf", "package", "service",
                    "user", "group", "file", "copy", "template",
                    "command", "shell", "get_url", "uri",
                    "include_tasks", "include_vars", "set_fact",
                    "debug", "stat", "git", "lineinfile",
                    "blockinfile", "systemd", "cron", "mount",
                    "sysctl", "assert", "fail", "meta",
                    "import_tasks", "import_role", "include_role"
                }

                for key in item:
                    if isinstance(key, str) and (
                        "." in key or key in common_modules
                    ):
                        modules.add(key)

        digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
        if digest in seen_hashes:
            duplicate_of = seen_hashes[digest]
            stats["exact_duplicates"] += 1
        else:
            seen_hashes[digest] = relative_path

    except Exception as exc:
        status = "parse_error"
        error = str(exc)

    stats[status] += 1
    stats["task_items"] += task_count
    stats["named_task_items"] += named_tasks

    rows.append({
        "role": role,
        "file": relative_path,
        "yaml_status": status,
        "task_items": task_count,
        "named_task_items": named_tasks,
        "possible_modules": ";".join(sorted(modules)),
        "duplicate_of": duplicate_of,
        "error": error,
    })

report = OUT / "galaxy_task_inspection.csv"

with report.open("w", newline="", encoding="utf-8") as f:
    fieldnames = [
        "role", "file", "yaml_status", "task_items",
        "named_task_items", "possible_modules",
        "duplicate_of", "error"
    ]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Task-path files inspected: {len(files)}")
print(f"YAML files parsed as lists: {stats['valid']}")
print(f"Files not parsed as lists: {stats['not_a_task_list']}")
print(f"Parse errors: {stats['parse_error']}")
print(f"Exact duplicate files after first occurrence: {stats['exact_duplicates']}")
print(f"Task items counted: {stats['task_items']}")
print(f"Named task items: {stats['named_task_items']}")
print(f"Report saved to: {report}")
