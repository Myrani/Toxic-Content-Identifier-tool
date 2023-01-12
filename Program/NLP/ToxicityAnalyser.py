import random
from Program.Utils.PathHandler import PathHandler
from Parameters.paths import paths
import json
import os 

class ToxicityAnalyser():

    def __init__(self,classifierName) -> None:
        
        # Basic info setup 
        self.pathHandler = PathHandler(paths=paths)
        self.classifierName = classifierName
        
        # PlaceHolder 
        self.classifier = None
        self.priors = {}
        self.uniqueWordsSet = {}
        self.lexiconSize = 0

        self._setUpClassifier()

    def _loadClassifier(self):
    
        data = open(self.pathHandler.getClassifiersPath()+self.classifierName+""".json""")
        return json.load(data)
    
    

    def _getRandomBag(self):

        """
            Internal function used to get all bags of words in the BagOfWords Folder 
        
        """
        liste = os.listdir(self.pathHandler.getBagOfWordsPath())
        return liste[random.randint(0,len(liste)-1)]


    def _loadRadomBag(self):

        """
            Internal function used to load the data from a specified bag of words
        
        """
        data = open(self.pathHandler.getBagOfWordsPath()+self._getRandomBag())
        return json.load(data)
    


    def _setUpClassifier(self):
        loadedFile = self._loadClassifier()
        self.classifier = loadedFile["classifier"]
        self.priors = loadedFile["priors"]
        self.uniqueWordsSet = set(loadedFile["uniqueWords"])
        self.lexiconSize = loadedFile["lexiconSize"]

    def naiveBayes(self):
        results = {}
        bagOfWords = self._loadRadomBag()


        for label,bag in bagOfWords.items(): 
            if label != "title":
                if label not in results:
                    results[label] = self.priors[label]

                for word,count in bag.items():
                        results[label] = results[label] * ( (self.classifier[label][word] + 1) / (self.lexiconSize + len(self.uniqueWordsSet.union(set(bag.values())))) )
                    
            print(results)
