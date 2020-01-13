from wiktionaryparser import WiktionaryParser
parser = WiktionaryParser()

def fetch_wiktionary_word(word):
    """ Read french_homophones.txt to request words' informations with WiktionaryParser
        Write relevant structured information to homophones.txt
    """
    parsedHomophone = parser.fetch(word.strip(), "french")

    # Treat each information accordingly
    try:
        ipaHomophones = parsedHomophone[0]["pronunciations"]['text']
        if len(ipaHomophones) > 1:  # Has IPA and homophones
            ipa = ipaHomophones[0]
            homophones = ipaHomophones[1]
        else:
            ipa = None
            homophones = ipaHomophones[0]
        homophones = homophones[11:].split(',')

        wordDefinitions = parsedHomophone[0]["definitions"][0]["text"][1:]

        # try:
        #     # ipa = re.sub(r".*IPA:\s*", "", ipa)
        # except:
        #     ipa = None

        homophones[0] = homophones[0].strip()

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

    except:
        pass
