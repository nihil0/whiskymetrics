#! /usr/bin/env python
"""
fextract:

This tool iterates through the files in the folder created by scrape.py and extracts
term frequencies (TF) of words associated with four whisky characteristics, namely,
colour, nose, taste and finish. The data are stored in JSON in a directory called
JsonDumps. The JSON files have the same name as the folder specified in the command
line argument. 
"""
import argparse,os,json,sqlite3,tokenizer,utils

def main(dataDir):
    # Setup variables for path and folder
    pwd = os.getcwd()
    filesPath = os.path.join(pwd,dataDir)

    # Folder for holding json files
    try:
        os.mkdir('JsonDumps')
    except:
        pass

    jsonPath = os.path.join(pwd,'JsonDumps')
    # Setup database connection
    dbconn = sqlite3.connect('singlemalt.db')
    c = dbconn.cursor()

    # Get list of text files in folder
    filesList = [m for m in os.listdir(filesPath) if m.endswith('.txt')]

    # Create python dict with feature names as keys and a dict of word counts
    # of words describing each feature
    features = ['color','nose','taste','finish']
    featureDict = {k:dict() for k in features}
    s = tokenizer.StopWords()

    # Iterate through each file in folder
    for txtFile in filesList:
        msg = 'Extracting features. {0:.2f}% complete'.format(((filesList.index(txtFile)+1.0)/len(filesList))*100)
        utils.printStatus(msg)
        with open(os.path.join(filesPath,txtFile)) as f:
            # read file contents as string using read()
           reviewText = f.read()

        # lookup name of whisky file refers to from database
        wName = c.execute('select name from review where postID = ?',
                                                [txtFile.split('.')[0]])

        # Instantiate an Indexer object for wName
        idx = tokenizer.Indexer(reviewText,wName.fetchone()[0])

        # Do this only if all dict values are non-empty
        if any(idx.idxDict.values()):

            # Filter feature descriptors through stop-word filter
            for m in features:
                words = s.swFilter(idx.getFeature(m,reviewText))
                tokenizer.updateFeatureDict(featureDict,words,m)

    # Normalize word counts by the number of text files to get TF
    numFiles = len(filesList)
    tokenizer.normalizeWordCounts(featureDict,numFiles)

    # Add information about the analysis type and name of whisky to JSON file
    aType,wName = [dataDir.split('_')[0], " ".join(dataDir.split('_')[1:])]
    jsonDict = {'type':aType,'name':wName}

    # Add feature dict to JSON file
    jsonDict['features'] = featureDict

    # Dump file in directory
    with open(os.path.join(jsonPath,dataDir+'.json'),'w+') as f:
        json.dump(jsonDict,f)

    print "\n Done!"

if __name__ == '__main__':

    # Command line interface
    cliParser = argparse.ArgumentParser(description =
    """
    This tool iterates through the files in the folder created by scrape.py and extracts
    term frequencies (TF) of words associated with four whisky characteristics, namely,
    colour, nose, taste and finish. The data are stored in JSON in a directory called
    JsonDumps. The JSON files have the same name as the folder specified in the command
    line argument.

    """)

    cliParser.add_argument('dir_name',help='Name of the folder containing \
    the review files.')

    userArg = cliParser.parse_args()

    dataDir = userArg.dir_name

    main(dataDir)



