# tokenize.py

"""
This module defines functions used in tokenizing whisky review text
"""
import os
import re

class StopWords:
    """ List of English stop words """
    def __init__(self):
        pwd = os.getcwd();

        with open(os.path.join(pwd,'stopwords_en.txt')) as f:
            self.stopWords = set(f.read().replace("'","").splitlines());
    def swFilter(self,txt):
        myTxt = set(txt.split());
        return myTxt.difference(self.stopWords);

class Indexer:
    """
    Gives you what you need
    """
    def __init__(self,reviewText,wName):
        def getIdxDict(reviewText,wName):
            """
            Returns a dict where keys \in {name,color,nose,taste,finish} and values are
            a list of ending indicies of the words pertaining to key after searching
            the entire string in reviewText.
            """
            def getIdx(reviewText,regEx):
                return [m.span()[1] for m in regEx.finditer(reviewText)];

            idxDict = dict();
            idxDict['name'] = getIdx(reviewText,re.compile(wName,re.M));
            idxDict['color'] = getIdx(reviewText,re.compile('^\s*(colo(u)?r|appearance)',re.M));
            idxDict['nose'] = getIdx(reviewText,re.compile('^\s*nose',re.M));
            idxDict['taste'] = getIdx(reviewText,re.compile('^\s*(taste|palate|mouth)',re.M));
            idxDict['finish'] = getIdx(reviewText,re.compile('^\s*finish',re.M));

            return idxDict;

        self.idxDict = getIdxDict(reviewText,wName);
        self.instCount = [len(val) for val in self.idxDict.itervalues()];
        self.fNames = {self.idxDict.keys()[m]:m for m in range(len(self.idxDict.keys()))};

    def getFeature(self,fNameStr,reviewText):
        """
        Returns a string which most likely represents descriptors for feature
        specified in fNameStr. fNameStr \in \{color,nose,taste,finish \}
        """
        if fNameStr not in self.idxDict.keys() or fNameStr == 'name':
            raise Exception("Invalid feature name");
        else:
            numInst = self.instCount[self.fNames[fNameStr]];
            if numInst == 0:
                return '';
            elif numInst == 1:
                return re.match('.*',reviewText[self.idxDict[fNameStr][0]:]).group(0);
            else:
                stPos = self.getStartPos(fNameStr);
                if stPos is None:
                    return '';
                else:
                    return re.match('.*',reviewText[stPos:]).group(0);

    def getStartPos(self,fNameStr):
        """
        Returns the most likely position from which to select the descriptor
        """
        threshold = 1000;
        feedPosDict = dict();
        wOccList = self.idxDict['name'];
        # If whisky is not mentioned in the review assume it is mentioned at position 0
        if not wOccList:
            wOccList.append(0);

        fOccList = self.idxDict[fNameStr];

        for wLoc in wOccList:
            for fLoc in fOccList:
                if (fLoc-wLoc) > 0 and (fLoc-wLoc) < threshold:
                    feedPosDict[(fLoc-wLoc)] = fLoc;
        if feedPosDict:
            return feedPosDict[min(feedPosDict)];
        else:
            return None

def updateFeatureDict(featureDict,fSet,fName):

    if fName not in featureDict.keys():
            raise Exception("Invalid feature name");
    else:
        for word in fSet:
                if featureDict[fName].has_key(word):
                    featureDict[fName][word] += 1;
                else:
                    featureDict[fName][word] = 1;

def normalizeWordCounts(featureDict,N):
    for k in featureDict.keys():
        for l in featureDict[k].keys():
            featureDict[k][l] /= (float(N));
            featureDict[k][l] = round(featureDict[k][l],6)









