import time
import json
import os.path
import datetime as dt 
from Program.Utils.PathHandler import PathHandler
from Program.Utils.WindowsNamingConventionsHandler import WindowsNamingConventionsHandler


class ToxicityAnalyserDataHandler():
    def __init__(self) -> None:

        """
            Handles the saving/reading/loadings interactions for the ToxicityAnalyser
        
        """
        self.pathHandler = PathHandler()
        self.namingHandler = WindowsNamingConventionsHandler()
    
    def _generateBaseFile(self):
        """
            Create the base json file to track the comments
        """
        file = {"Name":"ToxicCommentsList.json","Comments":[]}
        name = self.pathHandler.getToxicFlaggedContentsFilePath()+"ToxicCommentsList.json"

        json_baseFile = json.dumps(file)

        with open(name, 'w') as outfile:
            outfile.write(json_baseFile)


    def dumpToxicCommentToListJSON(self,comment):
        """
            Internal function used to create a JSON file from a reddit post converted into a dictionnary 
        """
        arr = os.listdir(self.pathHandler.getToxicFlaggedContentsFilePath())

        if not arr:
            self._generateBaseFile()
        
        name = self.pathHandler.getToxicFlaggedContentsFilePath()+"ToxicCommentsList.json"

        with open(name, "r") as jsonFile:
            data = json.load(jsonFile)
            
        data["Comments"].append(comment)
            
        with open(name, "w") as jsonFile:
            json.dump(data, jsonFile)
        


