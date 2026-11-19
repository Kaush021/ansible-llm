
import json
from pathlib import Path

OUTPUT = Path("data/finetuning/candidates/galaxy_instructions.jsonl")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

examples = [
    {
        "instruction": (
            "Write an Ansible task to install the ca-certificates "
            "and python3-debian packages on a Debian-based system."
        ),
        "output": """- name: Ensure dependencies are installed.
  ansible.builtin.apt:
    name:
      - ca-certificates
      - python3-debian
    state: present""",
        "source": (
            "geerlingguy.docker/tasks/setup-Debian.yml"
        ),
    },
    {
        "instruction": (
            "Write an Ansible task to create the Nginx virtual-host "
            "configuration directory with permissions 0755."
        ),
        "output": """- name: Ensure nginx_vhost_path exists.
  ansible.builtin.file:
    path: "{{ nginx_vhost_path }}"
    state: directory
    mode: "0755"
  notify: reload nginx""",
        "source": (
            "geerlingguy.nginx/tasks/vhosts.yml"
        ),
    },
]

with OUTPUT.open("w", encoding="utf-8") as f:
    for example in examples:
        f.write(json.dumps(example) + "\n")

print(f"Created {len(examples)} candidate examples.")
print(f"Output: {OUTPUT}")
