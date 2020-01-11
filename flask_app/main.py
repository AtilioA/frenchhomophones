import random

from flask import Blueprint, render_template, url_for

from wiktionaryparser import WiktionaryParser
# Initialize parser
parser = WiktionaryParser()

from .extensions import mongo 

main = Blueprint('main', __name__)

@main.route('/')
def index():
    user_collection = mongo.db.homophones
    # user_collection.insert({'name' : 'Cristina'})
    # user_collection.insert({'name' : 'Derek'})

    with open("french_homophones.txt", "r+", encoding="utf8") as f:
        words = f.readlines()
    randomHomophone = random.choice(words).strip()
    print(randomHomophone)
        
    parsedHomophone = parser.fetch("faire", "french")
    print(f"The random homophone is \"{randomHomophone}\"")
    print(parsedHomophone)

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
        try:
            match = re.search(r"of (\w+)$", str(wordDefinitions[0]))
            root = parser.fetch(match.group(1), "french")
            # print(root)
            # print(match.group(1))
        except:
            root = None
            pass
        
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
    except:
        homophone = None

    print("HOMOPHONE:")
    print(homophone)
    user_collection.insert(homophone)
        
    return render_template("index.html", homophone=homophone)
