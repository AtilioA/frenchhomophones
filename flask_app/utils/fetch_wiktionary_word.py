import os
import re
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))

from wiktionaryparser import WiktionaryParser
parser = WiktionaryParser()


def find_infinitive_form(verbDefinition):
    match = re.search(r".*of (\w+)\s*$", verbDefinition)
    if match:
        return match.group(1)
    else:
        return None


def fetch_wiktionary_word(word, isInfinitive=False):
    """ Extract word information with WiktionaryParser """

    parsedHomophone = parser.fetch(word.strip(), "french")[0]
    if not parsedHomophone["definitions"]:
        print("Word not found.")
        exit(-1)

    # print(parsedHomophone)

    try: 
        # If IPA entry exists
        if parsedHomophone['pronunciations']['text'][0][:3] == "IPA":
            # print("Has IPA")
            parsedHomophone['pronunciations']['IPA'] = parsedHomophone['pronunciations']['text'][0]
            if parsedHomophone['pronunciations']['text'][1][:10] == "Homophones":
                # print("Has Homophones")
                parsedHomophone['pronunciations']['homophones'] = parsedHomophone['pronunciations']['text'][1][12:].split(", ")

        # If IPA entry doesn't exist
        elif parsedHomophone['pronunciations']['text'][0][:8] in "Homophone":
            # print("Doesn't have IPA, has Homophones")
            parsedHomophone['pronunciations']['IPA'] = None
            parsedHomophone['pronunciations']['homophones'] = parsedHomophone['pronunciations']['text'][0].split(", ")
        else:
            # print(parsedHomophone['pronunciations']['text'][0][:8])
            print("\n!Something wrong is not right!\n")
    except KeyError as err:
        print(err)

    # Delete "text" key from "pronunciations" value
    parsedHomophone['pronunciations'].pop('text', None)
    
    for i, pOS in enumerate(parsedHomophone['definitions']):
        # Introduce "infinitive" key
        if pOS['partOfSpeech'] == "verb" and not isInfinitive:
            # Look for infinitive form if it's a verb
            try:
                infinitive = find_infinitive_form(pOS['text'][1]).strip()
                # print(f"\nFetching infinitive: {pOS['text'][1]}")
                # print(infinitive)
                parsedInfinitive = parser.fetch(infinitive, "french")[0]
                # print(f"infinitive dictionary: {parsedInfinitive}")
                parsedHomophone['definitions'][i]['infinitive'] = {
                    "text": parsedInfinitive['definitions'][0]['text'][0],
                    "meanings": parsedInfinitive['definitions'][0]['text'][1:]
                }
            except (TypeError, AttributeError):
                print("Couldn't fetch infinitive form")

        else:
            parsedHomophone['definitions'][i]['infinitive'] = None

        # Split "text" value from "definitions" key into keys "word" and "meanings"
        parsedHomophone['word'] = parsedHomophone['definitions'][i]['text'][0]
        parsedHomophone['definitions'][i]['meanings'] = parsedHomophone['definitions'][i]['text'][1:]
        # Remove "text" value from definitions key
        word = parsedHomophone['definitions'][i].pop('text', None)


    return parsedHomophone


def request_homophones_wiktionary():
    """ Read french_homophones.txt to request words' informations with WiktionaryParser.

        Write to homophones.txt.
    """

    with open("french_homophones.txt", "r+", encoding="utf8") as fHomophones:
        with open("homophones2.txt", "a+", encoding="utf8") as fOut:
            words = fHomophones.readlines()
            for word in words[100:300]:
                print(f"Fetching word {word}", end="")
                parsedHomophone = fetch_wiktionary_word(word.strip())
                fOut.write(f"{parsedHomophone}\n")


if __name__ == "__main__":
    # print(fetch_wiktionary_word("abadez"))
    request_homophones_wiktionary()
