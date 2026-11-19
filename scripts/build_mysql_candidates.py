
import json
from pathlib import Path

OUTPUT = Path("data/finetuning/candidates/mysql_instructions.jsonl")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

examples = [
    {
        "instruction": (
            "Write an Ansible task to install the PyMySQL Python "
            "library package on Debian or Ubuntu."
        ),
        "output": """- name: Install the PyMySQL Python library.
  ansible.builtin.apt:
    name: python3-pymysql
    state: present""",
        "source": "geerlingguy.mysql/tasks/setup-Debian.yml",
        "note": (
            "Adapted example. Verify the package name for the target "
            "distribution and MySQL client library requirements."
        ),
    },
    {
        "instruction": (
            "Write an Ansible task to create the MySQL data directory "
            "owned by the mysql user and group, with permissions 0755."
        ),
        "output": """- name: Create the MySQL data directory.
  ansible.builtin.file:
    path: /var/lib/mysql
    state: directory
    owner: mysql
    group: mysql
    mode: "0755" """.rstrip(),
        "source": "geerlingguy.mysql/tasks/configure.yml",
        "note": (
            "Simplified example. Confirm the data directory and "
            "security context for the target installation."
        ),
    },
    {
        "instruction": (
            "Write an Ansible task to ensure the MySQL service is "
            "started and enabled at boot on a Linux server."
        ),
        "output": """- name: Ensure MySQL is started and enabled.
  ansible.builtin.service:
    name: mysql
    state: started
    enabled: true""",
        "source": "geerlingguy.mysql/tasks/configure.yml",
        "note": (
            "Assumes the service is named mysql. Some distributions "
            "use a different service name."
        ),
    },
]

with OUTPUT.open("w", encoding="utf-8") as f:
    for example in examples:
        f.write(json.dumps(example) + "\n")

print(f"Created {len(examples)} MySQL candidate examples.")
print(f"Output: {OUTPUT}")
