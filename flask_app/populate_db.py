import re
from wiktionaryparser import WiktionaryParser
# Initialize parser
parser = WiktionaryParser()

with open("french_homophones.txt", "r+", encoding="utf8") as fHomophones:
    with open("homophones.txt", "a+", encoding="utf8") as fOut:
        words = fHomophones.readlines()
        for word in words[2:50]:
            parsedHomophone = parser.fetch(word.strip(), "french")
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
                # print(wordDefinitions[0])
                try:
                    match = re.search(r"of (\w+)$", str(wordDefinitions[0].strip()))
                    root = match.group(1)
                    # root = parser.fetch(match.group(1).strip(), "french")
                except:
                    root = None
                    pass

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
                'root': root
                }
                # print(homophone)
                fOut.write(f"{homophone}\n")
            except:
                print("NAO ESCREVI.\n\n")
                homophone = None
