import re
import random
from wiktionaryparser import WiktionaryParser
# Initialize parser
parser = WiktionaryParser()
# wiktionaryDomain = "https://en.wiktionary.org"

# print(parser.fetch("dépolymériser", "french"))


def print_word_definition(i, homophone):
    # parser.set_default_language('french')
    parsedHomophone = parser.fetch(homophone, "french")
    
    # print(parsedHomophone)
    try:
        wordText = homophone  # parsedHomophone[0]["definitions"][0]["text"][0]
        partOfSpeech = parsedHomophone[0]["definitions"][0]["partOfSpeech"]
        wordDefinitions = parsedHomophone[0]["definitions"][0]["text"][1:]
        sentenceExamples = parsedHomophone[0]["definitions"][0]["examples"]
        
        print(f"Word: {wordText}")
        print(f"Part of speech: {partOfSpeech}")
        
        print(f"Definitions:")
        for i, definition in enumerate(wordDefinitions):
            print(f"{i + 1}. {definition}")
            
        if sentenceExamples:
            print(f"Examples:")
            for sentence in sentenceExamples:
                print(f"\t{sentence}")
            
        match = re.search(r"person.* of (\w+)$", str(wordDefinitions[0]))
        if match:
            print(f"\nRetrieving root ({match.group(1)}) definition:")
            print_word_definition(0, match.group(1))
    except:
        pass
    pass


if __name__ == "__main__":
    with open("french_homophones.txt", "r+", encoding="utf8") as f:
        words = f.readlines()
        
        randomHomophone = random.choice(words).strip()
        print(f"The random homophone is \"{randomHomophone}\"")
        
        parsedHomophone = parser.fetch(randomHomophone, "french")
        # print(parsedHomophone)
        word = parsedHomophone[0]["definitions"][0]["text"][0]
        partOfSpeech = parsedHomophone[0]["definitions"][0]["partOfSpeech"]
        wordDefinitions = parsedHomophone[0]["definitions"][0]["text"][1:]
        sentenceExamples = parsedHomophone[0]["definitions"][0]["examples"]
        
        ipaHomophones = parsedHomophone[0]["pronunciations"]['text']
        if len(ipaHomophones) > 1:  # Has IPA and homophones
            ipa = ipaHomophones[0]
            homophones = ipaHomophones[1]
        else:
            homophones = ipaHomophones[0]
        homophones = homophones[12:].split(',')
        
        pronunciations = parsedHomophone[0]["pronunciations"]
        audio = parsedHomophone[0]["pronunciations"]['audio']
        # print(pronunciations)
        
        print(f"\nWord: {word}")
        print(f"Part of speech: {partOfSpeech}")
        
        print(f"Definitions:")
        for i, definition in enumerate(wordDefinitions):
            print(f"{i + 1}. {definition}")
            
        if sentenceExamples:
            print(f"Examples:")
            for sentence in sentenceExamples:
                print(f"\t{sentence}")
                
        match = re.search(r"of (\w+)$", str(wordDefinitions[0]))
        if match:
            print(f"\nRetrieving root ({match.group(1)}) definition:")
            print_word_definition(0, match.group(1))
            print()
        
        print(f"Homophones: {homophones}")
        try:
            print(ipa)
        except:
            # print("IPA is unavailable.")
            pass
        
        if audio:
            print(f"Audio URL: https://{audio[0][2:]}")
        else:
            print("Audio is unavailable.")
            
        print("--------------------------------------")
        print("Retrieving homophones' definitions:")
        for i, homophone in enumerate(homophones):
            print(f"\nHomophone: {homophone.strip()}\n")
            print_word_definition(i, homophone.strip())
    pass
