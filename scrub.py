#!/usr/bin/env python
# coding: utf-8
"""
    ===================
    WhiskyMetrics.scrub
    ===================

    Functions for cleaning raw review data returned by :class:`scrape.WhiskyBot`

    :copyright: 2016 Neelabh Kashyap, see AUTHORS for more details
    :license: MIT, see LICENSE for more details
"""
import re, nltk
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
import numpy as np

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

def represent(segments,whisky_name):
    '''
    Returns a 5-D vector representation of a list of strings in ``segments``
    based on the algorithm described below.

    Each element of the vector is a 1 or 0 depending on presence or absence of
    the following keywords, respectively:
    ``whisky_name, color, nose, taste, finish.``
    '''

    keywords = ['name','color','nose','taste','finish']

    regex_lookup = {'name':whisky_name,
             'color':'(colo(u)?r|appearance)',
             'nose':'nose',
             'taste':'(taste|palate|mouth)',
             'finish':'finish'
             }

    vector_space = list()

    for piece in segments:
        v = np.zeros(len(keywords))
        for k in keywords:
            if re.search(regex_lookup[k],piece,re.M):
                v[keywords.index(k)] = 1


        vector_space.append(v)

    V = np.array(vector_space)

    # If name is not found, prepend a dummy string to segments which
    # refences the whisky name. This is essential for the segmentation algo
    if V.sum(0)[0] == 0:
        V = np.vstack(([1,0,0,0,0],V))
        segments.insert(0,whisky_name)

    return(segments,V)

def relevant_segment_index(V):
    '''
    Returns the indices of releveant segments by analysing the vector space
    representation returned by ``represent()``.

    Here is a brief description of the algorithm to find the relevant segments:

    TODO: Describe the algorithm
    '''
    idx = list()
    for i,v in enumerate(V.cumsum(0)):
        if np.linalg.norm(V[i]) != 0:
            idx.append(i)
            if all(v >= np.ones(V.shape[1])):
                break

    return idx
