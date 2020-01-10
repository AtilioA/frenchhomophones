import re
import random

from flask import Flask, render_template, url_for   
from flask_sqlalchemy import SQLAlchemy

from wiktionaryparser import WiktionaryParser
# Initialize parser
parser = WiktionaryParser()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

db = SQLAlchemy(app)
class Homophone(db.Model):
    word = db.Column(db.String(50), primary_key=True)
    definition = db.Column(db.String(200), nullable=False)
    
    def __repr__(self):
        return '<Word %r>' % self.definition

@app.route("/")                  
def index():
    with open("french_homophones.txt", "r+", encoding="utf8") as f:
        words = f.readlines()
        
        randomHomophone = random.choice(words).strip()
        
        parsedHomophone = parser.fetch(randomHomophone, "french")
        print(f"The random homophone is \"{randomHomophone}\"")
        
        ipaHomophones = parsedHomophone[0]["pronunciations"]['text']
        if len(ipaHomophones) > 1:  # Has IPA and homophones
            ipa = ipaHomophones[0]
            homophones = ipaHomophones[1]
        else:
            ipa = None
            homophones = ipaHomophones[0]
        homophones = homophones[11:].split(',')
        
        wordDefinitions = parsedHomophone[0]["definitions"][0]["text"][1:]
        try:
            match = re.search(r"of (\w+)$", str(wordDefinitions[0]))
            root = parser.fetch(match.group(1), "french")
        except:
            root = None
        print(root)
        print(match.group(1))
        
        try:
            audio = parsedHomophone[0]["pronunciations"]['audio'][0]
        except:
            audio = parsedHomophone[0]["pronunciations"]['audio']
        
        pronunciations = parsedHomophone[0]["pronunciations"]
        homophone = {
        'word': parsedHomophone[0]["definitions"][0]["text"][0],
        'partOfSpeech': parsedHomophone[0]["definitions"][0]["partOfSpeech"],
        'wordDefinitions': parsedHomophone[0]["definitions"][0]["text"][1:],
        'sentenceExamples': parsedHomophone[0]["definitions"][0]["examples"],
        'audio': audio,
        'homophones': homophones,
        'ipa': ipa,
        'root': root
        }
        
    return render_template("index.html", homophone=homophone)
    
# @app.route("/about/")            
# def about():
#     return render_template("about.html")    
    
@app.route("/about/")            
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
