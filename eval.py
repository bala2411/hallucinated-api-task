import json
import sys
from pathlib import Path

INPUT_FILE = Path("input/api_examples.json")
OUTPUT_FILE = Path("output/classification.json")

ALLOWED_TAGS = {
    "valid API",
    "Hallucinated API",
    "Invalid API",
}

EXPECTED = {
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
    20: ("pd.read_excel", "valid API"),
}


def fail(message):
    print(f"FAIL: {message}")
    sys.exit(1)


def main():
    if not INPUT_FILE.exists():
        fail(f"Input file not found: {INPUT_FILE}")

    if not OUTPUT_FILE.exists():
        fail(f"Output file not found: {OUTPUT_FILE}")

    try:
        with INPUT_FILE.open("r", encoding="utf-8") as f:
            inputs = json.load(f)
    except Exception as exc:
        fail(f"Could not read input JSON: {exc}")

    try:
        with OUTPUT_FILE.open("r", encoding="utf-8") as f:
            outputs = json.load(f)
    except Exception as exc:
        fail(f"Could not read output JSON: {exc}")

    if not isinstance(inputs, list):
        fail("Input must be a JSON array.")

    if not isinstance(outputs, list):
        fail("Output must be a JSON array.")

    if len(outputs) != len(inputs):
        fail(
            f"Expected {len(inputs)} output records, "
            f"but found {len(outputs)}."
        )

    input_ids = [item.get("id") for item in inputs]

    if len(set(input_ids)) != len(input_ids):
        fail("Input contains duplicate IDs.")

    output_ids = [item.get("id") for item in outputs]

    if len(set(output_ids)) != len(output_ids):
        fail("Output contains duplicate IDs.")

    if set(output_ids) != set(input_ids):
        fail("Output IDs do not exactly match input IDs.")

    for record in outputs:
        if not isinstance(record, dict):
            fail("Every output record must be a JSON object.")

        required_fields = {"id", "api_name", "classification"}

        if set(record.keys()) != required_fields:
            fail(
                f"Invalid fields for ID {record.get('id')}. "
                f"Expected exactly: {sorted(required_fields)}"
            )

        record_id = record["id"]

        if record_id not in EXPECTED:
            fail(f"No expected classification for ID {record_id}.")

        api_name, classification = EXPECTED[record_id]

        if record["api_name"] != api_name:
            fail(
                f"ID {record_id}: expected API name "
                f"{api_name!r}, got {record['api_name']!r}."
            )

        if record["classification"] not in ALLOWED_TAGS:
            fail(
                f"ID {record_id}: invalid classification tag "
                f"{record['classification']!r}."
            )

        if record["classification"] != classification:
            fail(
                f"ID {record_id}: expected classification "
                f"{classification!r}, got {record['classification']!r}."
            )

    print(f"PASS: All {len(outputs)} records are correctly classified.")
    sys.exit(0)


if __name__ == "__main__":
    main()