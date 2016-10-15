#!/usr/bin/env python


#Import required modules
import praw, dbconfig
from urllib.parse import urlparse
import psycopg2 as pg

class WhiskyBot(praw.Reddit):
    """
    Iherits from the praw.Reddit class.
    """
    def __init__(self):
        praw.Reddit.__init__(self,'WhiskyB0t')

    def get_review_text(self,post_id=None,url=None):
        """
        Get review text from reddit given post ID or url to reddit post.
        """
        if post_id:
            # TODO: Exception handling here as well
            submission = self.get_submission(submission_id=post_id)
        elif url:
            if urlparse(url).scheme == 'http':
                url.replace('http','https')
            try:
                submission = self.get_submission(url)
            except:
                print('Failed unexpectedly...')
                return(None)

        else:
            raise(ValueError,'No input given!')

        try:
            firstComment = submission.comments[0]
        except:
            # TODO: indentify exception types. There are a million things
            # that can go wrong here.
            print('\nReceived bad data from reddit. Skipping...')
            return ''
        else:
            return firstComment.body

class WhiskyDB():
    '''
    Class to interact with WhiskyMetrics' database.
    '''
    def __init__(self):
        self.dbconn =pg.connect(database=dbconfig.database,
                user=dbconfig.user,
                password=dbconfig.password,
                host=dbconfig.host,
                port=dbconfig.port)
        self.crsr = self.dbconn.cursor()

    def get_post_links(self,name=None,distillery=None,region=None):
        '''
        Returns a generator of urls for all reviews that match one of the input
        criteria.

        Args:
            name: name of a specific whisky, e.g., Balvenie 12

            distillery: name of a distillery, e.g., Glenlivet (Leave out "The")

            region: Any of the main whisky producing regions of Scotland. E.g.,
                Islay, Highland, Campbeltown etc. Remove the s from Highlands
                and Lowlands

        Returns:
            A generator of names and urls

        Raises:
            ValueError id no inputs are given
        '''

        if name:
            query="SELECT topic, url FROM metadata WHERE topic='"+name+"';"
        elif distillery:
            query="SELECT topic, url FROM metadata WHERE topic like '"+distillery+"%';"
        elif region:
            query="SELECT topic, url FROM review WHERE region='"+region+"';"
        else:
            raise(ValueError,'Missing input!')

        return self.crsr.execute(query)



