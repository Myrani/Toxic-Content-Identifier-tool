import random
from Program.Utils.PathHandler import PathHandler
from Program.Parameters.paths import paths
from Program.RedditExplorer.AccountExplorer import AccountExplorer
import json
import os 
import nltk

class ToxicityAnalyser():

    def __init__(self,classifierName,reddit) -> None:
        
        """
            Bridge class over the NLP side and Reddit API .
            Once a classifier is loaded, this class serves as a comment analyser
            of a given profile .
        
        """


        # Basic info setup 
        self.pathHandler = PathHandler()
        self.accountExplorer = AccountExplorer(reddit=reddit)
        self.classifierName = classifierName
        
        # PlaceHolder 
        self.classifier = None
        self.priors = {}
        self.uniqueWordsSet = {}
        self.lexiconSize = 0

        self._setUpClassifier()

    def _loadClassifier(self):
        """
            Loads a classifier with the given name
            
        """
        
        data = open(self.pathHandler.getClassifiersPath()+self.classifierName)
        return json.load(data)
    
    def _judgeUseretrics(self,username):
        """
            Harvest all public specific user data 
        
        """
        ### self.accountExplorer.harvestUserMetrics(username)
        self.accountExplorer.explorerDataHandler._dumpBaggedProfileToJSON(self._convertRawUserMetricsToBagOfWords(username))



    def _setUpClassifier(self):

        """
            Loads all the specs of a classifier : name, priors, uniquewords, lexiconsize, Classifier 
        
        """

        loadedFile = self._loadClassifier()
        self.classifier = loadedFile["classifier"]
        self.priors = loadedFile["priors"]
        self.uniqueWordsSet = set(loadedFile["uniqueWords"])
        self.lexiconSize = loadedFile["lexiconSize"]


    def _tokenizeComment(self,comment):

        """
            Transforms into a list of token a given string
        
        """
        return nltk.word_tokenize(comment)



    def _convertRawUserMetricsToBagOfWords(self,username):
        """
            Convert an harvester user profile content to a bag of word structure
        
        """

        bag = {"username": username,"bag":{}}

        usermetrics = self.accountExplorer.getRawUserMetrics(username)

        for key,value in usermetrics["comments"].items():
            for comment in value:
                for word in self._tokenizeComment(comment["content"]):

                    if word in bag["bag"]:
                        bag["bag"][word] = bag["bag"][word] + 1
                    else:
                        bag["bag"][word] = 1        
        return bag
    
    def naiveBayes(self,bagOfWords):
        """
            Operates a naive bayes over a bag of words passed in argument with the loaded classifier

        """    
    
        
        results = {}
        #bagOfWords = self._loadRadomBag()


        for label,bag in bagOfWords.items(): 
            if label != "title":
                if label not in results:
                    results[label] = self.priors[label]

                for word,count in bag.items():
                        results[label] = results[label] * ( (self.classifier[label][word] + 1) / (self.lexiconSize + len(self.uniqueWordsSet.union(set(bag.values())))) )
                    
            print(results)
