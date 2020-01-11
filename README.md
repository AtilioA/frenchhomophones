## frenchhomophones

This is a little Flask web application I built during 2019-2020 summer vacation.
My inspiration was <a href="https://www.homophone.com/">this website</a>, which showed me interesting English homophones from time to time; I still use it as my homepage (on random).
I crawled through <a href ="https://en.wiktionary.org/w/index.php?title=Category:French_terms_with_homophones">Wiktionary's category of French homophones</a> with <a href="https://pypi.org/project/beautifulsoup4/">BeautifulSoup</a> and parsed words URLs entries with <a href="https://pypi.org/project/wiktionaryparser/">WiktionaryParser</a>. Thus, I had successfully extracted meaning from Wiktionary, I just had to create a database and a web application for it.
SQL solutions are limited to 10k rows on Heroku (Wiktionary has almost 60k homophones listed), so I went with MongoDB at mLab/Atlas, which offers 0.5GB storage for free and is easy enough to integrate with Heroku.

## Running locally
Create a `pipenv`, activate it and install the dependencies with `pipenv install`. Boot the flask app with `flask run`. Access it through `http://localhost:5000`. Flask should reload the application every time a `.py` file relevant to the project is changed.
