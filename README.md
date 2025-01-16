# PolyglotDict
A Python class designed to easily create, manage, and expand a smart multilingual dictionary.

## Features

- **JSON compatibility**: the PolyglotDict class itself relies to an external JSON file to store words.
- **Add words**: add words along with their
	- pronunciation
	- part of speech
	- multilanguage translations
- **Add words in bulk**: add a list of words from .txt file. 
- **Language detection**: automatically detect the language of words when needed.
- **Translation expansion**: fill translation gaps for all target languages in the dictionary.
- **Export to markdown**: export the dictionary to a Markdown table for easy sharing or documentation.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/LangDict.git
   ```
2. Go to the project directory:
   ```bash
   cd LangDict
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Initialize the dictionary
Create a new `LangDict` object by providing the path to a JSON file where the dictionary will be stored and interacted with.

```python
from LangDict import LangDict

dictionary = LangDict('dictionary.json')
```

### Add words

#### Add a single word
```python
dictionary.add_word("hello", source_lang="en", target_langs=["es", "fr", "it"])
```
#### Add words in bulk
Input a file where each word is on a separate line.
```python
dictionary.add_words_in_bulk("words.txt", source_lang="en", target_langs=["es", "fr"], verbose=True)
```

### Fill translation gaps
Automatically translate all words into missing target languages (it can take a while).
```python
dictionary.fill_translation_gaps(verbose=True)
```

### Export to markdown table
```python
dictionary.export_to_md("dictionary.md")
```

### Display the Dictionary
```python
print(dictionary)
```

## Dependencies

- [eng_to_ipa](https://pypi.org/project/eng-to-ipa/)
- [deep-translator](https://pypi.org/project/deep-translator/)
- [langid](https://github.com/saffsd/langid.py)
- [Dictionary API](https://dictionaryapi.dev/)

## Contributing

1. Fork the repository.
2. Create your feature branch:
   ```bash
   git checkout -b feature/YourFeature
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add some feature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature/YourFeature
   ```
5. Open a pull request.
