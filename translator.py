import argparse
import json
import requests

def translate(text, target_language):
    # MyMemory Translation API endpoint
    endpoint = "http://api.mymemory.translated.net/get"

    # Make a request to the API
    params = {
        "q": text,
        "langpair": f"en|{target_language}",
    }
    response = requests.get(endpoint, params=params)

    # Parse the response
    data = response.json()
    translated_text = data["responseData"]["translatedText"]

    return translated_text

def translate_json(json_data, target_language):
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            print(f"Checking key {key} with value {value}")
            if isinstance(value, str):
                json_data[key] = translate(value, target_language)
                print(f"Translated {value} to {json_data[key]}")
            else:
                # Skip values that are not strings
                print(f"Skipping non-string value for key {key}")
                continue
    elif isinstance(json_data, list):
        for item in json_data:
            translate_json(item, target_language)

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="input JSON file")
    parser.add_argument("-l", "--language", required=True, help="target language")
    args = parser.parse_args()

    # Load the JSON file
    with open(args.input, "r") as f:
        json_data = json.load(f)

    # Translate the JSON data
    translate_json(json_data, args.language)

    # Save the translated JSON data
    with open(args.input, "w") as f:
        json.dump(json_data, f, indent=2)
