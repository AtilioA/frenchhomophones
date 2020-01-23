import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))

from wiktionaryparser import WiktionaryParser
parser = WiktionaryParser()

# from . import populate_db as db


def fetch_wiktionary_word(word):
    """ Extract word's information with WiktionaryParser """

    parsedHomophone = parser.fetch(word.strip(), "french")[0]

    # TODO: Move to another function
    for i, pOS in enumerate(parsedHomophone["definitions"]):
        if pOS["partOfSpeech"] == "verb":
            foundVerb = True
            verbIndex = i

        parsedHomophone["definitions"][i]["text"] = parsedHomophone["definitions"][i]["text"][0]
        parsedHomophone["definitions"][i]["definitions"] = parsedHomophone["definitions"][i]["text"][1:]
    if foundVerb:
        parsedInfinitive = parser.fetch("test", "english")[0]
        parsedHomophone["definitions"][i]["infinitive"] = {
            "text": parsedInfinitive["definitions"][0]["text"][0],
            "definitions": parsedInfinitive["definitions"][0]["text"][1:]
        }

    return parsedHomophone
    pass


if __name__ == "__main__":
    print(fetch_wiktionary_word("faire"))
