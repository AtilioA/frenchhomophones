import random

from flask import Blueprint, render_template, url_for

from wiktionaryparser import WiktionaryParser
# Initialize parser
parser = WiktionaryParser()

from .extensions import mongo 

main = Blueprint('main', __name__)


def findRandomDocument(user_collection):
    cursor = user_collection.aggregate([
        { "$sample": { "size": 1 } }
    ])
    return list(cursor)


@main.route('/')
def index():
    user_collection = mongo.db.homophones

    homophone = findRandomDocument(user_collection)[0]
    print(type(homophone))
    print(homophone)

    # cursor = user_collection.find({"word": "abader"})
    # homophone = list(cursor)[0]

    return render_template("index.html", homophone=homophone)


@main.route('/find')
def find():
    pass


@main.route("/about/")            
def about():
    return render_template("about.html")


def find_document(word):
    user_collection = mongo.db.users

    query = {"word": f"{word}" }
    doc = user_collection.find(myquery)
    
    return "fodase"
