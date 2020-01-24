import os
import re
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))

from multiprocessing import Pool

from wiktionaryparser import WiktionaryParser
parser = WiktionaryParser()

from controllers import Homophones


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

        if not (parsedHomophone["definitions"] or parsedHomophone["etymology"] or parsedHomophone["pronunciations"]["text"]):
            with open("failed.txt", "a+", encoding="utf8") as failed:
                failed.write(f"{word}\n")
            print("Word not found.")
            # print(parsedHomophone)
            pass

        # PRONUNCIATIONS
        parsedHomophone['pronunciations']['homophones'] = None
        try: 
            # If IPA entry exists
            if "IPA" in parsedHomophone['pronunciations']['text'][0]:
                # print("Has IPA")
                parsedHomophone['pronunciations']['IPA'] = parsedHomophone['pronunciations']['text'][0]
                for element in parsedHomophone['pronunciations']['text']:
                    if "Homophone" in element:
                        # print("Has Homophones")
                        parsedHomophone['pronunciations']['homophones'] = element.split(", ")
                        break

            # If IPA entry doesn't exist
            elif "Homophone" in parsedHomophone['pronunciations']['text'][0]:
                # print("Doesn't have IPA, has Homophones")
                parsedHomophone['pronunciations']['IPA'] = None
                parsedHomophone['pronunciations']['homophones'] = parsedHomophone['pronunciations']['text'][0].split(", ")
            else:
                # print(parsedHomophone['pronunciations']['text'][0][:8])
                print("\n!Something wrong is not right!\n")
        except (IndexError, KeyError) as err:
            print("Error in pronunciations input.")
            print(err)

        if not parsedHomophone['pronunciations']['homophones']:
            print("Entry doesn't have homophones!")
            with open("failed2.txt", "a+", encoding="utf8") as failed:
                failed.write(f"No homophones: {word}\n")

        # Delete "text" key from "pronunciations" value
        parsedHomophone['pronunciations'].pop('text', None)
        
        # DEFINITIONS
        for i, pOS in enumerate(parsedHomophone['definitions']):
            try:
                # Split "text" value from "definitions" key into keys "word" and "meanings"
                # parsedHomophone['word'] = parsedHomophone['definitions'][i]['text'][0]
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

    homophone.update(parsedHomophone)
    return homophone


def request_homophones_wiktionary():
    """ Read french_homophones.txt to request words' informations with WiktionaryParser.

        Write to homophones.txt.
    """

    with open("french_homophones.txt", "r+", encoding="utf8") as fHomophones:
        with open("homophones.txt", "a+", encoding="utf8") as fOut:
            words = fHomophones.readlines()
            
            with Pool(10) as p:
                try:
                    fetchedHomophones = list(p.map(fetch_wiktionary_word, words[25000:]))
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
