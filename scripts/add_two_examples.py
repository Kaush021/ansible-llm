import json
from pathlib import Path

path = Path("data/finetuning/curated/ansible_instructions.jsonl")

with path.open(encoding="utf-8") as f:
    examples = [json.loads(line) for line in f if line.strip()]

new_examples = [
    {
        "instruction": "Write an Ansible task to add a list of users to the Docker group without removing their existing supplementary groups.",
        "output": """- name: Add users to the Docker group
  ansible.builtin.user:
    name: "{{ item }}"
    groups: docker
    append: true
  loop: "{{ docker_users }}""",
        "source": "data/raw/galaxy-roles/geerlingguy.docker/tasks/docker-users.yml",
        "notes": "Simplified adaptation. Requires docker_users to be defined as a list. Docker group membership grants powerful privileges."
    },
    {
        "instruction": "Write an Ansible task to ensure the Nginx virtual-host configuration directory exists with permissions 0755.",
        "output": """- name: Ensure Nginx virtual-host directory exists
  ansible.builtin.file:
    path: "{{ nginx_vhost_path }}"
    state: directory
    mode: "0755" """.rstrip(),
        "source": "data/raw/galaxy-roles/geerlingguy.nginx/tasks/vhosts.yml",
        "notes": "Simplified adaptation. Requires nginx_vhost_path to be defined; the original role also notifies a handler to reload Nginx."
    }
]

existing_instructions = {e["instruction"] for e in examples}

for example in new_examples:
    if example["instruction"] not in existing_instructions:
        examples.append(example)
        existing_instructions.add(example["instruction"])

with path.open("w", encoding="utf-8") as f:
    for example in examples:
        f.write(json.dumps(example, ensure_ascii=False) + "\n")

print(f"Total examples: {len(examples)}")
print(f"Output: {path}")
