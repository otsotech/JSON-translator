# JSON Translator
A Python application for translating the strings in a JSON file to a different language.

## Features
- Translate the strings in a JSON file to a specified target language
- Uses machine translation for fast and accurate results
- Easy to use

## Getting Started
To use the JSON Translator, you will need to have Python 3 installed on your machine. You will also need to install the required dependencies by running the following command:
```
pip install -r requirements.txt
```
Once the dependencies are installed, you can use the tool by running the following command:
```
python translate.py -i INPUT_FILE -l TARGET_LANGUAGE
```
Replace INPUT_FILE with the path to the JSON file you want to translate, and TARGET_LANGUAGE with the desired target language (e.g. "fr" for French).

## Example
python translate.py -i data.json -l es
This command will translate the strings in the data.json file to Spanish.

## Contributing
If you have an idea for a new feature or a bug fix, please open an issue or submit a pull request. Contributions to the JSON Translator are welcome and appreciated. Thank you for your interest in improving the tool!
