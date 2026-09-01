import json
import os
import sys

INPUT_FILE = "input/api_examples.json"
OUTPUT_FILE = "output/classification.json"

REFERENCE_FILE = os.environ.get(
    "REFERENCE_FILE",
    "/evaluation/answers.json"
)

ALLOWED_TAGS = {
    "valid API",
    "Hallucinated API",
    "Invalid API"
}

def load_json(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as error:
        print(f"FAIL: Could not read {filename}: {error}")
        sys.exit(1)


def main():
    input_data = load_json(INPUT_FILE)
    output_data = load_json(OUTPUT_FILE)
    reference_data = load_json(REFERENCE_FILE)

    expected = {
        item["id"]: item
        for item in reference_data
    }

    if not isinstance(output_data, list):
        print("FAIL: Output must be a JSON array.")
        sys.exit(1)

    if len(output_data) != len(input_data):
        print(
            f"FAIL: Expected {len(input_data)} records, "
            f"but found {len(output_data)}."
        )
        sys.exit(1)

    input_ids = [item["id"] for item in input_data]
    output_ids = [item.get("id") for item in output_data]

    if len(output_ids) != len(set(output_ids)):
        print("FAIL: Duplicate IDs found.")
        sys.exit(1)

    if set(input_ids) != set(output_ids):
        print("FAIL: Output IDs do not match input IDs.")
        sys.exit(1)

    for result in output_data:
        result_id = result.get("id")

        if result_id not in expected:
            print(f"FAIL: Unexpected ID {result_id}.")
            sys.exit(1)

        if "api_name" not in result:
            print(f"FAIL: ID {result_id} is missing api_name.")
            sys.exit(1)

        if "classification" not in result:
            print(f"FAIL: ID {result_id} is missing classification.")
            sys.exit(1)

        if result["classification"] not in ALLOWED_TAGS:
            print(
                f"FAIL: Invalid classification for ID {result_id}."
            )
            sys.exit(1)

        correct = expected[result_id]

        if result["api_name"] != correct["api_name"]:
            print(f"FAIL: Wrong API name for ID {result_id}.")
            sys.exit(1)

        if result["classification"] != correct["classification"]:
            print(
                f"FAIL: Wrong classification for ID {result_id}. "
                f"Expected '{correct['classification']}', "
                f"got '{result['classification']}'."
            )
            sys.exit(1)

    print("PASS: All 20 API classifications are correct.")


if __name__ == "__main__":
    main()