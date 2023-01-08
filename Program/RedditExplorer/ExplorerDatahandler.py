import time
import json
import os.path
import datetime as dt 
from Program.Utils.PathHandler import PathHandler


class ExplorerDataHandler():
    def __init__(self) -> None:
        self.pathHandler = PathHandler()


    
    def _dumpToJSON(self,metrics):
        """
            Internal function used to create a JSON file from a reddit post converted into a dictionnary 
        """

        with open(self._cleanName(self.pathHandler.getUsersMetricsFilePath(),metrics["username"]), 'w') as outfile:
            json.dump(metrics, outfile)
    
    def _cleanName(self,directory,string):
        """
            Clean the post name to fit the OS file name formatting 
        """

        string = directory+string.replace(":","colon").replace("?","questionmark").replace("\"","DoubleQuote").replace("/","SlashForward").replace("\\","SlashBackward").replace("<","inferior").replace(">","greater").replace("*","asterisk").replace("|","BarSymbol").replace(".","Dot").replace("'"," ")
        if len(string) > 253:
            string = string[0:220]
            return string
        return string+".json"  


