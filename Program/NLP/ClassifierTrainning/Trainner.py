import os
from os import listdir
from os.path import isfile, join
import json
from Program.Utils.PathHandler import PathHandler
from Program.NLP.ToxicitySearch.ToxicityAnalyser import ToxicityAnalyser
from Program.NLP.ClassifierTrainning.TrainnerDataHandler import TrainnerDataHandler
from Program.NLP.LabelPipeline.PostRefiner import PostRefiner
from Program.NLP.LabelPipeline.PostBagger import PostBagger
class Trainner():
    
    def __init__(self,reddit) -> None:
        """
            Class in charge of the classifier's trainning tools and evaluations metrics

        """
    
        self.groundTruth = {"Not Toxic":[],"Toxic":[]}
        self.classifier = None
        self.pathHandler = PathHandler()
        self.toxicityAnalyser = ToxicityAnalyser(reddit)
        self.dataHandler = TrainnerDataHandler()
        self.postRefiner = PostRefiner()
        self.postBagger = PostBagger()

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
        
            Loads every posts present in the LabelisedPost folder as ground truths to test the classifier
        
        """

        foundPosts = [labelisedPost for labelisedPost in listdir(self.pathHandler.getBagOfWordsPath()) if isfile(join(self.pathHandler.getBagOfWordsPath(), labelisedPost))]

        for post in foundPosts:
            with open(self.pathHandler.getBagOfWordsPath()+post) as file :
                data = json.load(file)
                self.addGroundTruthPost(data)

    def fectchNextDayContent_RawPosts(self):
        
        """
        
            Fetch a new day Raw posts contents            
        
        """

        return self.dataHandler.fetchRawPosts_NewDay()



    

    


    def _getClassifierPrecision(self,resultMatrix):
        """
            Returns the precision of classifier over a test data set
        """
        return resultMatrix["truePositive"] / (resultMatrix["truePositive"] + resultMatrix["falsePositive"]+ 0.0001)

    def _getClassifierRecall(self,resultMatrix):
        """
            Returns the recall of classifier over a test data set
        """
        return resultMatrix["truePositive"] / (resultMatrix["truePositive"] + resultMatrix["falseNegative"]+0.0001)

    def _getClassifierF1Measure(self,resultMatrix):

        """
            Returns the F1 measure of classifier over a test data set
        """
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

    def scaleUpClassifierToxicity(self,scaleFactor):

        """
            Function to manually change the Toxic word frequency of a classifier 
                
        """

        for word,count in self.classifier["classifier"]["Toxic"].items():
            self.classifier["classifier"]["Toxic"][word] = count * scaleFactor

        self.toxicityAnalyser.classifier =self.classifier["classifier"]

    def priorsBalancing(self,addToNotToxic,addToToxic):

        """
            Function to manually change the priors of a classifier

        """


        self.classifier["priors"]["Not Toxic"] = self.classifier["priors"]["Not Toxic"] + addToNotToxic
        self.classifier["priors"]["Toxic"] = self.classifier["priors"]["Toxic"] + addToToxic

        self.toxicityAnalyser.priors =self.classifier["priors"]


    def _fetchDeeperComments(self,commentStructure):
        
        results = self.toxicityAnalyser.naiveBayes_overComment(commentStructure["body"])
        
        if results["Toxic"] > results["Not Toxic"]:
            self.toxicityAnalyser._toxicityFlagging((commentStructure["author"],commentStructure["body"]))

        if commentStructure["replies"]:
            for comment in commentStructure["replies"]:
           
                self._fetchDeeperComments(comment)

    def startNaiveBayesOverPost(self,post):


        if post["content"]:

            results = self.toxicityAnalyser.naiveBayes_overComment(post["content"]["body"])

            if results["Toxic"] > results["Not Toxic"]:
                self.toxicityAnalyser._toxicityFlagging((post["author"],post["body"]))

            if post["content"]["comments"]:
                for comment in post["content"]["comments"] :
                
                    self._fetchDeeperComments(comment)

    def testClassifier_OverCurrentRawPosts(self):
        """
            Test the current classifier over the RawPosts present
        
        """
        for post in self.fectchNextDayContent_RawPosts():
            data = open(post)
            loadedRawPost = (json.load(data))
            tokenisedRawPost = self.postRefiner.refineARawPost(loadedRawPost)
            self.startNaiveBayesOverPost(tokenisedRawPost)


    def loopTests_UpscaleToxicContent(self):
        """
            Upscale toxic content until a minimum F1 measure of 0.97 is reached
        
        """
        result = self.startClassifierTest()
        precision = self._getClassifierPrecision(result)
        recall = self._getClassifierRecall(result)
        F1Measure = self._getClassifierF1Measure(result)

        while F1Measure < 0.97:
            
            self.scaleUpClassifierToxicity(0.10)
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