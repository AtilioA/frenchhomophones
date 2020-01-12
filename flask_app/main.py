import random

from flask import Blueprint, render_template, url_for, request

from wiktionaryparser import WiktionaryParser
# Initialize parser
parser = WiktionaryParser()

from .extensions import mongo 

main = Blueprint('main', __name__)


def find_document(word):
    user_collection = mongo.db.users

    query = {"word": word}
    doc = user_collection.find(query)
    
    print(doc)
    return doc


def findRandomDocument(user_collection):
    """ Returns random homophone from the database """
    cursor = user_collection.aggregate([
        { "$sample": { "size": 1 } }
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
            homophone = list(cursor)[0]
        except IndexError:  # No entry was found in the database
            return render_template("notfound.html", word=word_query)
    else:
        # Placeholder. Will show random homophones in the index page
        homophone = findRandomDocument(user_collection)[0]

    return render_template("index.html", homophone=homophone)


@main.route('/find')
def find():
    pass


@main.route("/about/")            
def about():
    return render_template("about.html")
