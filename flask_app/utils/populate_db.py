import os
import time
import urllib.parse
from pymongo import MongoClient
# To read dictionaries from txt
from ast import literal_eval
# To get structured data from Wiktionary
from multiprocessing import Pool

from wiktionaryparser import WiktionaryParser
parser = WiktionaryParser()

# MongoDB
MONGO_URI = os.environ.get("MONGO_URI")

# Connects to database collection. Creates one if it doesn't exist
client = MongoClient(MONGO_URI)
db = client.frenchhomophones
homophonesCollection = db.homophones
print("Connected to database.")


def process_missing_homophone(Homophone):
    try:
        with open("missing.txt", "a+", encoding="utf8", errors='ignore') as f:
            for homophone in Homophone['pronunciations']['homophones']:
                if homophonesCollection.find_one({"word": f"{homophone}"}) is None:
                    print(f"{homophone} is missing. Logging...")
                    f.write(f"{homophone}\n")
    except KeyError:
        print("fds")


def log_missing_homophones():
    allHomophones = list(homophonesCollection.find())

    with Pool(10) as p:
        p.map(process_missing_homophone, allHomophones)
    print("Logged all missing homophones.")


def populate_db():
    """ Insert information from homophones.txt in the database.

    Return the number of inserted documents.
    """

    with open("homophones.txt", "r+", encoding="utf8", errors='ignore') as f:
        # Read .txt and append entries (as dictionaries) to list
        dictList = []
        for line in f:
            wordDict = literal_eval(line)
            dictList.append(wordDict)

        # Insert whole list of dictionaries in one call
        insertedResult = homophonesCollection.insert_many(dictList)

        print(f"{len(insertedResult.inserted_ids)} documents inserted.")
        return len(insertedResult.inserted_ids)


if __name__ == "__main__":
    # populate_db()
    # log_missing_homophones()
    pass
