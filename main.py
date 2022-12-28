import argparse
import json

from translation_functions import translate, translate_json, TranslationError

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="input JSON file")
    parser.add_argument("-l", "--language", required=True, help="target language")
    parser.add_argument("-e", "--email", required=True, help="email address")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    print(f"Translating file {args.input} to language {args.language}. Email: {args.email}\n")

    try:
        with open(args.input, "r", encoding="utf-8") as f:
            json_data = json.load(f)
    except OSError as e:
        print("An error occurred while reading the input file: {}".format(e))
        exit(1)
    except json.JSONDecodeError as e:
        print("An error occurred while parsing the input file: {}".format(e))
        exit(1)

    try:
        translate_json(json_data, args.language, args.email)
    except TranslationError as e:
        print("An error occurred while translating the JSON data: {}".format(e))
        exit(1)

    try:
        with open(args.input, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2)
    except OSError as e:
        print("An error occurred while saving the translated JSON data to the file: {}".format(e))
        exit(1)

    print("Saved translated JSON data to file.")
