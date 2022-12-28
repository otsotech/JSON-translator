import re
import requests
import logging

class TranslationError(Exception):
    pass

def translate(text, target_language, email):
    endpoint = "http://api.mymemory.translated.net/get"

    params = {
        "q": text,
        "langpair": f"en|{target_language}",
        "de": email,
    }
    try:
        response = requests.get(endpoint, params=params)
    except requests.RequestException as e:
        raise TranslationError("An error occurred while making the request: {}".format(e))

    try:
        data = response.json()
    except ValueError as e:
        raise TranslationError("An error occurred while parsing the response: {}".format(e))

    try:
        translated_text = data["responseData"]["translatedText"]
    except KeyError as e:
        raise TranslationError("An error occurred while accessing the response data: {}".format(e))

    return translated_text

def translate_json(json_data, target_language, email, keys_processed=0, total_keys=None):
    if total_keys is None:
        try:
            total_keys = count_keys(json_data)
        except ValueError as e:
            raise TranslationError("An error occurred while counting the keys in the input data: {}".format(e))

    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if isinstance(value, str) and len(value) > 1:
                if not re.search(r'\b[a-zA-Z]+\b', value):
                    logging.info("Skipping '{}' because it does not contain a word.".format(value))
                elif len(value.strip()) == 1:
                    logging.info("Skipping '{}' because it contains only a single letter.".format(value))
                else:
                    logging.info("Translating '{}'".format(value))
                    try:
                        json_data[key] = translate(value, target_language, email)
                    except TranslationError as e:
                        logging.error("Error occurred while translating '{}': {}".format(value, e))
            else:
                translate_json(value, target_language, email, keys_processed, total_keys)
            keys_processed += 1
            percentage_complete = keys_processed / total_keys * 100
            logging.info("    {:.2f}% complete\n".format(percentage_complete))
    elif isinstance(json_data, list):
        for i, item in enumerate(json_data):
            if isinstance(item, str) and len(item) > 1:
                if not re.search(r'\b[a-zA-Z]+\b', item):
                    logging.info("Skipping '{}' because it does not contain a word.".format(item))
                elif len(item.strip()) == 1:
                    logging.info("Skipping '{}' because it contains only a single letter.".format(item))
                else:
                    logging.info("Translating '{}'\n".format(item))
                    try:
                        json_data[i] = translate(item, target_language, email)
                    except TranslationError as e:
                        logging.error("Error occurred while translating '{}': {}".format(item, e))
            else:
                translate_json(item, target_language, email, keys_processed, total_keys)
            keys_processed += 1
            percentage_complete = keys_processed / total_keys * 100
            logging.info("    {:.2f}% complete".format(percentage_complete))
    return json_data

def count_keys(data):
    if not isinstance(data, (dict, list)):
        raise ValueError("Input data must be a dictionary or a list")
    total_keys = 0
    stack = [data]
    while stack:
        value = stack.pop()
        if isinstance(value, dict):
            total_keys += len(value)
            stack.extend(value.values())
        elif isinstance(value, list):
            total_keys += len(value)
            stack.extend(value)
    return total_keys

def traverse(data):
    if isinstance(data, (dict, list)):
        for key, value in data.items() if isinstance(data, dict) else enumerate(data):
            if isinstance(value, (dict, list)):
                yield from traverse(value)
            else:
                yield value
