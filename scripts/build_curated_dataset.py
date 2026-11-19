import json
from pathlib import Path

OUTPUT = Path("data/finetuning/curated/ansible_instructions.jsonl")

examples = [
    {
        "instruction": "Write an Ansible task to install the Docker packages.",
        "output": """- name: Install Docker packages
  ansible.builtin.package:
    name:
      - docker-ce
      - docker-ce-cli
      - docker-ce-rootless-extras
      - containerd.io
      - docker-buildx-plugin
    state: present""",
        "source": "data/raw/galaxy-roles/geerlingguy.docker/defaults/main.yml; data/raw/galaxy-roles/geerlingguy.docker/tasks/main.yml",
        "notes": "Simplified adaptation using the role's default package list; repository availability is environment-dependent."
    },
    {
        "instruction": "Write an Ansible task to start Docker and enable it at boot.",
        "output": """- name: Ensure Docker is running and enabled
  ansible.builtin.service:
    name: docker
    state: started
    enabled: true""",
        "source": "data/raw/galaxy-roles/geerlingguy.docker/tasks/main.yml; data/raw/galaxy-roles/geerlingguy.docker/defaults/main.yml",
        "notes": "Simplified adaptation of the role's Docker service task."
    },
    {
        "instruction": "Write an Ansible task to create the /etc/docker directory with permissions 0755.",
        "output": """- name: Ensure Docker configuration directory exists
  ansible.builtin.file:
    path: /etc/docker
    state: directory
    mode: "0755" """.rstrip(),
        "source": "data/raw/galaxy-roles/geerlingguy.docker/tasks/main.yml",
        "notes": "Adapted from the role; omits the original conditional on daemon options."
    },
    {
        "instruction": "Write an Ansible task to ensure a MySQL database named example exists.",
        "output": """- name: Ensure example database exists
  ansible.mysql.mysql_db:
    name: example
    state: present""",
        "source": "data/raw/galaxy-roles/geerlingguy.mysql/tasks/databases.yml; data/raw/galaxy-roles/geerlingguy.mysql/defaults/main.yml",
        "notes": "Simplified adaptation; requires the ansible.mysql collection and its dependencies."
    },
    {
        "instruction": "Write an Ansible task to install the dirmngr package on Ubuntu.",
        "output": """- name: Ensure dirmngr is installed
  ansible.builtin.apt:
    name: dirmngr
    state: present""",
        "source": "data/raw/galaxy-roles/geerlingguy.nginx/tasks/setup-Ubuntu.yml",
        "notes": "Adapted from the role's Ubuntu setup tasks."
    },
    {
        "instruction": "Write an Ansible task to ensure the Nginx package is installed on Debian or Ubuntu.",
        "output": """- name: Ensure nginx is installed
  ansible.builtin.apt:
    name: nginx
    state: present""",
        "source": "data/raw/galaxy-roles/geerlingguy.nginx/tasks/setup-Debian.yml",
        "notes": "Simplified adaptation; the source role uses a configurable package-name variable."
    },
    {
        "instruction": "Write an Ansible task to add a list of users to the Docker group without removing their existing supplementary groups.",
        "output": """- name: Add users to the Docker group
  ansible.builtin.user:
    name: "{{ item }}"
    groups: docker
    append: true
  loop: "{{ docker_users }}\"""",
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

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

with OUTPUT.open("w", encoding="utf-8") as f:
    for example in examples:
        f.write(json.dumps(example, ensure_ascii=False) + "\n")

print(f"Created {len(examples)} examples.")
print(f"Output: {OUTPUT}")