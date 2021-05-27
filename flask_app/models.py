import os
# from gtts import gTTS
# from playsound import playsound
# from urllib.parse import quote_plus
# import requests

MONGO_URI = os.environ.get("MONGO_URI")


class HomophonesGroup:
    def __init__(self, homophonesList):
        self.homophonesList = homophonesList
        self.audio = self.determine_audio_URL()
        self.ipa = self.determine_ipa()

    def determine_ipa(self):
        """ Return first IPA string for a list of homophones.

            If no IPA is available, return `None`
        """

        if not self.homophonesList:
            return None

        # Find first IPA string from list of homophones
        for homophone in self.homophonesList:
            if homophone['pronunciations']['IPA']:
                ipa = homophone['pronunciations']['IPA']
                return ipa
        return None

    def determine_audio_URL(self):
        """ Return first audio URL from Wiktionary for a list of homophones.

            If no audio is available, request from Google Translate
            (this URL may break anytime).
        """

        if not self.homophonesList:
            return None

        # Find any audio file from list of homophones
        # # If not available, get from Google Translate (this URL may break anytime)
        audio = f"https://translate.google.com.vn/translate_tts?ie=&q={self.homophonesList[0]['word']}&tl=fr-fr&client=tw-ob"
        # audio = None

        # headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_10_1) AppleWebKit/538.36 (KHTML, like Gecko) Chrome/41.0.2171.95 Safari/538.36'}
        # response = requests.get("https://translate.google.com.vn/translate_tts?ie=&q=" + quote_plus(f"{self.homophonesList[0]['word']}&tl=fr-fr&client=tw-ob"), headers=headers)
        # print(response)
        # if response.status_code == 200:
        #     print("Successful GET request to TTS endpoint!")
        #     results = response.json()
        #     print(results)

        for homophone in self.homophonesList:
            # playsound("welcome1.mp3")
            if homophone['pronunciations']['audio']:
                # print(homophone['pronunciations']['audio'])
                audio = homophone['pronunciations']['audio']
            # else:
            #     language='fr'
            #     myobj=gTTS(text=self.homophonesList[0]['word'],lang=language)
            #     myobj.save(f"tmp/{self.homophonesList[0]['word']}.mp3")
            # continue

        # Return the first if there are more than one
        if isinstance(audio, list):
            return audio[0]
        else:
            return audio


if __name__ == "__main__":
    pass
