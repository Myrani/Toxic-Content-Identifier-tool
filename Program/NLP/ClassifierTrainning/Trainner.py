import os
from os import listdir
from os.path import isfile, join
import json
from Program.Utils.PathHandler import PathHandler
from Program.NLP.ToxicityAnalyser import ToxicityAnalyser
class Trainner():
    
    def __init__(self,reddit) -> None:
        """
            Class in charge of the classifier's trainning tools and evaluations metrics

        """

        self.groundTruth = {"Not Toxic":[],"Toxic":[]}
        self.classifier = None
        self.pathHandler = PathHandler()
        self.toxicityAnalyser = ToxicityAnalyser(reddit)

    def loadClassifier(self,classifierFileName):
        """
            Loads a classifier file into the trainner and the toxicity analyser    
        
        """

        data = open(self.pathHandler.getClassifiersPath()+classifierFileName)
        self.classifier = json.load(data)

        self.toxicityAnalyser.loadSpecifiedClassifier(classifierFileName)

    def addGroundTruthPost(self,BaggedPost):
        """
            Add a post into the ground truth disctionnary
        
        """

        for label,content in BaggedPost["content"].items():
            
            self.groundTruth[label].append(content)

    def addListOfGroundTruth_FromLabelisedFolder(self):
        """
        
            Loads every posts present in the LabelisedPost folder
        
        """

        foundPosts = [labelisedPost for labelisedPost in listdir(self.pathHandler.getBagOfWordsPath()) if isfile(join(self.pathHandler.getBagOfWordsPath(), labelisedPost))]

        for post in foundPosts:
            with open(self.pathHandler.getBagOfWordsPath()+post) as file :
                data = json.load(file)
                self.addGroundTruthPost(data)
        
    def _getClassifierPrecision(self,resultMatrix):

        return resultMatrix["truePositive"] / (resultMatrix["truePositive"] + resultMatrix["falsePositive"]+ 0.0001)

    def _getClassifierRecall(self,resultMatrix):

        return resultMatrix["truePositive"] / (resultMatrix["truePositive"] + resultMatrix["falseNegative"]+0.0001)

    def _getClassifierF1Measure(self,resultMatrix):
        precision = self._getClassifierPrecision(resultMatrix)
        recall = self._getClassifierRecall(resultMatrix)
        
        return 2*((precision*recall)/(precision+recall+0.0000000000001))


    def startClassifierTest(self):

        """
            Start the test over the given ground Truths and classifier
        
        """

        resultMatrix = {"truePositive":0,"falsePositive":0,"trueNegative":0,"falseNegative":0}

        for label,labelisedEntitiesList in self.groundTruth.items():
            
            for entity in labelisedEntitiesList:
                bayesResults = self.toxicityAnalyser.naiveBayes_overPost(entity)
            
            # Correct assetion of Toxic Comment
                if bayesResults["Not Toxic"] < bayesResults["Toxic"] and label == "Toxic":
                
                    resultMatrix["truePositive"] = resultMatrix["truePositive"] + 1
            
            # Correct assetion of Not Toxic Comment
                if bayesResults["Not Toxic"] > bayesResults["Toxic"] and label == "Not Toxic":
                    resultMatrix["trueNegative"] = resultMatrix["trueNegative"] + 1
            
            # Wrong assetion of Not Toxic Comment
                if bayesResults["Not Toxic"] > bayesResults["Toxic"] and label == "Toxic":
                    resultMatrix["falseNegative"] = resultMatrix["falseNegative"] + 1

            # Wrong assetion of Toxic Comment
                if bayesResults["Not Toxic"] < bayesResults["Toxic"] and label == "Not Toxic":
                    resultMatrix["flasePositive"] = resultMatrix["falsePositive"] + 1

        

        return resultMatrix

    def scaleUpClassifierToxicity(self):
        
        for word,count in self.classifier["classifier"]["Toxic"].items():
            self.classifier["classifier"]["Toxic"][word] = count * 1.10

        self.toxicityAnalyser.classifier =self.classifier["classifier"]

    def priorsBalancing(self,addToNotToxic,addToToxic):
        
        self.classifier["priors"]["Not Toxic"] = self.classifier["priors"]["Not Toxic"] + addToNotToxic
        self.classifier["priors"]["Toxic"] = self.classifier["priors"]["Toxic"] + addToToxic

        self.toxicityAnalyser.priors =self.classifier["priors"]


    def loopTests(self):
        
        result = self.startClassifierTest()
        precision = self._getClassifierPrecision(result)
        recall = self._getClassifierRecall(result)
        F1Measure = self._getClassifierF1Measure(result)

        while F1Measure < 0.97:
            
            self.scaleUpClassifierToxicity()
            self.priorsBalancing(-0.05,0.05)

            result = self.startClassifierTest()
            precision = self._getClassifierPrecision(result)
            recall = self._getClassifierRecall(result)
            F1Measure = self._getClassifierF1Measure(result)

            print("Result :",result)
            print("Precision :",precision)
            print("Recall",recall)
            print("F1",F1Measure)
            print(self.classifier["priors"])

        self.classifier["title"] = self.classifier["title"] + "_modified"

        self._dumpClassiferToJSON(self.classifier)

    def _dumpClassiferToJSON(self,classifier):
                
        """
            Internal function used to create a JSON file from Raw JSON post
        """
        name = self.pathHandler.getClassifiersPath()+classifier["title"]+""".json"""
        
        with open(name, 'w') as outfile:
            json.dump(classifier, outfile)