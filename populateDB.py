#!/usr/bin/env python
"""
This script consumes a csv file containing metadata about /r/scotch whisky reviews
and populates a SQLite database which can be queried by WhiskyMetrics scripts

"""
import sqlite3,re,sys

# ---------------------------------------------------------------------------- #
#                           Function Definitions                               #
# ---------------------------------------------------------------------------- #

def rowParse(row):
    """
    Parses a row in a whisky_review csv file and returns a list containing
    data that is pushed into the database
    """
    def getPostID(url):
        """
        Strips away the leading and trailing parts of the url and returns
        the postID
        """
        reBeforePostID = re.compile('(http:\/\/)?.*\.com\/r\/.*\/comments\/')
        reSelectPostID = re.compile('[a-z0-9]*')

        temp = reBeforePostID.sub('',url)
        postID = reSelectPostID.match(temp).group(0)
        return postID

    result = list()

    # Extract region
    region = row[5].strip().lower()
    # We are only interested in single malt Scotch
    if region in set(['lowland','speyside','highland','island','islay','campbeltown']):
        # Extract name
        name = row[1].strip().lower()
        # remove quotes and apostrophe
        name = name.replace('"','')
        name = name.replace("'",'')
        result.append(name)

        # Add region
        result.append(region)

        # Extract post ID
        postID = getPostID(row[3])
        result.append(postID)

        # Extract score
        try:
            result.append(int(row[4].strip()))
        except ValueError:
            result.append(None)

    return result

def printStatus(msg):
    sys.stdout.write("\r"+msg)
    sys.stdout.flush()
    

def main():

    # Connect to database and create table
    dbConn = sqlite3.connect("singlemalt.db")
    dbConn.text_factory = str
    c = dbConn.cursor()

    c.execute("drop table if exists review")

    # Create table called reviews
    sqlQuery = """create table if not exists review(
                        name text, --whisky name
                        region text, --region in Scotland where it was produced
                        postID text, --reddit post ID
                        score integer --review score
                        )
                        """

    c.execute(sqlQuery)

    # Count the number of rows in the csv file for progress indicator
    fileName = "whisky_reviews.csv"
    with open(fileName,'rb') as f:
        rowCount = sum(1 for line in f)

    with open(fileName,'rb') as f:
        count = 1
        for line in f:
            row = line.split(',')
            # Enter row into database
            dbEntry = rowParse(row)
            if dbEntry:
                if dbEntry[-1]:
                    sqlQuery = """insert into review (name,region,postID,score)
                                              values (?,?,?,?)""";
                    c.execute(sqlQuery,dbEntry)
                else:
                    sqlQuery = """insert into review (name,region,postID,score)
                                              values (?,?,?,NULL)""";
                    c.execute(sqlQuery,dbEntry[0:3])
                dbConn.commit()
            # Indicate progess
            msg = "Processing. {0:.3f}% complete.".format(((count*1.0)/rowCount)*100)
            printStatus(msg)
            count+=1

    numRecords = c.execute("select count(*) from review").next()
    print ' '+str(numRecords[0])+" entires have been added to table 'review' in 'singlemalt.db'."

    dbConn.close()

if __name__ == '__main__':
    main()















