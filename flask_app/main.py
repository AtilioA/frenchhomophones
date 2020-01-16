from flask import Blueprint, render_template, request

# from .extensions import mongo
from .utils.controllers_utils import determine_audio_URL_homophones, create_homophones_list

main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
def index():
    """ Homepage of the web application. """

    # TODO: Refactor this later
    homophonesLists = []
    audiosList = []
    for i in range(0, 4):
        homophonesLists.append(create_homophones_list(random=True))
        audiosList.append(determine_audio_URL_homophones(homophonesLists[i]))

    print(audiosList)
    print(homophonesLists)

    return render_template("index.html", homophonesLists=homophonesLists, audios=audiosList)


@main.route("/find")
def find():
    """ Route that handle query from users. """

    query = request.args['search'].strip().lower()

    homophonesList = create_homophones_list(query)
    if not homophonesList:
        return render_template("notfound.html", word=query)

    audio = determine_audio_URL_homophones(homophonesList)

    return render_template("homophones.html", homophones=homophonesList, audio=audio)


@main.route("/random/", methods=['GET'])
def random_route():
    """ Route that retrieves random document from database to be shown to the user. """

    homophonesList = create_homophones_list(random=True)
    print(homophonesList)

    audio = determine_audio_URL_homophones(homophonesList)

    return render_template("homophones.html", homophones=homophonesList, audio=audio)


@main.route("/about/", methods=['GET'])
def about():
    """ About section of the web application. """

    return render_template("about.html")
