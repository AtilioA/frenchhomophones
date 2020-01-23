import mongoengine as me
import os

from wiktionaryparser import WiktionaryParser
parser = WiktionaryParser()
MONGO_URI = os.environ.get("MONGO_URI")


class Pronunciations(me.EmbeddedDocument):
    text = me.ListField()
    audio = me.ListField()


class RelatedWords(me.EmbeddedDocument):
    relationshipType = me.StringField()
    words = me.ListField()


class Definitions(me.EmbeddedDocument):
    partOfSpeech = me.StringField(required=True)
    text = me.ListField()
    relatedWords = me.EmbeddedDocumentListField(RelatedWords)
    examples = me.ListField()


class Word(me.Document):
    etymology = me.StringField()
    definitions = me.EmbeddedDocumentListField(Definitions, required=True)
    pronunciations = me.EmbeddedDocumentField(Pronunciations, required=True)


if __name__ == "__main__":
    me.connect("frenchhomophones", host=MONGO_URI)
    print("Connected to database.")
    
    parsedHomophone = parser.fetch("fer", "french")[0]
    parsedHomophone2 = parser.fetch("faire", "french")[0]
    test = Word(
        etymology=parsedHomophone["etymology"],
        definitions=parsedHomophone["definitions"],
        pronunciations=parsedHomophone["pronunciations"]
    )
    test.save()

    print(Word.objects.first()["etymology"])
