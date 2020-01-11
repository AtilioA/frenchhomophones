import re
import json 

from wiktionaryparser import WiktionaryParser
parser = WiktionaryParser()
from ast import literal_eval

from flask import Blueprint, render_template, url_for

from flask_pymongo import PyMongo 
from pymongo import MongoClient
mongo = PyMongo()
connection = MongoClient()

main = Blueprint('main', __name__)


def populate_db():
    client = MongoClient('mongodb+srv://atilioa:obBpW3F0j8rQy@cluster0-iqyn6.gcp.mongodb.net/test?retryWrites=true&w=majority')
    db = client.test
    homophones = db.homophones
    print("Connected to database.")

    with open("homophones.txt", "r+", encoding="utf8") as f:
        listDict = []
        for line in f:
            your_dict = literal_eval(line)
            listDict.append(your_dict)

        inserted = db.homophones.insert_many(listDict)

        print(f"\n{len(inserted)} documents inserted.\n")


def request_wiktionary():
    with open("french_homophones.txt", "r+", encoding="utf8") as fHomophones:
        with open("homophones.txt", "a+", encoding="utf8") as fOut:
            words = fHomophones.readlines()
            for word in words[3:]:
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
                    try:
                        match = re.search(r"of (\w+):?$", str(wordDefinitions[0].strip()))
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
                    print(homophone)
                    fOut.write(f"{homophone}\n")
                except:
                    pass


if __name__ == "__main__":
    populate_db()
