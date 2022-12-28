import requests
import re

def translate(text, target_language, email):
    # MyMemory Translation API endpoint
    endpoint = "http://api.mymemory.translated.net/get"

    # Make a request to the API
    params = {
        "q": text,
        "langpair": f"en|{target_language}",
        "de": email,
    }
    response = requests.get(endpoint, params=params)

    # Parse the response
    data = response.json()
    translated_text = data["responseData"]["translatedText"]

    return translated_text

def translate_json(json_data, target_language, email, keys_processed=0, total_keys=None):
    # Initialize total_keys to the number of keys in json_data if it is not provided
    if total_keys is None:
        total_keys = count_keys(json_data)

    # If json_data is a dictionary, process each key-value pair
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            # Skip values that are not strings or have only one character
            if isinstance(value, str) and len(value) > 1:
                # Skip values that do not contain a word (i.e., a sequence of one or more letters surrounded by word boundaries)
                if not re.search(r'\b[a-zA-Z]+\b', value):
                    print("Skipping '{}' because it does not contain a word.".format(value))
                # Skip values that contain only a single letter
                elif len(value.strip()) == 1:
                    print("Skipping '{}' because it contains only a single letter.".format(value))
                # Translate values that meet the above conditions
                else:
                    print("Translating '{}'".format(value))
                    json_data[key] = translate(value, target_language, email)
            # Recursively process values that are not strings or have only one character
            else:
                translate_json(value, target_language, email, keys_processed, total_keys)
            # Increment the keys_processed counter and print the percentage complete
            keys_processed += 1
            percentage_complete = keys_processed / total_keys * 100
            print("    {:.2f}% complete\n".format(percentage_complete))
    # If json_data is a list, process each item
    elif isinstance(json_data, list):
        for i, item in enumerate(json_data):
            # Skip items that are not strings or have only one character
            if isinstance(item, str) and len(item) > 1:
                # Skip items that do not contain a word (i.e., a sequence of one or more letters surrounded by word boundaries)
                if not re.search(r'\b[a-zA-Z]+\b', item):
                    print("Skipping '{}' because it does not contain a word.".format(item))
                # Skip items that contain only a single letter
                elif len(item.strip()) == 1:
                    print("Skipping '{}' because it contains only a single letter.".format(item))
                # Translate items that meet the above conditions
                else:
                    print("Translating '{}'\n".format(item))
                    json_data[i] = translate(item, target_language, email)
            # Recursively process items that are not strings or have
            else:
                translate_json(item, target_language, email, keys_processed, total_keys)
            # Increment the keys_processed counter and print the percentage complete
            keys_processed += 1
            percentage_complete = keys_processed / total_keys * 100
            print("    {:.2f}% complete".format(percentage_complete))
    # Return the modified json_data
    return json_data



def count_keys(data):
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
    if isinstance(data, dict):
        for key, value in data.items():
            yield value
            yield from traverse(value)
    elif isinstance(data, list):
        for item in data:
            yield item
            yield from traverse(item)
