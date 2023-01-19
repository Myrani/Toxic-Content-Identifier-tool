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

