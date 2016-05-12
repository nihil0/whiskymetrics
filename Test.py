#!/usr/bin/env python
"""
Dumps term frequecies of words used to describe the features of whiskies specified
in the input.txt file as json files in a directory called 'Results'
"""
import os,scrape,scrub,fextract

with open('input.txt','rb') as f:
    contents = [m.strip() for m in list(f)]

# Select only whisky names
wList = [m for m in contents if not(m.startswith('#') or m == '')]


for item in wList:
    dirName = 'whisky_'+("_".join(item.split(' ')))
    if not os.path.isdir(dirName):
        print "Collecting reviews for "+item
        scrape.main(item,3)
        scrub.main(dirName)
        fextract.main(dirName)
    else:
        print "Data acquisition already completed. Moving on..."



