import eng_to_ipa as ipa
from deep_translator import GoogleTranslator
import langid

import requests
import json
import inspect



def detect_lang(word): # langid is pretty slow, I plan to replace it with another system
    return langid.classify(word)[0]



def translate_word(word, source_lang, target_lang):
    return GoogleTranslator(source_lang, target_lang).translate(word).strip().lower()



def get_word_class(word, language):

    # because the dictionary api works only in english,
    # words need to be translated into english to get their grammar class. 
    if language != 'en':
        word = translate_word(word, language, 'en')

    url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'

    try:

        response = requests.get(url, timeout=1)
        # the timeout is set to 1 second for a compromise between an actually working function and speed. 
        data = json.loads(response.text.encode('utf-8'))

        # this list comprehension captures al the meanings of a word from it's JSON file in the API.
        return ', '.join([
            data[0]['meanings'][i]['partOfSpeech']
            for i in range(len(data[0]['meanings']))
        ])

    except:
        return '' #if the code above fails a blank space is returned.



class dictionary:



    def __init__(self, source_path):

        self.source_path = source_path # the path of the JSON file in which the dictionary is stored.

        with open(source_path, 'a') as f: # checks if the JSON exists; if it doesn't, it creates one.
            pass

        with open(self.source_path, 'r') as f:
            source_content = f.read()
            if len(source_content) < 5: # if the json is empty, a new dictionary is initialized.
                self.words = dict()
            else:
                self.words = json.loads(source_content)



    def update_languages(self):

        """
        Update self.languages with every target language in the dictionary sorted by frequency.
        """
    
        all_languages = [
            lang for word in self.words
            for lang in self.words[word]['translations']
        ]        
        all_languages_counted = list(
            {(lang, all_languages.count(lang)) for lang in all_languages}
        )
        all_languages_counted.sort(key = lambda x: x[1], reverse = True)

        self.languages = list(map(lambda x: x[0], all_languages_counted))



    def add_word(self, word, source_lang, target_langs):

        """
        Add a single word and its translations to the dictionary.

        This method adds a word to the dictionary with its source language, 
        grammatical class, pronunciation, and translations into target languages. 
        It updates the JSON file of the dictionary and language list if called directly from <module>,
        but doesn't update them when called from another function for optimization.

        word (str): The word to be added.
        source_lang (str): The source language of the word. Use 'auto' to detect the language.
        target_langs (str or list): Target language(s) for translations. A single string is converted to a list.


        - It translates the word into the specified target languages using `translate_word`.
        - It detects the language if `source_lang` is 'auto'.
        - It determines the grammatical class of the word with `get_word_class`.
        - It converts the word to IPA pronunciation using `ipa.convert`.
        - It updates the JSON file and languages list only if called directly.
        """
    
        # if there's only a target language, it's put into a list to make the code more general.
        if isinstance(target_langs, str): 
            target_langs = [target_langs]
        
        word = word.lower().strip()

        translations = { # every element is 'language: translation' for every target language.
            lang: translate_word(word, source_lang, lang)
            for lang in target_langs            
        }
        
        self.words[word] = { # this is the format of core elements of self.words
            'language': detect_lang(word) if source_lang == 'auto'
            else source_lang,
            'class': get_word_class(word, source_lang),
            'pronunciation': ipa.convert(word),
            'translations': translations,
        }

        caller_frame = inspect.stack()[1]
        caller_name = caller_frame.function

        if caller_name == '<module>':
            self.update_json()
            self.update_languages()
         


    def fill_translation_gaps(self, verbose=False):

        """
        This method ensures that every word in the dictionary is translated into all 
        self.languages. If a translation is missing for a specific language, it uses 
        the `translate_word` function to generate the translation and adds it to the 
        dictionary.


        - It updates the list of target languages using `update_languages`.
        - It iterates through all words and target languages.
        - it adds missing translations by calling `translate_word` with the source word, 
          its language, and the target language.
        - it updates the JSON file after completing the process.
        """

        self.update_languages()

        for i, word in enumerate(self.words):
            for j, lang in enumerate(self.languages):

                if not self.words[word]['translations'].get(lang):

                    new_translation = translate_word(
                        word,
                        self.words[word]['language'],
                        lang
                    )

                    self.words[word]['translations'][lang] = new_translation

                if verbose:
                    print(f'{i+1}({j+1})/{len(self.words)}')
            
        self.update_json()



    def add_words_in_bulk(self, filepath, source_lang=None, target_langs=None, verbose=False):

        """
        Add words in bulk from to the dictionary from a file.
        
        This method reads words from a file and adds them to the dictionary using the `add_word` method,
        then it updates the JSON file of the dictionary.

        filepath (str): Path to the file containing words to add, one word per line.
        source_lang (str, optional): The source language of the words. Default is None.
        target_langs (list of str, optional): List of target languages for translations. Default is None.
        verbose (bool, optional): If True, prints progress during word addition. Default is False.
        """    

        with open(filepath, 'r') as f:

            words_to_add = f.readlines()

            for i, word in enumerate(words_to_add):
                self.add_word(word, source_lang, target_langs)
                if verbose:
                    print(f'{i+1}/{len(words_to_add)}')

        self.update_json()
        self.update_languages()



    def __str__(self):
        return '\n'.join(
            [f'{word}: {self.words[word]}' for word in sorted(self.words)]
        )



    def update_json(self):

        """
        This method writes the self.words data to the JSON file of the dictionary.
        """

        with open(self.source_path, 'w') as f:
            json.dump(self.words, f, indent=4)



    def export_to_md(self, destination: str):

        """
        Export words and their translations to a Markdown table.

        This method generates a Markdown table with columns for the word, its grammatical 
        class, pronunciation, and translations in various languages. The table is saved to 
        the destination file.

        Table columns: "Word", "Class", "Pronunciation", and one for each language.

        Example:
            | Word       | Class    | Pronunciation | es        | fr        |
            |------------|----------|---------------|-----------|-----------|
            | en: hello  | noun     | həˈloʊ        | hola      | bonjour   |
        """

        self.update_languages()
        
        table = [
            f'| Word | Class | Pronunciation | {" | ".join(self.languages)} |',
            f'{"|---"*(len(self.languages)+3)}|'
        ]

        for word in sorted(self.words.keys()):

            word_to_display = f'{self.words[word]["language"]}: {word}'  
            pronunciation = self.words[word]['pronunciation']
            grammar_class = self.words[word]['class']
            
            translations = list()
            for lang in self.languages:
                try:
                    translations.append(self.words[word]['translations'][lang])
                except:
                    translations.append(' ')
            translations = ' | '.join(translations)

            table.append(
                f'| {word_to_display} | {grammar_class} | {pronunciation} | {translations} |'
            )

        with open(destination, 'w') as f:
            f.write('\n'.join(table))



if __name__ == '__main__':

    # to use for testing
    Lang_dict = PolyglotDict('test.json')
    Lang_dict.add_word('hi', 'en', ['fr','sw'])
    Lang_dict.add_words_in_bulk('list.txt', 'en', ['it','es'], verbose = True)
    Lang_dict.fill_translation_gaps(verbose = True)
    Lang_dict.export_to_md('dict.md')
    print(Lang_dict)
