from typing import overload
from Program.CommentLabeler.FetchStrategies.Strategy import Strategy
from Program.Utils.PathHandler import PathHandler
from Program.Parameters.paths import paths
import json
import os
import datetime as dt
import random


class StrategySequentialFile(Strategy):
    def __init__(self) -> None:
        super().__init__()
        self.pathHandler = PathHandler(paths=paths)
        
        self.allMonths =[month for month in os.listdir(self.pathHandler.getRawPostsPath())]
        self.currentMonth = self.allMonths.pop(0)
        self.allDays = [day for day in os.listdir(self.pathHandler.getRawPostsPath()+"/"+self.currentMonth)]
        self.currentDay = self.allDays.pop(0)
        self.currentBuffer = [self.pathHandler.getRawPostsPath()+"/"+self.currentMonth+"/"+self.currentDay+"/"+file for file in os.listdir(self.pathHandler.getRawPostsPath()+"/"+self.currentMonth+"/" +self.currentDay)]
        
        print(self.currentMonth,self.currentDay,self.currentBuffer)

    def getNextPost(self):
        """
            Get the next post
            Params : None 
            Returns : JSON File 

        """
        with open(self.currentBuffer.pop(0)) as filename:
            element = json.load(filename)

            if not self.currentBuffer:
                self._refillBuffer()
        
            return element


    def _refillBuffer(self):
        """
        function to call when the post buffer is depleted and needs new posts
        Params : None
        Returns : None
        """
        if not self.currentBuffer: # Si buffer de post vide 
            
            if not self.allDays: # Si buffer de jours vide 
                self.currentMonth = self.allMonths.pop(0)
                self.allDays = [day for day in os.listdir(self.pathHandler.getRawPostsPath()+"/"+self.currentMonth)]
                self.currentDay = self.allDays.pop(0)
                self.currentBuffer = [self.pathHandler.getRawPostsPath()+"/"+self.currentMonth+"/"+self.currentDay+"/"+file for file in os.listdir(self.pathHandler.getRawPostsPath()+"/"+self.currentMonth+"/" +self.currentDay)]
            
            else : # Si il reste des jours dans le buffer de jours
                self.currentDay = self.allDays.pop(0)
                self.currentBuffer = [self.pathHandler.getRawPostsPath()+"/"+self.currentMonth+"/"+self.currentDay+"/"+file for file in os.listdir(self.pathHandler.getRawPostsPath()+"/"+self.currentMonth+"/" +self.currentDay)]