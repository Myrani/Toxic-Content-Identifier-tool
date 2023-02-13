from Program.Parameters.paths import paths

class PathHandler():

    def __init__(self) -> None:
        """
            Handles the Path logic into the program

        """
        
        self.path = paths

    def getRawPostsPath(self):
        return self.path["RawPostsFilePath"]
    
    def getDoneRawPostsPath(self):
        return self.path["DoneRawPostsFilePath"]

    def getRefinedPostsPath(self):
        return self.path["RefinedPostsFilePath"]

    def getLabeledPostsPath(self):
        return self.path["LabeledPostsFilePath"]

    def getBagOfWordsPath(self):
        return self.path["BagOfWordsFilePath"]

    def getClassifiersPath(self):
        return self.path["ClassifiersFilePath"]

    def getParametersPath(self):
        return self.path["ParametersFileFilePath"]

    def getLabelSetsPath(self):
        return self.path["LabelSetsFileFilePath"]
    
    def getRawUserMetricsFilePath(self):
        return self.path["RawUserMetricsFilePath"]

    def getBaggedUserMetricsFilePath(self):
        return self.path["BaggedUserMetricsFilePath"]

    def getToxicFlaggedContentsFilePath(self):
        return self.path["ToxicFlaggedContentsFilePath"]


        