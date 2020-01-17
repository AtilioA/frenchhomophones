import os
import sys
from typing import Collection

# Needed to execute this package as a script
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))

# MongoDB
# from flask_pymongo import PyMongo
from pymongo import MongoClient
MONGO_URI = os.environ.get("MONGO_URI")

from .fetch_wiktionary_word import fetch_wiktionary_word


def find_one_random_document():
    """ Return dict for random noun homophone from the database. """

    # Connect to database
    client = MongoClient(MONGO_URI)
    db = client.frenchhomophones
    user_collection = db.homophones

    cursor = user_collection.aggregate(
        [
            {"$match": {"partOfSpeech": "noun"}},
            {"$sample": {"size": 1}}
        ])

    return list(cursor)[0]


def find_nth_document(n):
    """ Return nth document from database (insertion order). """

    # Connect to database
    client = MongoClient(MONGO_URI)
    db = client.frenchhomophones
    user_collection = db.homophones

    return list(user_collection.find().limit(n))[-1]


def determine_audio_URL_homophones(homophonesList):
    """ Return audio URL for list of homophones.

        Return first audio file from Wiktionary from the list of homophones.

        If no audio is available, request from google translate
        (Request URL may break anytime).
    """

    # Find any audio file from list of homophones
    # If not available, get from Google Translate (this URL may break anytime)
    audio = f"//translate.google.com.vn/translate_tts?ie=&q={homophonesList[0]['word']}&tl=fr-fr&client=tw-ob"
    for homophone in homophonesList:
        if homophone["audio"]:
            audio = homophone["audio"]
            break

    print(audio)
    return audio


def create_homophones_list(query="", random=False):
    """ Return list with queried word (if applicable) and its homophones.

        Until infinitive forms are stored in the database,
        will look up with WiktionaryParser during execution.

        Optional keyword arguments:

        `random`: will use a random homophone as starting point
        if set to `True`.
    """

    # Connects to database collection. Creates one if it doesn't exist
    client = MongoClient(MONGO_URI)
    db = client.frenchhomophones
    user_collection = db.homophones

    homophonesList = []

    if random:
        homophone = find_one_random_document()
    else:
        homophone = user_collection.find_one({"word": query.strip()})
        if homophone is None:
            return None

        # Look for infinitive form if it's a verb
        try:
            if homophone["partOfSpeech"] == "verb":
                root = homophone["root"].strip()
                print(f"\n\nFetching root: {root}")
                dictRoot = fetch_wiktionary_word(root)
                print(f"Root dictionary: {dictRoot}")
                homophone["rootWord"] = dictRoot
                print(homophone)
        except (TypeError, AttributeError):
            print("Couldn't fetch infinitive form")

    # Create list querying all homophones
    homophonesList.append(homophone)
    for otherHomophone in homophone["homophones"]:
        try:
            print(f"Querying {otherHomophone.strip()}...")
            wordQueryResult = user_collection.find_one(
                {"word": otherHomophone.strip()})
            print(f"query: {wordQueryResult}")
        except TypeError:  # If the query return None
            wordQueryResult = None

        # If didn't find in the database, proceed to next iteration
        if not wordQueryResult:
            continue
        else:
            # Look for infinitive form if it's a verb
            try:
                if wordQueryResult["partOfSpeech"] == "verb":
                    root = wordQueryResult["root"].strip()
                    print(f"\n\nFetching root: {root}")
                    dictRoot = fetch_wiktionary_word(root)
                    print(f"Root dictionary: {dictRoot}")
                    wordQueryResult["rootWord"] = dictRoot
                    print(wordQueryResult)
            except (TypeError, AttributeError):
                print("Couldn't fetch infinitive form")

        homophonesList.append(wordQueryResult)

    return homophonesList
