
import json
from pathlib import Path

SOURCES = [
    Path("data/finetuning/curated/ansible_instructions.jsonl"),
    Path("data/finetuning/candidates/galaxy_instructions.jsonl"),
    Path("data/finetuning/candidates/mysql_instructions.jsonl"),
]

OUTPUT = Path("data/finetuning/combined/ansible_instructions.jsonl")


def main():
    records = []
    seen = {}
    duplicates = 0
    conflicts = 0

    for source in SOURCES:
        if not source.exists():
            raise FileNotFoundError(f"Missing dataset: {source}")

        with source.open(encoding="utf-8") as f:
            for line_number, line in enumerate(f, 1):
                if not line.strip():
                    continue

                record = json.loads(line)
                instruction = record.get("instruction", "").strip()
                output = record.get("output", "").strip()

                if not instruction or not output:
                    raise ValueError(
                        f"Missing instruction/output: {source}:{line_number}"
                    )

                # Use normalized instruction text for exact instruction deduplication.
                key = " ".join(instruction.casefold().split())

                if key in seen:
                    duplicates += 1
                    previous = seen[key]

                    if previous["output"].strip() != output:
                        conflicts += 1
                        print(
                            "CONFLICT: Same instruction has different outputs:",
                            instruction,
                        )
                    else:
                        print("DUPLICATE:", instruction)

                    continue

                record["instruction"] = instruction
                seen[key] = record
                records.append(record)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print("\n=== Combined Dataset Summary ===")
    print("Source files:", len(SOURCES))
    print("Unique instructions:", len(records))
    print("Duplicate instructions skipped:", duplicates)
    print("Conflicting duplicate instructions:", conflicts)
    print("Output:", OUTPUT)

    if conflicts:
        print("WARNING: Review conflicting duplicates before training.")
    else:
        print("No conflicting duplicate instructions found.")


if __name__ == "__main__":
    main()
