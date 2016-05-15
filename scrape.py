#!/usr/bin/env python3


#Import required modules
import praw,sqlite3,os,argparse,time,utils

class WhiskyBot(praw.Reddit):
    """
    Iherits from the praw.Reddit class.
    """
    def __init__(self):
        praw.Reddit.__init__(self,'WhiskyB0t')

    def get_review_text(self,postID):
        """
        Get review text from reddit given post ID.
        """
        submission = self.get_submission(submission_id=postID)
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
    def __init__(self,path_to_db):
        self.dbconn = sqlite3.connect(path_to_db)
        self.crsr = self.dbconn.cursor()

    def get_post_links(self,name=None,distillery=None,region=None):
        '''
        Yields a generator of urls for all reviews that match one of the input
        criteria.

        Args:
            name: name of a specific whisky, e.g., Balvenie 12

            distillery: name of a distillery, e.g., Glenlivet (Leave out "The")

            region: Any of the main whisky producing regions of Scotland. E.g.,
                Islay, Highland, Campbeltown etc. Remove the s from Highlands
                and Lowlands

        Returns:
            A generator of urls

        Raises:
            ValueError id no inputs are given
        '''

        if name:
            query="SELECT url FROM review WHERE name='"+name+"';"
            rec = self.crsr.execute(query)
            return (m[0] for m in rec)
        elif distillery:
            query="SELECT url FROM review WHERE name like '"+distillery+"%';"
            rec = self.crsr.execute(query)
            return (m[0] for m in rec)
        elif region:
            query="SELECT url FROM review WHERE type='"+region+"';"
            rec = self.crsr.execute(query)
            return (m[0] for m in rec)
        else:
            raise(ValueError,'Missing input!')

def main(name,choice):
    ##############################################################################
    # Main:
    ##############################################################################
    # Open database connection
    dbConn = sqlite3.connect('singlemalt.db')

    # prepare a cursor object using cursor() method
    c = dbConn.cursor()

    # Fetch post IDs from the database
    if choice == 1:
        analyseBy = 'distillery'
        rec = c.execute('SELECT postID FROM review WHERE name LIKE ?',[name.lower()+'%']).fetchall();
        nRec = c.execute('select count(postID) from review where name like ?',[name.lower()+'%']).fetchone()[0]
    elif choice == 2:
        analyseBy = 'region'
        rec = c.execute('select postID from review where region = ?',[name.lower()]).fetchall();
        nRec = c.execute('select count(postID) from review where region = ?',[name.lower()]).fetchone()[0]
    elif choice ==3:
        analyseBy = 'whisky'
        rec = c.execute('select postID from review where name = ?',[name.lower()]).fetchall();
        nRec = c.execute('select count(postID) from review where name = ?',[name.lower()]).fetchone()[0];

    if nRec == 0: # Prints error message and quits if no records are found
        print('No records pertaining to your selection '+ name +' were found in the database.')
        exit()

    # Begin processing the records

    # Make folder to store review data.
    dirName = analyseBy+'_'+("_".join(name.split(' ')))
    os.mkdir(dirName)

    # Create metadata file
    f = open(os.path.join(dirName,'metadata'),'a+')
    f.write('Web Scrape results for whisky reviews by '+analyseBy+'\n')
    f.write('Subject: '+name+'\n')

    f.write('Date: '+time.strftime('%d/%m/%Y\n'))
    f.write('Time: '+time.strftime('%H:%M:%S\n'))
    f.close()

    # Collect reviews

    # Instantiate WhiskyBot
    w = WhiskyBot()
    storagePath = os.path.join(os.getcwd(),dirName)
    count = 1
    for row in rec:
        postID = ''.join(row) # Convert to str
        if postID:
            msg = "\r{0:.2f}% complete".format(((count*1.0)/nRec)*100)
            utils.printStatus(msg)

            # Write review text to file
            with open(os.path.join(storagePath,(postID+'.txt')),'w+') as f:
                # re-encode unicode comment as ascii. Bad things happen if this is not done.
                reviewComment = w.getReviewtext(postID).encode('ascii','ignore')
                f.write(reviewComment)
        else:
            print( "\nField empty. Skipping...")

        count+=1

    print ("\nDone!\n")
    # Close database connection
    dbConn.close()

if __name__ == '__main__':
    # Command line interface
    cliParser = argparse.ArgumentParser(description=
    """
    Queries the database for post IDs associated with the information specified in the
    input, gets the reddit comment with said post IDs. The scrape command stores
    the comment text in.txt files whose  names are the same as the post IDs. 
    A METADATA file is also created, and information in this file may be used by tools yet to be written.

    """
    )
    cliParser.add_argument('search_string',help = 'Whisky, region or ditillery you want to get reviews of.')
    cliParser.add_argument('--type',default = 3,type = int,choices = [1,2,3],help =
    """
    1, 2 or 3 depending on whether your search string specifies a distillery name, a whisky producing
    region or the name of a particular whisky. Is set to 3 by default.
    """,dest='choice')
    choice =  cliParser.parse_args().choice
    name = cliParser.parse_args().search_string

    main(name,choice)

