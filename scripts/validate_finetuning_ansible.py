
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

DATASET = Path("data/finetuning/curated/ansible_instructions.jsonl")
def ansible_command(playbook_path):
    if sys.platform == "win32":
        path = Path(playbook_path).resolve()
        wsl_path = f"/mnt/{path.drive[0].lower()}{path.as_posix()[2:]}"
        wsl_python = "/mnt/c/Users/HP/Downloads/ansible llm/.venv-wsl/bin/python"
        return ["wsl.exe", "-d", "Ubuntu", "--", wsl_python, "-m", "ansible.cli.playbook", "--syntax-check", wsl_path]
    return [*ANSIBLE_PLAYBOOK, "--syntax-check", str(playbook_path)]


ANSIBLE_PLAYBOOK = [sys.executable, "-m", "ansible.cli.playbook"]


def validate_example(example, index):
    playbook = [
        {
            "name": f"Validate example {index}",
            "hosts": "localhost",
            "connection": "local",
            "gather_facts": False,
            "tasks": yaml.safe_load(example["output"]),
        }
    ]

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
        return result.returncode == 0, result.stdout + result.stderr
    finally:
        temp_path.unlink(missing_ok=True)


def main():
    with DATASET.open(encoding="utf-8") as f:
        examples = [json.loads(line) for line in f if line.strip()]

    passed = 0

    for index, example in enumerate(examples, 1):
        ok, output = validate_example(example, index)
        if ok:
            passed += 1
            print(f"PASS Example {index}: {example['instruction']}")
        else:
            print(f"FAIL Example {index}: {example['instruction']}")
            print(output)

    print(f"\nSyntax-check result: {passed}/{len(examples)} passed")
    print("Note: syntax checking does not execute tasks or prove they work on a real server.")


if __name__ == "__main__":
    main()
