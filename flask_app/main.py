import random
from .extensions import mongo
from .utils.fetch_wiktionary_word import fetch_wiktionary_word

from flask import Blueprint, render_template, url_for, request
# from flask_wtf import FlaskForm
# from wtforms import StringField

main = Blueprint('main', __name__)


def find_one_random_document(user_collection):
    """ Returns random noun homophone from the database. """

    cursor = user_collection.aggregate(
    [
        {"$match": { "partOfSpeech": "noun" } },
        {"$sample": {"size": 1 } }
    ])

    return list(cursor)[0]


def determine_audio_URL_homophones(homophonesList):
    """ Returns audio URL for list of homophones.

        Returns first audio file from Wiktionary from the list of homophones.

        If no audio is available, requests from google translate
        (Request URL may break anytime).
    """

    # Find any audio file from list of homophones
    # If not available, get from Google Translate (this URL may break anytime)
    audio = f"//translate.google.com.vn/translate_tts?ie=&q={homophonesList[0]['word']}&tl=fr-fr&client=tw-ob"
    for homophone in homophonesList:
        if homophone["audio"]:
            audio = homophone["audio"]
            break

    return audio


def create_homophones_list(query="", random=False):
    """ Returns list with queried word (if applicable) and its homophones.

        Until infinitive forms are stored in the database,
        will look up with WiktionaryParser during execution.

        Optional keyword arguments:

        `random`: will use a random homophone as starting point
        if `random` is set to True.
    """

    # Connects to database collection. Creates one if it doesn't exist
    user_collection = mongo.db.homophones

    homophonesList = []

    if random:
        homophone = find_one_random_document(user_collection)
    else:
        homophone = user_collection.find_one({"word": query.strip()})
        if homophone is None:
            return render_template("notfound.html", word=query)

        # Look for infinitive form if it's a verb
        try:
            if homophone["partOfSpeech"] == "verb":
                root = homophone["root"].strip()
                print(f"\n\nFetching root: {root}")
                dictRoot = fetch_wiktionary_word(root)
                print(f"Root dictionary: {dictRoot}")
                homophone["rootWord"] = dictRoot
        except:
            pass

    # Create list querying all homophones
    homophonesList.append(homophone)
    for otherHomophone in homophone["homophones"]:
        try:
            print(f"Querying {otherHomophone.strip()}...")
            wordQueryResult = user_collection.find_one({"word": otherHomophone.strip()})
            print(f"query: {wordQueryResult}")
        except:
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
            except:
                pass

        homophonesList.append(wordQueryResult)

    return homophonesList


@main.route('/', methods=['GET'])
def index():
    # Connects to database collection. Creates one if it doesn't exist
    user_collection = mongo.db.homophones
    
    return render_template("index.html")


@main.route("/find")
def find():
    user_collection = mongo.db.homophones

    query = request.args['search'].strip()
    homophonesList = create_homophones_list(query)

    audio = determine_audio_URL_homophones(homophonesList)

    return render_template("homophones.html", homophones=homophonesList, audio=audio)


@main.route("/random/", methods=['GET'])
def random():
    # Connects to database collection. Creates one if it doesn't exist    
    user_collection = mongo.db.homophones
    
    homophonesList = create_homophones_list(random=True)
    print(homophonesList)
    
    audio = determine_audio_URL_homophones(homophonesList)

    return render_template("homophones.html", homophones=homophonesList, audio=audio)


@main.route("/about/", methods=['GET'])            
def about():
    # Connects to database collection. Creates one if it doesn't exist    
    user_collection = mongo.db.homophones
            
    return render_template("about.html")
