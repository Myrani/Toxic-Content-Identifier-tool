import time
import json
import os.path
import datetime as dt
from Program.Utils.PathHandler import PathHandler
from Program.NLP.LabelPipeline.PostRefiner import PostRefiner
from Program.NLP.LabelPipeline.PostBagger import PostBagger

class TrainnerDataHandler():

    
    def __init__(self) -> None:
        self.pathHandler = PathHandler()
        self.postBagger = PostBagger() 
        self.currentMonth = ""
        self.currentDay = ""
        self.monthsFoldersList = []
        self.daysFoldersList = []

        self._setUpMonthsAndDays()


    def _setUpMonthsAndDays(self):
        
        self.monthsFoldersList = [month for month in os.listdir(self.pathHandler.getRawPostsPath())]
        self.currentMonth = self.monthsFoldersList.pop(0)
        self.daysFoldersList = [day for day in os.listdir(self.pathHandler.getRawPostsPath()+"/"+self.currentMonth)]

    def _refillDaysBuffer(self):

        if self.monthsFoldersList:
            self.currentMonth = self.monthsFoldersList.pop(0)
            self.daysFoldersList = [day for day in os.listdir(self.pathHandler.getRawPostsPath()+"/"+self.currentMonth)]
        else:
            print("All the files are done !")
            return None 

    def fetchRawPosts_NewDay(self):
        

        if not self.daysFoldersList:
            self._refillDaysBuffer()

        self.currentDay = self.daysFoldersList.pop(0)
        return [self.pathHandler.getRawPostsPath()+self.currentMonth+"/"+self.currentDay+"/"+file for file in os.listdir(self.pathHandler.getRawPostsPath()+self.currentMonth+"/"+self.currentDay)]

        

        