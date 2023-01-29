import argparse
import json
import logging
import sys
import requests

from translation_functions import translate, translate_json, TranslationError

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="input JSON file")
    parser.add_argument("-o", "--output", help="output JSON file")
    parser.add_argument("-l", "--language", required=True, help="target language")
    parser.add_argument("-e", "--email", required=True, help="email address")
    return parser.parse_args()

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logger = logging.getLogger(__name__)

    # Parse command line arguments
    args = parse_args()
    input_file = args.input
    output_file = args.output or input_file
    language = args.language
    email = args.email
    logger.info(f"Translating file {input_file} to language {language}. Email: {email}")

    # Read and parse input JSON file
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            json_data = json.load(f)
    except FileNotFoundError:
        logger.error(f"Input file '{input_file}' not found")
        sys.exit(1)
    except OSError as e:
        logger.error(f"An error occurred while reading the input file: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        logger.error(f"An error occurred while parsing the input file: {e}")
        sys.exit(1)

    # Translate JSON data
    try:
        translate_json(json_data, language, email)
    except TranslationError as e:
        logger.error(f"An error occurred while translating the JSON data: {e}")
        sys.exit(1)

    # Write translated JSON data to output file
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2)
    except OSError as e:
        logger.error(f"An error occurred while saving the translated JSON data to the file: {e}")
        sys.exit(1)

    logger.info(f"Saved translated JSON data to file '{output_file}'")
