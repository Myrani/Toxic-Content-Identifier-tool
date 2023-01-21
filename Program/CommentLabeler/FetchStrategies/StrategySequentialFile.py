from typing import overload
from Program.CommentLabeler.FetchStrategies.Strategy import Strategy
from Program.Utils.PathHandler import PathHandler
from Program.Parameters.paths import paths
from Program.Utils.WindowsNamingConventionsHandler import WindowsNamingConventionsHandler
import json
import os
import datetime as dt
import random
import shutil

class StrategySequentialFile(Strategy):
    def __init__(self) -> None:
        super().__init__()
        self.pathHandler = PathHandler()
        self.windowsNamingConvention = WindowsNamingConventionsHandler()
        
        self.allMonths =[month for month in os.listdir(self.pathHandler.getRawPostsPath())]
        self.currentMonth = self.allMonths.pop(0)
        self.allDays = [day for day in os.listdir(self.pathHandler.getRawPostsPath()+"/"+self.currentMonth)]
        self.currentDay = self.allDays.pop(0)
        self.currentBuffer = [self.pathHandler.getRawPostsPath()+self.currentMonth+"/"+self.currentDay+"/"+file for file in os.listdir(self.pathHandler.getRawPostsPath()+"/"+self.currentMonth+"/" +self.currentDay)]
        
        print(self.currentMonth,self.currentDay,self.currentBuffer)

    def _moveRawPostOnceLabeled(self,postOld,postNew):
        """

            Function used to archive a RawPost once it has been loaded
        
        """
        
        shutil.move( postOld, postNew)

    def getNextPost(self):
        """
            Get the next post
            Params : None 
            Returns : JSON File 

        """
        file = self.currentBuffer.pop(0)
        
        
        filename = open(file,"r")
        element = json.load(filename)
        filename.close()
        
        self._moveRawPostOnceLabeled(file,self.windowsNamingConvention._cleanName(string=element["title"],directory=self.pathHandler.getDoneRawPostsPath())+".json")
    
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