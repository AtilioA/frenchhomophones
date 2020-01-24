from flask import Blueprint, render_template, send_from_directory, request, redirect

from .controllers import determine_audio_URL_homophones, create_homophones_list, find_nth_document, find_one_random_document

views = Blueprint('views', __name__)


@views.route('/<path:urlpath>/', methods=['GET', 'POST'])  # Catch all undefined routes
@views.route('/', methods=['GET'])
def index(urlpath='/'):
    """ Homepage of the web application. """

    # TODO: Refactor this later
    homophonesLists = []
    audiosList = []
    for i in range(0, 5):
        homophonesLists.append(create_homophones_list(random=True))
        audiosList.append(determine_audio_URL_homophones(homophonesLists[i]))

    print(audiosList)
    print(homophonesLists)

    return render_template("index.html", homophonesLists=homophonesLists, audios=audiosList)


@views.route("/find")
def find(query=""):
    """ Handle query from users. """

    query = request.args['search'].strip().lower()
    return redirect(f"/h/{query}")


@views.route("/random/", methods=['GET'])
def random_route():
    """ Retrieve random document from database to be shown to the user. """

    randomHomophone = find_one_random_document()[0]
    print(randomHomophone)   
    query = randomHomophone["word"].lower()
    print(randomHomophone["pronunciations"]["homophones"])
    for string in randomHomophone["pronunciations"]["homophones"]:
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
    print(homophoneID.isdigit())
    if homophoneID.isdigit():
        nthDocument = find_nth_document(int(homophoneID))
        print(nthDocument["word"])
        if nthDocument:
            wordRoute = nthDocument["word"]
            print(nthDocument["pronunciations"]["homophones"])
            for string in nthDocument["pronunciations"]["homophones"]:
                wordRoute = f'{wordRoute}-{string}'

            return redirect(f'/h/{wordRoute.strip()}')
        else:
            return render_template("notfound.html", word=homophoneID)
    else:
        homophoneID = homophoneID.split("-")[0]
        print(homophoneID)
        homophones = create_homophones_list(homophoneID)
        if not homophones:
            return render_template("notfound.html", word=homophoneID)

        return render_template("homophones.html", homophones=homophones.homophonesList, audio=homophones.audio, ipa=homophones.ipa)


@views.route("/robots.txt/")
def robots():
    """ Send robots.txt. """
    return send_from_directory("static", "robots.txt")
