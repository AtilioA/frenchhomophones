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
    db = client.test
    homophonesCollection = db.test
    print("Connected to database.")

    # print(parsedHomophone)
    # homophonesCollection.insert_one(parsedHomophone)
    # with open("homophones.txt", "r+", encoding="utf8") as f:
        # Read .txt and append entries (as dictionaries) to list
        # dictList = []
        # for line in f:
        #     wordDict = literal_eval(line)
        #     dictList.append(wordDict)

        # Insert whole list of dictionaries in one call
        # insertedResult = homophonesCollection.insert_many(dictList)
    
        # print(f"{len(insertedResult.inserted_ids)} documents inserted.")
        # return len(insertedResult.inserted_ids)
    pass


if __name__ == "__main__":
    populate_db()
    pass
