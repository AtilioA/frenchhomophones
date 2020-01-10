import sqlite3
import re
import random
from wiktionaryparser import WiktionaryParser

DB_FILE_NAME = "homophones.db"
conn = sqlite3.connect(f"{DB_FILE_NAME}.sqlite", isolation_level=None)
cursor = conn.cursor()

# Initialize parser
parser = WiktionaryParser()

def create_table():
    cursor.execute("""
        CREATE TABLE homophones (
        word VARCHAR(50) NOT NULL,
        definition VARCHAR(200) NOT NULL,
        partOfSpeech VARCHAR(20) NOT NULL,
        audio VARCHAR(250),
        ipa VARCHAR(50)
    );
    """)
    cursor.execute("CREATE UNIQUE INDEX ocurrence ON homophones (word);")


def clear_table():
    cursor.execute("""
        DELETE FROM homophones;
    """)
    cursor.execute("VACUUM")


def populate_db():
    with open("french_homophones.txt", "r+", encoding="utf8") as f:
        words = f.readlines()
        
        for homophone in words[20:30]:
            homophone = homophone.strip()
            print(f"Processing word \"{homophone}\"...")
            
            parsedHomophone = parser.fetch(homophone, "french")
            word = parsedHomophone[0]["definitions"][0]["text"][0]

            partOfSpeech = parsedHomophone[0]["definitions"][0]["partOfSpeech"]
            wordDefinitions = parsedHomophone[0]["definitions"][0]["text"][1:]
            sentenceExamples = parsedHomophone[0]["definitions"][0]["examples"]
            
            ipaHomophones = parsedHomophone[0]["pronunciations"]['text']
            if len(ipaHomophones) > 1:  # Has IPA and homophones
                ipa = ipaHomophones[0]
                print(ipa)
                homophones = ipaHomophones[1]
            else:
                ipa = None
                homophones = ipaHomophones[0]
            homophones = homophones[12:].split(',')
            
            pronunciations = parsedHomophone[0]["pronunciations"]
            audio = parsedHomophone[0]["pronunciations"]['audio']
            
            print(f"\nWord: {word}")
            print(f"Part of speech: {partOfSpeech}")
            
            print(f"Definitions:")
            for i, definition in enumerate(wordDefinitions):
                print(f"{i + 1}. {definition}")
                
            if sentenceExamples:
                print(f"Examples:")
                for sentence in sentenceExamples:
                    print(f"\t{sentence}")
                    
            # Find word's root
            # match = re.search(r"of (\w+)$", str(wordDefinitions[0]))
            # if match:
            #     print(f"\nRetrieving root ({match.group(1)}) definition:")
            #     # print_word_definition(0, match.group(1))
            #     print()
            
            print(f"Homophones: {homophones[2:]}")
            try:
                ipa = re.sub(r".*IPA:\s*", "", ipa)
                print(ipa)
            except:
                ipa = None
            
            if audio:
                audio = f"https://{audio[0][2:]}"
                print(f"Audio URL: {audio}")
            else:
                audio = None
                # print("Audio is unavailable.")
                
            try:
                cursor.execute(f"""
                    INSERT INTO homophones (word, partOfSpeech, definition, audio, ipa) VALUES ('{word}', '{partOfSpeech}', '{wordDefinitions[0]}', '{audio}', '{ipa}')
                """)
                print("Palavra inserida!")
            except sqlite3.IntegrityError:
                print("Erro. Palavra não inserida (provavelmente duplicada).")
                pass

        conn.commit()
        print("Tabela atualizada com sucesso.")

        print("Desconectando...")
        conn.close()


if __name__ == "__main__":
    clear_table()
    # create_table()
    populate_db()
