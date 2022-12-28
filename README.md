# JSON Translator
a Python application for translating the strings in a JSON file to a different language.

## Features
- Recursively processes a JSON data structure and translates all string values that meet certain conditions
- Uses the MyMemory Translation API to translate the string values from English to the specified target language
- Skips string values that are not at least two characters long, do not contain a word, or contain only a single letter after being stripped of leading and trailing whitespace
- Keeps track of the progress of the translation process and prints the percentage complete
- Easy to use and customize to fit your translation needs

## Getting Started
To use the JSON Translator, you will need to have Python 3 installed on your machine. You will also need to install the required dependencies by running the following command:
```
pip install -r requirements.txt
```
Once the dependencies are installed, you can use the tool by running the following command:
```
python main.py -i INPUT_FILE -l TARGET_LANGUAGE -e EMAIL
```
Replace `INPUT_FILE` with the path to the JSON file you want to translate, `TARGET_LANGUAGE` with the desired target language, and `EMAIL` with your valid email address.

## Example
```
python main.py -i data.json -l es -e me@example.com
```
This command will translate the strings in the data.json file to Spanish.

## Q&A
**Q: Why do I need to provide an email address as a command line argument?**

A: The MyMemory Translation API requires a valid email address to be included in the request as the `de` parameter. This is a requirement to use the API, and providing your email address allows you to access the API's full capabilities, including the ability to translate up to 50,000 characters per day.

## Contributing
If you have an idea for a new feature or a bug fix, please open an issue or submit a pull request. Contributions to the JSON Translator are welcome and appreciated. Thank you for your interest in improving the tool!
