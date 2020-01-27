import os
import sys

# Needed to execute this package as a script
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))


def find_one_random_document(user_collection):
    cursor = user_collection.aggregate([
        { "$sample": { "size": 1 } }
    ])

    return list(cursor)[0]


def find_nth_document(user_collection, n):
    """ Return nth document from database (insertion order). """

    return list(user_collection.find().limit(n))[-1]


def create_homophones_list(user_collection, query="", random=False):
    """ Return Homophone object with queried word (if applicable) and its homophones.

        Until infinitive forms are stored in the database,
        will look up with WiktionaryParser during execution.

        Optional keyword arguments:

        `random`: will use a random homophone as starting point
        if set to `True`.
    """

    homophonesList = []

    if random:
        homophone = find_one_random_document(user_collection)
        # print(homophone)
    else:
        homophone = user_collection.find_one({"word": query.strip()})
        if homophone is None:
            return None

    # Create list querying all homophones
    homophonesList.append(homophone)
    print(homophone)
    for otherHomophone in homophone["pronunciations"]["homophones"]:
        try:
            # print(f"Querying {otherHomophone.strip()}...")
            wordQueryResult = user_collection.find_one(
                {"word": otherHomophone})
            # print(f"query: {wordQueryResult}")
        except TypeError:  # If the query return None
            wordQueryResult = None

        # If didn't find in the database, proceed to next iteration
        if not wordQueryResult:
            continue

        homophonesList.append(wordQueryResult)

    homophones = Homophones(homophonesList)

    return homophones


class Homophones:
    def __init__(self, homophonesList):
        self.homophonesList = homophonesList

        audio = self.determine_audio_URL()
        # print(audio)
        if isinstance(audio, list):
            self.audio = audio[0]
        else:
            self.audio = audio

        self.ipa = self.determine_ipa()

    def determine_ipa(self):
        """ Return IPA for list of homophones.

            Return first IPA string from Wiktionary from the list of homophones.

            If no IPA is available, return `None`
        """

        # Find any IPA string from list of homophones
        for homophone in self.homophonesList:
            if homophone["pronunciations"]["IPA"]:
                ipa = homophone["pronunciations"]["IPA"]
                # print(ipa)
                return ipa
        return None

    def determine_audio_URL(self):
        """ Return audio URL for list of homophones.

            Return first audio file from Wiktionary from the list of homophones.

            If no audio is available, request from google translate
            (Request URL may break anytime).
        """

        # Find any audio file from list of homophones
        # If not available, get from Google Translate (this URL may break anytime)
        audio = f"https://translate.google.com.vn/translate_tts?ie=&q={self.homophonesList[0]['word']}&tl=fr-fr&client=tw-ob"
        for homophone in self.homophonesList:
            if homophone["pronunciations"]["audio"]:
                audio = homophone["pronunciations"]["audio"]
        return audio
