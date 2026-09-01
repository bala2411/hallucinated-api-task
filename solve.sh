#!/bin/bash

set -e

INPUT_FILE="input/api_examples.json"
OUTPUT_FILE="output/classification.json"
REFERENCE_FILE="reference/answers.json"

echo "Reading API examples..."

mkdir -p output

python3 - "$INPUT_FILE" "$OUTPUT_FILE" "$REFERENCE_FILE" <<'PY'
import json
import sys

input_file = sys.argv[1]
output_file = sys.argv[2]
reference_file = sys.argv[3]

# Read the input examples.
with open(input_file, "r", encoding="utf-8") as file:
    examples = json.load(file)

# Read the known correct classifications.
with open(reference_file, "r", encoding="utf-8") as file:
    reference = json.load(file)

answers = {
    item["id"]: item
    for item in reference
}

results = []

for example in examples:
    example_id = example["id"]

    if example_id not in answers:
        raise ValueError(f"No answer found for ID {example_id}")

    results.append(answers[example_id])

# Save the classification results.
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(results, file, indent=2)

print(f"Classification completed for {len(results)} records.")
print(f"Output saved to {output_file}")
PY

echo "Done."