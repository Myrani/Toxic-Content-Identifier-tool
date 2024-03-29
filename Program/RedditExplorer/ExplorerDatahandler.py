import time
import json
import os.path
import datetime as dt 
from Program.Utils.PathHandler import PathHandler
from Program.Utils.WindowsNamingConventionsHandler import WindowsNamingConventionsHandler


class ExplorerDataHandler():
    def __init__(self) -> None:

        """
            Handles the saving/reading/loadings interactions  
        
        """
        self.pathHandler = PathHandler()
        self.namingHandler = WindowsNamingConventionsHandler()
    
    def _dumpToJSON(self,metrics):
        """
            Internal function used to create a JSON file from a reddit post converted into a dictionnary 
        """

        with open(self.namingHandler._cleanName(self.pathHandler.getRawUserMetricsFilePath(),metrics["username"]), 'w') as outfile:
            json.dump(metrics, outfile)
    
    def _dumpBaggedProfileToJSON(self,baggedProfile):

        with open(self.namingHandler._cleanName(self.pathHandler.getBaggedUserMetricsFilePath(),baggedProfile["username"])+".json", 'w') as outfile:
            json.dump(baggedProfile, outfile)


    def _loadUserMetrics(self,username):

        """
            Loads a saved userMetrics file and returns its content
        
        """

        filename = self.pathHandler.getRawUserMetricsFilePath()+username+".json"

        with open(filename, 'r') as userMetrics:
            MetricsJson = json.loads(userMetrics.read())
            
            return MetricsJson

    def _loadUserBaggedMetrics(self,username):

        """
            Loads a saved userMetrics file and returns its content
        
        """

        filename = self.pathHandler.getBaggedUserMetricsFilePath()+username+".json"

        with open(filename, 'r') as userMetrics:
            MetricsJson = json.loads(userMetrics.read())
            
            return MetricsJson
