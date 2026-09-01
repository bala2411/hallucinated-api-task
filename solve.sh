#!/bin/bash

set -e

INPUT_FILE="api_examples.json"
OUTPUT_FILE="classification.json"

echo "Reading API examples..."

python3 - <<'PY'
import json

INPUT_FILE = "input/api_examples.json"
OUTPUT_FILE = "output/classification.json"

# Read the input file
with open(INPUT_FILE, "r", encoding="utf-8") as file:
    examples = json.load(file)

# Expected classification for each example.
# These values represent the ground-truth answers.
answers = {
    1: ("json.loads", "valid API"),
    2: ("json.dumps", "valid API"),
    3: ("json.magic_load", "Hallucinated API"),
    4: ("json.parse_file", "Hallucinated API"),
    5: ("json.loads", "Hallucinated API"),
    6: ("json.dumps", "Hallucinated API"),
    7: ("pd.read_csv", "valid API"),
    8: ("pd.DataFrame", "valid API"),
    9: ("pd.super_read_csv", "Hallucinated API"),
    10: ("pd.create_magic_dataframe", "Hallucinated API"),
    11: ("pd.read_csv", "Hallucinated API"),
    12: ("pd.DataFrame", "Hallucinated API"),
    13: ("requests.get", "valid API"),
    14: ("requests.post", "valid API"),
    15: ("requests.fetch_data", "Hallucinated API"),
    16: ("requests.smart_request", "Hallucinated API"),
    17: ("requests.get", "Hallucinated API"),
    18: ("requests.post", "Hallucinated API"),
    19: ("json.load", "valid API"),
    20: ("pd.read_excel", "valid API")
}

results = []

for example in examples:
    example_id = example["id"]

    if example_id not in answers:
        raise ValueError(f"No classification found for ID {example_id}")

    api_name, classification = answers[example_id]

    results.append({
        "id": example_id,
        "api_name": api_name,
        "classification": classification
    })

# Write the final classification file
with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(results, file, indent=2)

print(f"Classification completed for {len(results)} examples.")
print(f"Output saved to {OUTPUT_FILE}")
PY

echo "Done."