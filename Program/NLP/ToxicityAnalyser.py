import random
from Program.Utils.PathHandler import PathHandler
from Program.Parameters.paths import paths
from Program.RedditExplorer.AccountExplorer import AccountExplorer
import json
import os 
import nltk

class ToxicityAnalyser():

    def __init__(self,reddit) -> None:
        
        """
            Bridge class over the NLP side and Reddit API .
            Once a classifier is loaded, this class serves as a comment analyser
            of a given profile .
        
        """


        # Basic info setup 
        self.pathHandler = PathHandler()
        self.accountExplorer = AccountExplorer(reddit=reddit)
        
        # PlaceHolder 
        self.classifier = None
        self.loadedFile = None
        self.priors = {}
        self.uniqueWordsSet = {}
        self.lexiconSize = 0



    def loadSpecifiedClassifier(self,name):
        """
            Loads a classifier with the given name
            
        """
        
        data = open(self.pathHandler.getClassifiersPath()+name)
        
        self.loadedFile =  json.load(data)

        self._setUpClassifier()


    
    def _judgeUseretrics(self,username):
        """
            Harvest all public specific user data 
        
        """
        ### self.accountExplorer.harvestUserMetrics(username)
        ###self.accountExplorer.explorerDataHandler._dumpBaggedProfileToJSON(self._convertRawUserMetricsToBagOfWords(username))
        self.naiveBayes_overProfile(self.accountExplorer.explorerDataHandler._loadUserBaggedMetrics(username))        


    def _setUpClassifier(self):

        """
            Loads all the specs of a classifier : name, priors, uniquewords, lexiconsize, Classifier 
        
        """

    
        self.classifier = self.loadedFile["classifier"]
        self.priors = self.loadedFile["priors"]
        self.uniqueWordsSet = set(self.loadedFile["uniqueWords"])
        self.lexiconSize = self.loadedFile["lexiconSize"]


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
        
        for key,value in usermetrics["posts"].items():
            for comment in value:
                for word in self._tokenizeComment(comment["content"]):

                    if word in bag["bag"]:
                        bag["bag"][word] = bag["bag"][word] + 1
                    else:
                        bag["bag"][word] = 1             
 
        
        
        return bag
    
    def naiveBayes_overProfile(self,baggedUserProfile):
        """
            Operates a naive bayes over a bag of words passed in argument with the loaded classifier

        """    

        results = dict.fromkeys(self.priors,1.0)

        for word,count in baggedUserProfile["bag"].items(): 
            for prior in results.keys():
                if word in self.classifier[prior]:
                    results[prior] = results[prior] * self.priors[prior] * ( (self.classifier[prior][word] + 1) / (self.lexiconSize + len(self.uniqueWordsSet.union(set(baggedUserProfile["bag"].values())))))
                else:
                     results[prior] = results[prior] * self.priors[prior] * ( 1 / (self.lexiconSize + len(self.uniqueWordsSet.union(set(baggedUserProfile["bag"].values())))))
                
                if results[prior] == 0:
                    return results
        
        return results


    def naiveBayes_overPost(self,baggedUserPost):
        """
            Operates a naive bayes over a bag of words passed in argument with the loaded classifier

        """    

        results = dict.fromkeys(self.priors,1.0)

        for word,count in baggedUserPost.items(): 
            
            for prior in results.keys():
                if word in self.classifier[prior]:
                    results[prior] = results[prior] * self.priors[prior] * ( (count + 1) / (self.lexiconSize + len(self.uniqueWordsSet.union(set(baggedUserPost.keys())))))
                else:
                     results[prior] = results[prior] * self.priors[prior] * ( 1 / (self.lexiconSize + len(self.uniqueWordsSet.union(set(baggedUserPost.keys())))))
                
                if results[prior] == 0:
                    return results
        
        return results