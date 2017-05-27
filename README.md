# Focused crawler

This is a simple version of a focused crawler. Instead of massively crawling all pages' URL, for a given domain, it will first parse all sub-pages, then for each sub-page, it calculates cosine distance between the page's content and the content of a given page model.

It then returns a list of sub-pages (URLs) of all given domains whose contents best match with the given page model

This technique is called **focused crawling**, which is common in massive data collection. It is used to avoid crawling non-related pages

# How does it work ?

In this simple version, the procedure is:
1. Declare all interested domains in `jarvis_scraper/sipders/jarvis_scraper`. Give all concerned domain as a list:
```
start_urls = ['http://www.musee-armee.fr']
```

2. The spider will parse all sub-pages for each domain declared in `start_urls`
3. The crawler extract raw content of each sub-pages
4. The crawler use RAKE algorithm to extract list of keywords for each page
5. It then calculate cosine distance between this page and the declared keywords. The keywords are simple stored as a list in `jarvis_scraper/nlp/lib` as:
```
standard_keywords = ['découvrir', 'conférences', 'musée',
                     'expositions', 'agenda', 'objets', 'visitez',
                     'enfants', 'ligne', 'visites', 'recherche',
                     'missions', "Conditions d'accès", 'visite',
                     'rechercher', 'jusqu', 'billetterie',
                     'exposition']
```
6. For each domain, the crawler returns 5 url who has highest cosine score

# How to try ?

1. Install `requirements.txt` with Python 3 (3.4 is the tested environment)
2. Navigate to project root dire and launch the following command
```
scrapy crawl jarvis_scraper -o result.csv
```

The 5 url whose contents most related to the given model will be outputed in the `result.csv` file

You can try to twist the page models (declared above) and change the interested domains to see results

Note that this version works best with French language page.

# Libraries used

The implementation of RAKE algorithm and the list of French stopwords are taken from [here](https://github.com/zelandiya/RAKE-tutorial)

Thanks the author for her implementation and the given French stopwords
# License
The source code is released under the MIT License
