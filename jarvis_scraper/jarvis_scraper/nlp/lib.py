# -*- coding: utf-8 -*-
from __future__ import division

import math
from collections import Counter
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

import jarvis_scraper.nlp.rake as rake
from gensim.summarization import summarize

# French stopwords
stoppath = "jarvis_scraper/nlp/FrenchStoplist.txt"
rake_object = rake.Rake(stoppath, 5, 1, 4)
standard_keywords = ['découvrir', 'conférences', 'musée',
                     'expositions', 'agenda', 'objets', 'visitez',
                     'enfants', 'ligne', 'visites', 'recherche',
                     'missions', "Conditions d'accès", 'visite',
                     'rechercher', 'jusqu', 'billetterie',
                     'exposition']


def counter_cosine_similarity(c1, c2):
    terms = set(c1).union(c2)
    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    magA = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    try:
        res = dotprod / (magA * magB)
    except ZeroDivisionError:
        res = 0
    return res


def should_parse(url, limit=0.5):
    text = get_text_from_url(url)
    keywords = get_keywords_vectors(text)
    k_counter = Counter(keywords)
    st_k_counter = Counter(standard_keywords)
    dis = counter_cosine_similarity(k_counter, st_k_counter)
    return dis > limit


def get_text_from_url(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    soup = BeautifulSoup(html)
    return soup.get_text().strip()


def get_keywords_vectors(text):
    keywords = rake_object.run(text)
    return [k[0] for k in keywords]


def summarize_text(text):
    return summarize(text, word_count=50)
