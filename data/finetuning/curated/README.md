# Curated Ansible Instruction Dataset

## Purpose
Initial dataset for natural-language-to-Ansible-YAML generation,
inspired by Ansible Wisdom.

## Current dataset
- Number of examples: 6
- Format: JSONL
- Instruction: natural-language task description
- Output: Ansible YAML task list
- Source: original Galaxy role file paths
- Notes: adaptation details and limitations

## Source roles
- geerlingguy.docker
- geerlingguy.mysql
- geerlingguy.nginx

Check the original role licenses before redistributing derived data.

## Validation
- JSONL parsing: passed
- YAML parsing: passed
- Unique instructions: 6
- Ansible syntax checks: 6 passed, 0 failed

Syntax checks do not prove that tasks execute correctly on real hosts.

## Limitations
This is a small pilot dataset, not yet sufficient for reliable model
fine-tuning or evaluation. Examples require manual review for correctness,
platform compatibility, and source attribution.

## Next steps
1. Review the six examples.
2. Collect more traceable examples from Galaxy roles.
3. Validate YAML and Ansible syntax.
4. Split examples into training, validation, and test sets.
5. Evaluate the base CodeGen-350M model before fine-tuning.
