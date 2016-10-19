#!/usr/bin/env python

'''

A script to collect reviews and put them in a directory called ``review-corpora``.

This scripts illustrates the features of Whiskymetrics so far.

'''

import scrape,scrub,dbconfig,time,psycopg2

w = scrape.WhiskyBot()
db = scrape.WhiskyDB()

db.crsr.execute("SELECT review_id FROM metadata EXCEPT SELECT review_id FROM review ORDER BY review_id;")
review_ids = [m[0] for m in db.crsr]
for i in review_ids:
    print(i)
    time.sleep(1)

    foo = [m for m in db.get_post_links(review_id=i)]

    for m in foo:
        print(m)
        try:
            text = w.get_review_text(url=m[2])
        except:
            print('Something went wrong. Skipping...')
            continue


        cleaned_text = scrub.clean(text)

        #Split into paragraphs
        paragraphs = [' '.join(scrub.tokenize(m)) for m in cleaned_text.split('\n\n')]


        (segments,V) = scrub.represent(paragraphs,m[1])

        relevant_idx = scrub.relevant_segment_index(V)
        print(relevant_idx)

        if relevant_idx:
            filtered_segments = [segments[m] for m in relevant_idx]
            review_text = ' '.join(filtered_segments)
            try:
                db.put_review_text(i,review_text)
            except psycopg2.IntegrityError:
                db.dbconn.rollback()
                print('Already exists. Skipping...')
                pass

        else:
            print('No keywords found. Skipping...')



del(db)
