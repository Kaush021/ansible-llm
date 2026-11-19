
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

DATASET = Path("data/finetuning/combined/ansible_instructions.jsonl")
def ansible_command(playbook_path):
    if sys.platform == "win32":
        path = Path(playbook_path).resolve()
        wsl_path = f"/mnt/{path.drive[0].lower()}{path.as_posix()[2:]}"
        wsl_python = "/mnt/c/Users/HP/Downloads/ansible llm/.venv-wsl/bin/python"
        return [
            "wsl.exe", "-d", "Ubuntu", "--", wsl_python,
            "-m", "ansible.cli.playbook", "--syntax-check", wsl_path,
        ]
    return [*ANSIBLE_PLAYBOOK, "--syntax-check", str(playbook_path)]


ANSIBLE_PLAYBOOK = [sys.executable, "-m", "ansible.cli.playbook"]


def main():
    records = [
        json.loads(line)
        for line in DATASET.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    passed = 0
    failed = 0

    for index, record in enumerate(records, start=1):
        try:
            tasks = yaml.safe_load(record["output"])

            if not isinstance(tasks, list) or not tasks:
                raise ValueError("Output must be a non-empty YAML task list")

            playbook = [{
                "name": f"Validate example {index}",
                "hosts": "localhost",
                "connection": "local",
                "gather_facts": False,
                "tasks": tasks,
            }]

            with tempfile.NamedTemporaryFile(
                mode="w",
                suffix=".yml",
                encoding="utf-8",
                delete=False,
            ) as temp:
                yaml.safe_dump(playbook, temp, sort_keys=False)
                temp_path = Path(temp.name)

            try:
                result = subprocess.run(
                    ansible_command(temp_path),
                    capture_output=True,
                    text=True,
                )
            finally:
                temp_path.unlink(missing_ok=True)

            if result.returncode == 0:
                passed += 1
                print(f"PASS {index}: {record['instruction']}")
            else:
                failed += 1
                print(f"FAIL {index}: {record['instruction']}")
                print(result.stdout)
                print(result.stderr)

        except Exception as exc:
            failed += 1
            print(f"FAIL {index}: {record.get('instruction', 'Unknown instruction')}")
            print(f"Reason: {exc}")

    print("\n=== Ansible Syntax Check Summary ===")
    print("Total records:", len(records))
    print("Passed:", passed)
    print("Failed:", failed)
    print("RESULT:", "PASS" if failed == 0 else "CHECK FAILURES")


if __name__ == "__main__":
    main()
