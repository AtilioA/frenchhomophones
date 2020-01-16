import os
import re

# from __future__ import absolute_import
# from flask_pymongo import PyMongo
from pymongo import MongoClient
# To read dictionaries from txt
from ast import literal_eval
# To get structured data from Wiktionary
from wiktionaryparser import WiktionaryParser
parser = WiktionaryParser()

# MongoDB
MONGO_URI = os.environ.get("MONGO_URI")


def clean_IPA_string(IPAString: str) -> str:
    """ Clean the IPA string provided by WiktionaryParser.

    Return the cleaned string.
    """

    return re.sub(r"(?:^.*IPA:.*?(?=/))|'", "", IPAString)


def populate_db():
    """ Insert information from homophones.txt in the database.

    Return the number of inserted documents.
    """
    
    # Connects to database collection. Creates one if it doesn't exist
    client = MongoClient(MONGO_URI)
    db = client.frenchhomophones
    homophonesCollection = db.homophones
    print("Connected to database.")

    with open("homophones.txt", "r+", encoding="utf8") as f:
        # Read .txt and append entries (as dictionaries) to list
        dictList = []
        for line in f:
            wordDict = literal_eval(line)
            dictList.append(wordDict)

        # Insert whole list of dictionaries in one call
        insertedResult = homophonesCollection.insert_many(dictList)

        print(f"{len(insertedResult.inserted_ids)} documents inserted.")
        return len(insertedResult.inserted_ids)


def request_wiktionary():
    """ Read french_homophones.txt to request words' informations with WiktionaryParser.

        Write relevant structured information to homophones.txt.
    """

    # with open("french_homophones.txt", "r+", encoding="utf8") as fHomophones:
    #     with open("homophones.txt", "a+", encoding="utf8") as fOut:
    #         words = fHomophones.readlines()
    #         for word in words:
    #             parsedHomophone = parser.fetch(word.strip(), "french")

    #             homophone = {
    #                  'word': parsedHomophone[0]["definitions"][0]["text"][0],
    #                  'partOfSpeech': parsedHomophone[0]["definitions"][0]["partOfSpeech"],
    #                  'wordDefinitions': parsedHomophone[0]["definitions"][0]["text"][1:],
    #                  'sentenceExamples': parsedHomophone[0]["definitions"][0]["examples"],
    #                  'audio': audio,
    #                  'homophones': homophones,
    #                  'ipa': ipa,
    #                  'infinitive': infinitive
    #             }
    #             print(homophone)

    #             fOut.write(f"{homophone}\n")
    pass


if __name__ == "__main__":
    # populate_db()
    pass
