# Ansible LLM

A domain-specific language model project focused on generating Ansible YAML from natural-language instructions, inspired by IBM Research's Ansible Wisdom.

## Project Goals

- Collect Ansible YAML data from GitHub and Ansible Galaxy.
- Clean, classify and audit YAML files.
- Build instruction-output datasets for fine-tuning.
- Prepare training, validation and test splits.
- Explore fine-tuning Salesforce CodeGen 350M Multi for Ansible YAML generation.

## Repository Structure

- `scripts/` - Dataset collection, cleaning, inspection and validation scripts.
- `data/finetuning/` - Curated, candidate and combined instruction datasets and splits.
- `data/metadata/` - Dataset source and inspection metadata.
- `audit_results/` - Dataset classification and quality audit reports.
- `requirements.txt` - Python dependencies.

## Dataset Validation

The current datasets have passed YAML syntax validation:

| Dataset | Valid examples |
|---|---:|
| Curated | 8/8 |
| Combined | 28/28 |
| Galaxy candidates | 14/14 |
| MySQL candidates | 6/6 |
| **Total** | **56/56** |

Passing YAML syntax validation does not guarantee that tasks will execute successfully on an Ansible-managed system.

## Setup

Create a virtual environment:

`python -m venv .venv`

Activate it in Windows PowerShell:

`.venv\Scripts\Activate.ps1`

Install dependencies:

`pip install -r requirements.txt`

## Validation

Run the validation scripts:

- `python scripts/validate_finetuning_ansible.py`
- `python scripts/validate_combined_dataset.py`
- `python scripts/validate_galaxy_candidates.py`
- `python scripts/validate_mysql_candidates.py`

## Base Model

Salesforce CodeGen 350M Multi

https://huggingface.co/Salesforce/codegen-350M-multi

## Project Status

Dataset collection, preparation, inspection and validation have been completed for the current dataset version. Model fine-tuning, testing and evaluation are ongoing.
