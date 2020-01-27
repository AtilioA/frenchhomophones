from pymongo import MongoClient
import os

from flask import Blueprint, render_template, send_from_directory, request, redirect, jsonify

from .controllers import create_homophones_list, find_nth_document, find_one_random_document

views = Blueprint('views', __name__)
MONGO_URI = os.environ.get("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client.frenchhomophones
userCollection = db.homophones

@views.route('/<path:urlpath>/', methods=['GET', 'POST'])  # Catch all undefined routes
@views.route('/', methods=['GET'])
def index(urlpath='/'):
    """ Homepage of the web application. """

    homophonesLists = []
    audiosList = []
    for i in range(4):
        homophonesLists.append(create_homophones_list(userCollection=userCollection, random=True))
        audiosList.append(homophonesLists[i].audio)

    return render_template("index.html", homophonesLists=homophonesLists, audios=audiosList)


@views.route("/find")
def find(query=""):
    """ Handle query from users. """

    query = request.args['search'].strip().lower()
    return redirect(f"/h/{query}")


@views.route("/random/", methods=['GET'])
def random_route():
    """ Retrieve random document from database to be shown to the user. """

    randomHomophone = find_one_random_document(userCollection)
    print(randomHomophone)

    query = randomHomophone['word'].lower()

    for string in randomHomophone['pronunciations']['homophones']:
        query = f'{query}-{string.lower()}'
    return redirect(f"/h/{query}")


@views.route("/about/", methods=['GET'])
def about():
    """ About section of the web application. """

    return render_template("about.html")


@views.route("/h/<homophoneID>", methods=['GET'])
def h(homophoneID):
    """ Homophones's pages route """

    print(homophoneID)
    # print(homophoneID.isdigit())
    if homophoneID.isdigit():
        nthDocument = find_nth_document(userCollection, int(homophoneID))
        # print(nthDocument['word'])
        if nthDocument:
            wordRoute = nthDocument['word']
            # print(nthDocument['pronunciations']['homophones'])
            for string in nthDocument['pronunciations']['homophones']:
                wordRoute = f'{wordRoute}-{string}'

            return redirect(f'/h/{wordRoute.strip()}')
        else:
            return render_template("notfound.html", word=homophoneID)
    else:
        homophoneID = homophoneID.split("-")[0]
        # print(homophoneID)
        homophones = create_homophones_list(userCollection=userCollection, query=homophoneID)
        if not homophones:
            return render_template("notfound.html", word=homophoneID)

        return render_template("homophones.html", homophones=homophones.homophonesList, audio=homophones.audio, ipa=homophones.ipa)


@views.route("/robots.txt/")
def robots():
    """ Send robots.txt. """
    return send_from_directory("static", "robots.txt")


def determine_pagination_urls(offset, limit):
    if offset - limit < 0:
        prevURL = None
    else:
        prevURL = f'/p/?limit={limit}&offset={offset - limit}'

    if offset + limit >= userCollection.count_documents({}):
        nextURL = None
    else:
        nextURL = f'/p/?limit={limit}&offset={offset + limit}'

    return (prevURL, nextURL)


@views.route("/browse")
def browse():
    if request.args:
        limit = int(request.args['limit'])
        offset = int(request.args['offset'])
    else:
        limit = 12
        offset = 0

    nthDocument = find_nth_document(userCollection, offset)
    nthID = nthDocument['_id']

    homophonesLists = []
    words = userCollection.find({'_id': {'$gte': nthID}}).limit(limit)
    for i in range(limit):
        try:
            homophonesLists.append(create_homophones_list(userCollection, query=words[i]["word"]))
        except IndexError:
            pass
    print(homophonesLists)

    totalPages = (userCollection.count_documents({}) // limit) + 1
    currentPage = (offset // limit) + 1
    prevURL, nextURL = determine_pagination_urls(offset, limit)

    return render_template("browse.html", offset=offset, limit=limit, prevURL=prevURL, nextURL=nextURL, totalPages=totalPages, currentPage=currentPage, homophonesLists=homophonesLists)
