from calendar import month
import json
import os
import datetime as dt
import random

class DataLabeler():
    """
        Used to label post with the sentiment 
    """


    def __init__(self,pathHandler) -> None:
        self.pathHandler = pathHandler


    def _askForOpinion(self,string):
        """
            Function to ask the sentiment of the post and it's replies
        """

        return int(input("How's this ?"))
        

    def _fetchNextStringToLabel(self,comment):

        """
            Recursively parcour the replies and ask for a label
        """

        comment["Label"] = self._askForOpinion(comment["body"])
        for reply in comment["replies"]:
            self._fetchNextStringToLabel(reply)
       

    def _labelPost(self,post):
        """
            function used to lauch the Labeling process over a post 
        
        """

        post["Label"] = self._askForOpinion(post["title"])
        
        for comment in post["comments"]:
            self._fetchNextStringToLabel(comment)


        return post
    
    def _cleanName(self,directory,string):
        """
            Clean the post name to fit the OS file name formatting 
        """

        string = directory+string.replace(":","colon").replace("?","questionmark").replace("\"","DoubleQuote").replace("/","SlashForward").replace("\\","SlashBackward").replace("<","inferior").replace(">","greater").replace("*","asterisk").replace("|","BarSymbol").replace(".","Dot").replace("'"," ")
        if len(string) > 253:
            string = string[0:220]
            return string
        return string 


    def loadPostsFromDirectory(self,dir_path):
        """
            Input of the program, loads in a RawPost, calls in the labelisation process, and saves it to the LabeledPost Directory

        """
        postList = []

        for path in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                postList.append(dir_path+path)


        return postList

    def _selectRandomMonth(self):
        """
            Select a Random month from the RawPosts Directory .
        """

        allMonths =[month for month in os.listdir(self.pathHandler.getRawPostsPath())]
        return allMonths[random.randint(0, len(allMonths)-1)]

    def _selectRandowDay(self):
        """
            Select a Random day from the random month selected .
        
        """

        month = self._selectRandomMonth()
        allDays =[day for day in os.listdir(self.pathHandler.getRawPostsPath()+month)]

        return (month,allDays[random.randint(0, len(allDays)-1)])


    def loadRandomPostsFromRandomDirectory(self):
        tupleMonthDay = self._selectRandowDay()
        rootPath = self.pathHandler.getRawPostsPath()

        return [rootPath+tupleMonthDay[0]+"/"+tupleMonthDay[1]+"/"+file for file in os.listdir(rootPath+"/"+tupleMonthDay[0]+"/" +tupleMonthDay[1])]


    def _saveLabeledPost(self,post):

        """
            Takes in a labeled post and dump it the the Labeled post Folder
        
        
        """

        currentFolder = self.pathHandler.getLabeledPostsPath()
        oldFolder = self.pathHandler.getRawPostsPath()
        newFolder = self.pathHandler.getDoneRawPostsPath()

        cleanName = self._cleanName(currentFolder,post["title"])+""".json"""
        rawPath = self._cleanName(oldFolder,post["title"])+""".json"""
        newPath = self._cleanName(newFolder,post["title"])+""".json"""

        with open(cleanName, 'w') as outfile:
            json.dump(post, outfile)

        
