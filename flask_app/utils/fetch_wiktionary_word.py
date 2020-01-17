import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))

from wiktionaryparser import WiktionaryParser
parser = WiktionaryParser()

from . import populate_db as db


def fetch_wiktionary_word(word):
    """ Extract word's information with WiktionaryParser """

    parsedHomophone = parser.fetch(word.strip(), "french")

    # Treat each information accordingly
    try:
        ipaHomophones = parsedHomophone[0]["pronunciations"]['text']
        if len(ipaHomophones) > 1:  # Has IPA and homophones
            ipa = ipaHomophones[0]
            homophones = ipaHomophones[1]
        else:
            ipa = None
    except:
        pass
    try:
        homophones = ipaHomophones[0]
        homophones = homophones[11:].split(',')
        homophones[0] = homophones[0].strip()
    except:
        homophones = None

    wordDefinitions = parsedHomophone[0]["definitions"][0]["text"][1:]

    ipa = db.clean_IPA_string(ipa)
    print(ipa)

    try:
        audio = parsedHomophone[0]["pronunciations"]['audio'][0]
    except:
        audio = parsedHomophone[0]["pronunciations"]['audio']

    pronunciations = parsedHomophone[0]["pronunciations"]

    homophone = {
        'word': parsedHomophone[0]["definitions"][0]["text"][0],
        'partOfSpeech': parsedHomophone[0]["definitions"][0]["partOfSpeech"],
        'wordDefinitions': parsedHomophone[0]["definitions"][0]["text"][1:],
        'sentenceExamples': parsedHomophone[0]["definitions"][0]["examples"],
        'audio': audio,
        'homophones': homophones,
        'ipa': ipa,
    }

    return homophone


if __name__ == "__main__":
    print(fetch_wiktionary_word("particulariser"))
