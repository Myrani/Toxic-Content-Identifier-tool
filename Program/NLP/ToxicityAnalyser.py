import random
from Program.Utils.PathHandler import PathHandler
from Program.Parameters.paths import paths
from Program.RedditExplorer.AccountExplorer import AccountExplorer
import json
import os 

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
        usermetrics = self.accountExplorer.getUserMetrics(username)
        print(usermetrics)



    def _setUpClassifier(self):
        loadedFile = self._loadClassifier()
        self.classifier = loadedFile["classifier"]
        self.priors = loadedFile["priors"]
        self.uniqueWordsSet = set(loadedFile["uniqueWords"])
        self.lexiconSize = loadedFile["lexiconSize"]

    def naiveBayes(self,bagOfWords):
        results = {}
        #bagOfWords = self._loadRadomBag()


        for label,bag in bagOfWords.items(): 
            if label != "title":
                if label not in results:
                    results[label] = self.priors[label]

                for word,count in bag.items():
                        results[label] = results[label] * ( (self.classifier[label][word] + 1) / (self.lexiconSize + len(self.uniqueWordsSet.union(set(bag.values())))) )
                    
            print(results)
