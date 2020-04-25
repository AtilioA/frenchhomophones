import os

from pymongo import MongoClient
from flask import Blueprint, render_template, send_from_directory, request, redirect, jsonify

from .controllers import create_homophones_list, find_nth_document, find_one_random_document, get_current_browse_page_homophones, define_limit_offset, define_pagination_variables

views = Blueprint('views', __name__)

MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.frenchhomophones
homophonesCollection = db.homophones  # Will be replaced by homophonesGroupColection
homophonesGroupCollection = db.homophonesGroup

HOMEPAGE_N_RANDOM_HOMOPHONES = 4  # Number of random homophones groups shown at homepage


# Catch all undefined routes
@views.route('/<path:urlpath>/', methods=['GET', 'POST'])
@views.route('/', methods=['GET'])
def index(urlpath='/'):
    """ Homepage of the web application. """

    homophonesLists = []
    audiosList = []
    for i in range(HOMEPAGE_N_RANDOM_HOMOPHONES):
        homophonesLists.append(create_homophones_list(
            homophonesCollection=homophonesCollection, random=True))
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

    randomHomophone = find_one_random_document(homophonesCollection)
    # print(randomHomophone)

	# STUB: WILL BE REFACTORED
    query = randomHomophone['word'].lower()

    for string in randomHomophone['pronunciations']['homophones']:
        query = f'{query}-{string.lower()}'
    return redirect(f"/h/{query}")


@views.route("/about/", methods=['GET'])
def about():
    """ About section of the web application. """

    return render_template("about.html")


# STUB: WILL BE REFACTORED
@views.route("/h/<homophoneID>", methods=['GET'])
def h(homophoneID):
    """ Homophones' pages route """

    # print(homophoneID)
    # print(homophoneID.isdigit())
    if homophoneID.isdigit():
        nthDocument = find_nth_document(homophonesCollection, int(homophoneID))
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
        homophones = create_homophones_list(
            homophonesCollection=homophonesCollection, query=homophoneID)
        if not homophones:
            return render_template("notfound.html", word=homophoneID)

        return render_template("homophones.html", homophones=homophones.homophonesList, audio=homophones.audio, ipa=homophones.ipa)


@views.route("/browse")
def browse():
    """ Browse pages (pagination) route """

    limit, offset = define_limit_offset(request)

    homophones = get_current_browse_page_homophones(homophonesGroupCollection, limit, offset)

    prevURL, nextURL, totalPages, currentPage = define_pagination_variables(limit, offset, homophonesGroupCollection=homophonesGroupCollection)

    return render_template("browse.html", limit=limit, offset=offset, prevURL=prevURL, nextURL=nextURL, totalPages=totalPages, currentPage=currentPage, homophonesLists=homophones)


@views.route("/robots.txt/")
def robots():
    """ Send robots.txt. """
    return send_from_directory("static", "robots.txt")
