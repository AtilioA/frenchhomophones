import random
from .extensions import mongo
from .fetch_wiktionary_word import fetch_wiktionary_word

from flask import Blueprint, render_template, url_for, request

main = Blueprint('main', __name__)


def find_document(word):
    user_collection = mongo.db.users

    query = {"word": word}
    doc = user_collection.find_one(query)

    print(doc)
    return doc


def find_random_document(user_collection):
    """ Returns random homophone from the database """
    cursor = user_collection.aggregate([
        {"$sample": {"size": 1}}
    ])
    return list(cursor)


@main.route('/', methods=['GET', 'POST'])
def index():
    # Connects to database collection. Creates one if it doesn't exist
    user_collection = mongo.db.homophones

    # For querying the database through the website
    if request.method == 'POST':
        word_query = request.form.get('word').strip().lower()
        cursor = user_collection.find({"word": word_query})
        try:
            homophone = dict(cursor)
        except IndexError:  # No entry was found in the database
            return render_template("notfound.html", word=word_query)
    else:
        # Placeholder. Will show random homophones in the index page

        homophone = user_collection.find_one({"word": "faire"})
        homophonesList = [homophone]
        # print(homophone)
        for homophone in homophone["homophones"]:
            print(f"Querying {homophone.strip()}...")
            homophonesList.append(user_collection.find(
                {"word": homophone.strip()}))

        # try:
        #     # homophonesList = list(map(dict, homophonesList))
        # except:
        #     pass
        # homophonesList = [list(x) for x in homophonesList if homophonesList]
        print(homophonesList)

    return render_template("index.html", homophones=homophonesList)


@main.route('/find')
def find():
    pass


@main.route('/random')
def random():
    user_collection = mongo.db.homophones

    homophone = find_random_document(user_collection)[0]
    try:
        root = homophone["root"].strip()
        print(f"\n\nFetching root: {root}")
        dictRoot = fetch_wiktionary_word(root)
        print(f"Root dictionary: {dictRoot}")
        homophone["rootWord"] = dictRoot
        # print(homophone)
    except:
        pass
    homophonesList = [homophone]

    for otherHomophone in homophone["homophones"]:
        print(f"Querying {otherHomophone.strip()}...")
        wordQueryResult = list(user_collection.find({"word": otherHomophone.strip()}))
        print(f"query: {wordQueryResult}")
        # print(f"list: {list(wordQueryResult)}")

        # try:
        #     # wordQueryResult = list(wordQueryResult)[0]
        # except:
        #     pass
        
        if not wordQueryResult:
            continue
        else:
            try:
                root = wordQueryResult[0]["root"].strip()
                print(f"\n\nFetching root: {root}")
                dictRoot = fetch_wiktionary_word(root)
                print(f"Root dictionary: {dictRoot}")
                wordQueryResult[0]["rootWord"] = dictRoot
                print(wordQueryResult[0])
            except:
                pass
            homophonesList.append(wordQueryResult[0])

    return render_template("homophones.html", homophones=homophonesList)



@main.route("/about/")            
def about():
    return render_template("about.html")
