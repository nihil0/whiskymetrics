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
import csv
from datetime import datetime

# Add NLTK datadir
nltk.data.path.append('/l/nltk_data')

def clean(string):
    '''
    Removes all special characters keeeping only alphanumerics and newlines.
    Also converts everything to lowercase.

    Args Type:
        string

    Returns Type:
        string

    '''
    return re.sub('[^A-Za-z0-9 \n]+','',string).lower()

def tokenize(string):
    '''
    Returns a list of word tokens after removing stop words

    Args Type:
        string

    Returns Type:
        list
    '''

    tokens = wordpunct_tokenize(string);
    stop_words = stopwords.words('english')
    return [word for word in tokens if word not in stop_words]

def represent(segments,whisky_name):
    '''
    Maps each element of the list of strings in ``segments`` to a 5-D vector in {0,1}
    such that each element of the vector is a 1 or 0 depending on presence or absence 
    of the following keywords, respectively:
    ``whisky_name, color, nose, taste, finish.``

    Args Type:
        segments: list of strings where each string represents e.g., a paragraph
        whisky_name: string

    Returns Type:
        tuple (segments: list of strings,
        V: list of numpy vectors)

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
    # refence the whisky name. This is essential to identify relevant segments.
    if V.sum(0)[0] == 0:
        V = np.vstack(([1,0,0,0,0],V))
        segments.insert(0,whisky_name)

    return(segments,V)

def relevant_segment_index(V):
    '''
    Returns the indices of releveant segments by analysing the vector space
    representation returned by ``represent()``.

    Sometimes users submit reviews of multiple whiskies in the same comment.
    It is essential to identify which review block is most relevant to the whisky
    being analysed. The algorithm proceeds as follows:

    Each column of V is represents the presence/absence of certain keywords in 
    a segment represented by a row. We first locate the segment which references
    the name of the whisky. Next, we check if the next keyword is also referenced
    in the same segment. If yes, we move onto the next keyword, if no, we proceed
    to look in the next segment. In the end we end up with the minimum  set of all
    segments which reference the keywords starting from the first one.

    Args:
        V: numpy array of vectors

    Returns:
        idx : List

    '''
    def idx_search(V,idx):
        '''Recursion to get the most relevant segments'''
        if V.size == 0:
            return idx
        else:
            try:
                non_zero_row_idx = np.where(V[:,0])[0][0]
            except IndexError:
                non_zero_row_idx = 0

            if not idx:
                idx.append(non_zero_row_idx)
            else:
                idx.append(idx[-1]+non_zero_row_idx)

            return idx_search(np.delete(V[non_zero_row_idx:,:],0,1),idx)

    if not any(V[:,1:].sum(0)):
    # Return None if all keywords are not present in text
        return None
    else:
        return list(np.unique(idx_search(V,[])))


def transform_csv(input_filename):
    '''
    Returns a CSV file which can be directly loaded into the whiskymetrics database.
    Refer to metadata table in WhiskyDBSchema.sql for the format spec.
    '''
    with open(input_filename) as f:
        with open('out.csv','w+') as f_out:
            fieldnames = ['url','timestamp','author','topic','region','score']
            wr = csv.DictWriter(f_out,fieldnames=fieldnames)
            wr.writeheader()
            r = csv.reader(f)

            for row in r:
                try:
                    timestamp = datetime.strftime(
                        datetime.strptime(row[0],"%m/%d/%Y %H:%M:%S"),
                        "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    continue

                wr.writerow({
                    'url': row[3].strip(),
                    'timestamp' : timestamp,
                    'author' : row[2].lower().strip(),
                    'topic' : row[1].lower().strip(),
                    'region' : row[5].lower().strip(),
                    'score' : (''.join(row[4].split())).strip()
                    })
