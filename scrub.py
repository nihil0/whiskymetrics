#!/usr/bin/env python
"""
Processes the review files creates by the scrape command of the Wiskymetrics
toolkit. All text is converted to lowercase and special characters are removed.
This is the final stage before the text-mining algorithms begin their work.

The script takes as its input a DATA_* folder, processes all text files in it
and adds a SCRUBBED flag to the METADATA file.

"""

import argparse, os, glob, re, utils

def main(dirName):
    # Create a list of all files in the directory
    fileList =  glob.glob(os.path.join(dirName,'*.txt'))

    # Iterate through the list
    for line in fileList:
        msg = 'Cleaning raw data. {0:.2f}% complete.'.format(((fileList.index(line)+1.0)/len(fileList))*100)
        utils.printStatus(msg)
        with open(line,'r') as f:
            reviewText = f.readlines()

        with open(line,'w') as f:
            for row in reviewText:
                # Convert to lower case and remove special characters
                newRow = re.sub('[^A-Za-z0-9 \n]+','',row).lower()
                f.write(newRow)


    # Add SCRUBBED flag to the METADATA file
    fileName = os.path.join(dirName,'metadata')

    with open(fileName,'a') as f:
        f.write('SCRUBBED = 1')
    print "\nDone!"

if __name__ == '__main__':

    # Command-line Interface
    cliParser = argparse.ArgumentParser(description =
    """
    Processes the review files creates by the scrapereviews command of the Wiskymetrics
    toolkit. All text is converted to lowercase and special characters are removed.
    This is the final stage before the text-mining algorithms begin their work.

    The script takes as its input a folder name, processes all text files in it
    and adds a SCRUBBED flag to the METADATA file.

    """)

    cliParser.add_argument('dir_name',help='Name of the folder containing \
    the review files to be scrubbed.')

    userArg = cliParser.parse_args()

    dirName = userArg.dir_name

    main(dirName)








