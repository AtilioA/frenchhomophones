from pymongo import MongoClient
import os
import sys

# Needed to execute this package as a script
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))

# MongoDB
# from flask_pymongo import PyMongo
MONGO_URI = os.environ.get("MONGO_URI")


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
        if homophone["pronunciations"]["audio"]:
            audio = homophone["pronunciations"]["audio"]
            print(audio)
            return audio


def find_one_random_document():
    client = MongoClient(MONGO_URI)
    db = client.test
    user_collection = db.test

    cursor = user_collection.aggregate([
        { "$sample": { "size": 1 } }
    ])

    return list(cursor)


def find_nth_document(n):
    """ Return nth document from database (insertion order). """

    # Connect to database collection. Create one if it doesn't exist
    client = MongoClient(MONGO_URI)
    db = client.test
    user_collection = db.test

    return list(user_collection.find().limit(n))[-1]


def create_homophones_list(query="", random=False):
    """ Return list with queried word (if applicable) and its homophones.

        Until infinitive forms are stored in the database,
        will look up with WiktionaryParser during execution.

        Optional keyword arguments:

        `random`: will use a random homophone as starting point
        if set to `True`.
    """

    # Connect to database collection. Create one if it doesn't exist
    client = MongoClient(MONGO_URI)
    db = client.test
    user_collection = db.test

    homophonesList = []

    if random:
        homophone = find_one_random_document()
    else:
        homophone = user_collection.find_one({"word": query.strip()})
        if homophone is None:
            return None

    # Create list querying all homophones
    homophonesList.append(homophone)
    for otherHomophone in homophone["pronunciations"]["homophones"]:
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

        homophonesList.append(wordQueryResult)

    homophones = Homophones(homophonesList)

    return homophones


class Homophones:
    def __init__(self, homophonesList):
        self.homophonesList = homophonesList
        
        audio = self.determine_audio_URL(homophonesList)
        try:
            self.audio = audio[0]
        except TypeError:
            self.audio = audio
            
        self.ipa = self.determine_ipa(homophonesList)

    def determine_ipa(self, homophonesList):
        """ Return IPA for list of homophones.

            Return first IPA string from Wiktionary from the list of homophones.

            If no IPA is available, return `None`
        """

        # Find any IPA string from list of homophones
        for homophone in homophonesList:
            if homophone["pronunciations"]["IPA"]:
                ipa = homophone["pronunciations"]["IPA"]
                print(ipa)
                return ipa
        return None

    def determine_audio_URL(self, homophonesList):
        """ Return audio URL for list of homophones.

            Return first audio file from Wiktionary from the list of homophones.

            If no audio is available, request from google translate
            (Request URL may break anytime).
        """

        # Find any audio file from list of homophones
        # If not available, get from Google Translate (this URL may break anytime)
        audio = f"//translate.google.com.vn/translate_tts?ie=&q={homophonesList[0]['word']}&tl=fr-fr&client=tw-ob"
        for homophone in homophonesList:
            if homophone["pronunciations"]["audio"]:
                audio = homophone["pronunciations"]["audio"]
                print(audio)
                return audio
