#!/usr/bin/env python
# coding: utf-8
"""
    WhiskyMetrics.analytics
    ~~~~~~~~~~~~~

    The main text analytics functionalities of WHiskymetrics are implemented
    here. TODO: Complete docs

    :copyright: 2016 Neelabh Kashyap, see AUTHORS for more details
    :license: MIT, see LICENSE for more details
"""
import re, nltk
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords

# Add NLTK datadir
nltk.data.path.append('/l/nltk_data')

def clean(string):
    '''
    Removes all special characters keeeping only alphanumerics and newlines.
    Also converts everything to lowercase.
    '''
    return re.sub('[^A-Za-z0-9 \n]+','',string).lower()

def tokenize(string):
    '''
    Returns a list of word tokens after removing stop words
    '''

    tokens = wordpunct_tokenize(string);
    stop_words = stopwords.words('english')
    return [word for word in tokens if word not in stop_words]


