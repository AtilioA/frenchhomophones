import os
import sys

from .models import HomophonesGroup

# Needed to execute this package as a script
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))


def find_one_random_document(userCollection):
    cursor = userCollection.aggregate([
        { "$sample": { "size": 1 } }
    ])

    return list(cursor)[0]


def find_nth_document(userCollection, n):
    """ Return nth document from database (insertion order). """

    return userCollection.find_one(skip=n)


def create_homophones_list(userCollection, query="", random=False):
    """ Return Homophone object with queried word (if applicable) and its homophones.

        Until infinitive forms are stored in the database,
        will look up with WiktionaryParser during execution.

        Optional keyword arguments:

        `random`: will use a random homophone as starting point
        if set to `True`.
    """

    homophonesList = []

    if random:
        homophone = find_one_random_document(userCollection)
        # print(homophone)
    else:
        homophone = userCollection.find_one({"word": query.strip()})
        if homophone is None:
            return None

    # Create list querying all homophones
    homophonesList.append(homophone)
    print(homophone)
    for otherHomophone in homophone['pronunciations']['homophones']:
        try:
            # print(f"Querying {otherHomophone.strip()}...")
            wordQueryResult = userCollection.find_one(
                {"word": otherHomophone})
            # print(f"query: {wordQueryResult}")
        except TypeError:  # If the query return None
            wordQueryResult = None

        # If didn't find in the database, proceed to next iteration
        if not wordQueryResult:
            continue

        homophonesList.append(wordQueryResult)

    homophones = HomophonesGroup(homophonesList)

    return homophones
