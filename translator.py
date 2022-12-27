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
    print(f"Making request to {endpoint} with params {params}")
    response = requests.get(endpoint, params=params)

    # Parse the response
    data = response.json()
    translated_text = data["responseData"]["translatedText"]

    return translated_text

def translate_json(json_data, target_language):
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            print(f"Processing key {key} with value {value}")
            if isinstance(value, str) and len(value) > 1:
                # Check if the string contains only a symbol
                if not value.strip():
                    print(f"Skipping string {value} because it contains only a symbol")
                    continue
                print(f"Translating string {value}")
                json_data[key] = translate(value, target_language)
            else:
                translate_json(value, target_language)
    elif isinstance(json_data, list):
        for item in json_data:
            print(f"Processing item {item}")
            translate_json(item, target_language)
    else:
        # Return immediately if the value is not a string, dict, or list
        print(f"Skipping value {json_data} because it is not a string, dict, or list")
        return

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="input JSON file")
    parser.add_argument("-l", "--language", required=True, help="target language")
    args = parser.parse_args()
    print(f"Translating file {args.input} to language {args.language}")

    # Load the JSON file
    with open(args.input, "r") as f:
        json_data = json.load(f)
    print(f"Loaded JSON data: {json_data}")

    # Translate the JSON data
    translate_json(json_data, args.language)
    print(f"Translated JSON data: {json_data}")

    # Save the translated JSON data
    with open(args.input, "w") as f:
        json.dump(json_data, f, indent=2)
    print("Saved translated JSON data to file")
