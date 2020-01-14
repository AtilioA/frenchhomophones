import random
from .extensions import mongo
from .fetch_wiktionary_word import fetch_wiktionary_word

from flask import Blueprint, render_template, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField

main = Blueprint('main', __name__)

class SearchForm(FlaskForm):
    searchQuery = StringField('searchQuery')


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

    if request.method == 'POST':
        try:
            print("\n")
            wordQuery = request.form.get('wordQuery').strip()
            print(wordQuery)
            homophone = list(user_collection.find({"word": wordQuery}))[0]
            print(homophone)
        except:
            return render_template("notfound.html", word=wordQuery)

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
    
    return render_template("index.html")


@main.route("/find/")
def find():
    return render_template("index.html")
    pass


@main.route("/random/", methods=['GET', 'POST'])
def random():
    user_collection = mongo.db.homophones
    # form = SearchForm()

    if request.method == 'POST':
        try:
            print("\n")
            wordQuery = request.form.get('wordQuery').strip()
            print(wordQuery)
            homophone = list(user_collection.find({"word": wordQuery}))[0]
            print(homophone)
        except:
            return render_template("notfound.html", word=wordQuery)
    else:
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


@main.route("/about/", methods=['GET', 'POST'])            
def about():
    user_collection = mongo.db.homophones

    if request.method == 'POST':
        try:
            print("\n")
            wordQuery = request.form.get('wordQuery').strip()
            print(wordQuery)
            homophone = list(user_collection.find({"word": wordQuery}))[0]
            print(homophone)
        except:
            return render_template("notfound.html", word=wordQuery)

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
            
    return render_template("about.html")


@main.route("/timothee/")
def timothee():
    return "<h1>Amada??</h1> <script>alert(\"Amada??\")</script>"
