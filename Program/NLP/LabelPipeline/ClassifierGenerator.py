from Program.Utils.PathHandler import PathHandler
from Program.Parameters.paths import paths
import os
import json
import random


class ClassifierGenerator():
    
    def __init__(self) -> None:
        """
            Creates a Classifer from BagOfWord Structure
        
        """

        self.pathHandler = PathHandler()

    def _getAllBagOfWords(self):
        """
            Internal function used to get all bags of words in the BagOfWords Folder 
        
        """
        #print(os.listdir(self.pathHandler.getBagOfWordsPath()))
        return os.listdir(self.pathHandler.getBagOfWordsPath())

    def _getAllClassifiers(self):
        """
            Internal function used to get all bags of words in the BagOfWords Folder 
        
        """
        return os.listdir(self.pathHandler.getClassifiersPath())

    def _loadRefinedBag(self,name):

        """
            Internal function used to load the data from a specified bag of words
        
        """
        data = open(self.pathHandler.getBagOfWordsPath()+name)
        return json.load(data)
    

    def _dumpClassiferToJSON(self,classifier):
                
        """
            Internal function used to create a JSON file from Raw JSON post
        """
        name = self.pathHandler.getClassifiersPath()+classifier["title"]+""".json"""
        
        with open(name, 'w') as outfile:
            json.dump(classifier, outfile)

    def _determinePriors(self,priors):

        """
            Generate the final priors after all the bags have been computed, could be optimised 
            
            Args : Priors Dict

            returns : Priors Dict, but better
        """

        cpt = 0
        for key,value in priors.items():
            cpt+=value

        for key,value in priors.items():
            priors[key] = value/cpt

        return priors
    
    def generateClassifierFromAllBags(self):
        """
            Master Function
            Generates a Classifier from all available BagOfWords
        
            Args : None 

            Returns : None

        """
        
        # Setting up main variables

        file = {}
        classifier = {}
        priors = {}

        bufferUniqueWordsList = []
        bufferLexiconSize = 0





        for bag in self._getAllBagOfWords():
            loadedBag = self._loadRefinedBag(bag)
            for label,words in loadedBag["content"].items() :
                #print(label,words)
                
                if label != "title":
                    if label not in classifier:
                        classifier[label] = {}
                        priors[label] = 0
                    
                    priors[label] = priors[label] + 1
                    for word,count in words.items():
                        if word not in classifier[label]:
                            classifier[label][word] = count
                            bufferUniqueWordsList.append(word)
                            bufferLexiconSize += 1
                        else:
                            classifier[label][word] = classifier[label][word] + count
                            bufferUniqueWordsList.append(word)
                            bufferLexiconSize += 1
        
        
        file["title"] = "Classifier_"+str(len(self._getAllClassifiers()))
        
        file["classifier"] = classifier
        file["priors"] = self._determinePriors(priors)
        file["uniqueWords"] = list(set(bufferUniqueWordsList))
        file["lexiconSize"] = bufferLexiconSize

        self._dumpClassiferToJSON(file)

    def generateClassifierFromAllBags_WithToxicityUpScaleFactor(self,upscaleFactor = 0.1):

        """
            Master Function
            Generates a Classifier from all available BagOfWords
        
            Args : None 

            Returns : None

        """

        # Setting up main variables


        file = {}
        classifier = {}
        priors = {}

        bufferUniqueWordsList = []
        bufferLexiconSize = 0


        # Toxicity scale up variables

        toxiContentBuffer = []


        for bag in self._getAllBagOfWords():
            loadedBag = self._loadRefinedBag(bag)
            for label,words in loadedBag["content"].items() :
                
                if label == "Toxic":
                    toxiContentBuffer.append(words)
                if label != "title":
                    if label not in classifier:
                        classifier[label] = {}
                        priors[label] = 0
                    
                    priors[label] = priors[label] + 1
                    for word,count in words.items():
                        if word not in classifier[label]:
                            classifier[label][word] = count
                            bufferUniqueWordsList.append(word)
                            bufferLexiconSize += 1
                        else:
                            classifier[label][word] = classifier[label][word] + count
                            bufferUniqueWordsList.append(word)
                            bufferLexiconSize += 1
        
        
        selectedToxicity = random.sample(toxiContentBuffer,int((priors["Toxic"]+priors["Not Toxic"])*upscaleFactor))

  
        for bag in selectedToxicity:
            priors["Toxic"] = priors["Toxic"] + 1
            for word,count in bag.items():
                if word not in classifier[label]:
                    classifier["Toxic"][word] = count
                    bufferUniqueWordsList.append(word)
                    bufferLexiconSize += 1
                else:
                    classifier["Toxic"][word] = classifier["Toxic"][word] + count
                    bufferLexiconSize += 1

        print("Current contents",priors["Toxic"]+priors["Not Toxic"])

        file["title"] = "Classifier_"+str(len(self._getAllClassifiers()))
        
        file["classifier"] = classifier
        file["priors"] = self._determinePriors(priors)
        file["uniqueWords"] = list(set(bufferUniqueWordsList))
        file["lexiconSize"] = bufferLexiconSize

        self._dumpClassiferToJSON(file)