import requests

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
    if total_keys is None:
        total_keys = count_keys(json_data)

    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if isinstance(value, str) and len(value) > 1:
                if not value.strip() or len(value.strip()) == 1 or value.isdigit():
                    print(f"Skipping '{value}' because it contains only a single letter or symbol or only numbers.")
                else:
                    print(f"Translating '{value}'")
                    json_data[key] = translate(value, target_language, email)
            else:
                translate_json(value, target_language, email, keys_processed, total_keys)
            keys_processed += 1
            percentage_complete = keys_processed / total_keys * 100
            print(f"{percentage_complete:.2f}% complete\n")
    elif isinstance(json_data, list):
        for i, item in enumerate(json_data):
            if isinstance(item, str) and len(item) > 1:
                if not item.strip() or len(item.strip()) == 1 or item.isdigit():
                    print(f"Skipping '{item}' because it contains only a single letter or symbol or only numbers.")
                else:
                    print(f"Translating '{item}'")
                    json_data[i] = translate(item, target_language, email)
            else:
                translate_json(item, target_language, email, keys_processed, total_keys)
            keys_processed += 1
            percentage_complete = keys_processed / total_keys * 100
            print(f"{percentage_complete:.2f}% complete\n")
    else:
        print(f"Skipping '{json_data}' because it is not a string, dict, or list.")
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
