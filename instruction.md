Error Classification and Tagging - Hallucinated API


Task Description:
	
	I have JSON file containing Python code snippets that use APIs form different Python libraries. My task is to analyze each code snippet and classify the API usage. I located input file as api_examples.json and Classification Tags like valid API, Hallucinated API, Invalid API.I get required output file as classification.json.

Requirements:

	Process every record in input file.
	Produce exactly one output record for each input.
	Do not add duplicates IDs.
	Use only the allowed classification tags.
	Preserver the API name as it appears in the code snippet.
	Write final result in output file.
	The output must be valid JSON.

Constraints:

	Do not modify input file.
	Do not modify evaluate file.
	Solution must work without network access.
	Solution must be deterministic.
