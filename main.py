import argparse
import json

from translation_functions import translate, translate_json

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="input JSON file")
    parser.add_argument("-l", "--language", required=True, help="target language")
    parser.add_argument("-e", "--email", required=True, help="email address")
    args = parser.parse_args()
    print(f"Translating file {args.input} to language {args.language}. Email: {args.email}\n")

    # Load the JSON file
    with open(args.input, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    # Translate the JSON data
    translate_json(json_data, args.language, args.email)

    # Save the translated JSON data
    with open(args.input, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2)
    print("Saved translated JSON data to file.")
