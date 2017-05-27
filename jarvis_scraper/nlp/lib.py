# -*- coding: utf-8 -*-
from __future__ import division

import math
from collections import Counter
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup
from gensim.summarization import summarize

import jarvis_scraper.nlp.rake as rake

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
    """Caluclate Cosine distance of 2 counter objects"""
    terms = set(c1).union(c2)
    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    magA = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    try:
        res = dotprod / (magA * magB)
    except ZeroDivisionError:
        res = 0
    return res


def get_distance(url):
    """Given an URL, parse content and get
    Cosine distance from given list of keywords
    """
    text = get_text_from_url(url)
    keywords = get_keywords_vectors(text)
    k_counter = Counter(keywords)
    st_k_counter = Counter(standard_keywords)
    dis = counter_cosine_similarity(k_counter, st_k_counter)
    print("Distance from {} is ".format(url), dis)
    return dis


def get_text_from_url(url):
    """Get raw text from a given URL"""
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    soup = BeautifulSoup(html)
    return soup.get_text().strip()


def get_keywords_vectors(text):
    """Using RAKE algorithm, extract vector of keywords from text"""
    keywords = rake_object.run(text)
    return [k[0] for k in keywords]


def summarize_text(text):
    """Summarize text into 50 words"""
    return summarize(text, word_count=50)
