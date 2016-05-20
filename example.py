#!/usr/bin/env python

'''

A script to collect reviews and put them in a directory called ``review-corpora``.

This scripts illustrates the features of Whiskymetrics so far.

'''

import scrape,scrub,os,re

w = scrape.WhiskyBot()
db = scrape.WhiskyDB('whisky.db')

subject = 'Laphroaig Quarter Cask'

links = db.get_post_links(name=subject)
count=0
if os.path.exists(os.path.expanduser('~/review-corpora')):
    with open(os.path.join(os.path.expanduser('~/review-corpora'),
        re.sub('\s','',subject)+'.txt'),'a+') as f:
        for name,link in links:
            count+=1
            print(count)
            try:
                text = w.get_review_text(url=link)
            except:
                print('Something went wrong. Skipping...')
                continue


            cleaned = scrub.clean(text)

            paragraphs = [' '.join(scrub.tokenize(m)) for m in cleaned.split('\n\n')]

            (segments,V) = scrub.represent(paragraphs,name)

            filtered_segments = [segments[m] for m in scrub.relevant_segment_index(V)]

            f.write(' '.join(filtered_segments))


