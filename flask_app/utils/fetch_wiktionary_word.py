import os
import re
import sys
import urllib.parse
from multiprocessing import Pool

sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))

from wiktionaryparser import WiktionaryParser
parser = WiktionaryParser()


def unquote_url():
    with open("french_homophones.txt", "r", encoding="utf8", errors='ignore') as fR:
        with open("french_homophones_unquoted.txt", "w+", encoding="utf8", errors='ignore') as fW:
            words = [urllib.parse.unquote(line) for line in fR]
            fW.writelines(words)


def find_infinitive_form(verbDefinition):
    match = re.search(r".*of (\w+)\s*$", verbDefinition)
    if match:
        return match.group(1)
    else:
        return None


def fetch_wiktionary_word(word, isInfinitive=False):
    """ Extract word information with WiktionaryParser """

    try:
        word = word.strip()
        print(word)

        homophone = {'word': f"{word}"}
        parsedHomophone = parser.fetch(word, "french")[0]
        # print(parsedHomophone)

        if not (parsedHomophone['definitions'] or parsedHomophone['etymology'] or parsedHomophone['pronunciations']['text']):
            with open("failed.txt", "a+", encoding="utf8", errors='ignore') as failed:
                failed.write(f"{word}\n")
            print("Word not found.")
            print(parsedHomophone)

        # PRONUNCIATIONS
        parsedHomophone['pronunciations']['homophones'] = None
        try:
            for element in parsedHomophone['pronunciations']['text']:
                if "IPA" in element:
                    parsedHomophone['pronunciations']['IPA'] = element
                if "Homophone" in element:
                    parsedHomophone['pronunciations']['homophones'] = element.split(", ")

            # # If IPA entry doesn't exist
            # if "Homophone" in parsedHomophone['pronunciations']['text'][0]:
            #     # print("Doesn't have IPA, has Homophones")
            #     parsedHomophone['pronunciations']['IPA'] = None
            #     parsedHomophone['pronunciations']['homophones'] = parsedHomophone['pronunciations']['text'][0].split(", ")
        except (IndexError, KeyError) as err:
            print("Error in pronunciations input.")
            print(err)

        if not parsedHomophone['pronunciations']['homophones']:
            print("Entry doesn't have homophones!")
            with open("failed.txt", "a+", encoding="utf8", errors='ignore') as failed:
                failed.write(f"No homophones: {word}\n")
            return None

        # Delete "text" key from "pronunciations" value
        parsedHomophone['pronunciations'].pop('text', None)

        # DEFINITIONS
        for i, pOS in enumerate(parsedHomophone['definitions']):
            try:
                # Split "text" value from "definitions" key into keys "word" and "meanings"
                parsedHomophone['definitions'][i]['meanings'] = parsedHomophone['definitions'][i]['text'][1:]
            except (IndexError, KeyError) as err:
                print("Error in definitions input.")
                print(err)

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
                except (IndexError, TypeError, AttributeError):
                    print("No infinitive form.")
            else:
                parsedHomophone['definitions'][i]['infinitive'] = None

            # Remove "text" value from definitions key
            word = parsedHomophone['definitions'][i].pop('text', None)
    except KeyboardInterrupt:
        raise KeyboardInterruptError()

    # Put dictionary after "word" key
    homophone.update(parsedHomophone)
    return homophone


def request_homophones_wiktionary():
    """ Read french_homophones.txt to request words' informations with WiktionaryParser.

        Write to homophones.txt.
    """

    with open("french_homophones.txt", "r+", encoding="utf8", errors='ignore') as fHomophones:
        with open("homophones.txt", "a+", encoding="utf8", errors='ignore') as fOut:
            words = fHomophones.readlines()

            with Pool(10) as p:
                try:
                    fetchedHomophones = list(p.map(fetch_wiktionary_word, words))
                except KeyboardInterrupt:
                    print('Got ^C while pool mapping, terminating the pool')
                    p.terminate()
                    print('Terminating pool...')
                    p.terminate()
                    p.join()
                    print('Done!')

            for fetchedHomophone in fetchedHomophones:
                fOut.write(f"{fetchedHomophone}\n")


if __name__ == "__main__":
    request_homophones_wiktionary()
