import time
import json
import os.path
import datetime as dt 
from Program.Utils.PathHandler import PathHandler


class ExplorerDataHandler():
    def __init__(self) -> None:
        self.pathHandler = PathHandler()



    def convertSubmissionToJSONwithDayFolder(self,submission,timestamp):
        """
            Convert a reddit submission comments into a JSON object with a timestamp
        
        """
        try : 
            post = {"title":submission.title,"author":submission.author.name,"score":submission.score,"id":submission.id,"url":submission.url,"comments":[]}
            submission.comments.replace_more(limit=0)
            comment_queue = submission.comments[:]  # Seed with top-level
        
            while comment_queue:
                comment = comment_queue.pop(0)
                post["comments"].append(self._fetchReplies(comment))

            self._dumpToJSONWithDay(post,timestamp)
        except Exception as e:
            print(e)
            pass
    
    def _dumpToJSONWithDay(self,post,timestamp):
        """
            Internal function used to create a JSON file from a reddit post converted into a dictionnary and save it in a special day folder
        """
        currentTopFolder = self.pathHandler.getRawPostsPath()+dt.datetime.fromtimestamp(timestamp).strftime('%m-%y')+"""/"""
        currentFolder = self.pathHandler.getRawPostsPath()+dt.datetime.fromtimestamp(timestamp).strftime('%m-%y')+"""/"""+dt.datetime.fromtimestamp(timestamp).strftime('%d-%m-%y')+"""/"""

        if not os.path.isdir(currentTopFolder):
            os.mkdir(currentTopFolder)

        if not os.path.isdir(currentFolder):
            os.mkdir(currentFolder)

        cleanName = self._cleanName(currentFolder,post["title"])
        
        with open(cleanName, 'w') as outfile:
            json.dump(post, outfile)
    
    
    def _fetchReplies(self,comment):
        """
            Internal function used to fetch comments in a Depth First manners .
        """
        try :
            commentDict = {"commentId":comment.id,"author":comment.author.name,"body":comment.body,"score":comment.score,"replies":[]}
        
            if comment.replies:
                for reply in comment.replies:
                    commentDict["replies"].append(self._fetchReplies(reply))

            return commentDict
        except Exception as e :
            pass

    def convertSubmissionToJSON(self,submission):
        """
            Convert a reddit submission comments into a JSON object
        
        """

        post = {"title":submission.title,"author":submission.author.name,"score":submission.score,"id":submission.id,"url":submission.url,"content":submission.selftext,"comments":[]}
        submission.comments.replace_more(limit=0)
        comment_queue = submission.comments[:]  # Seed with top-level
        
        while comment_queue:
            comment = comment_queue.pop(0)
            post["comments"].append(self._fetchReplies(comment))

        self._dumpToJSON(post)
    
    def _dumpToJSON(self,metrics):
        """
            Internal function used to create a JSON file from a reddit post converted into a dictionnary 
        """

        with open(self._cleanName(self.pathHandler.getRawPostsPath(),metrics["username"]), 'w') as outfile:
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

    def _fetchNextPrint(self,comment,deepness):
        """
            Internal function to fetch reaction comments and print it with the correct indentation
        """
        if comment['replies'] != "":
            print("   "*deepness*3,comment["body"])
            for reply in comment["replies"]:
                self._fetchNextPrint(reply,deepness+1)
                    
    def prettyPrint(self,post):
        """
            Internal function to showcase a comments chains from a post in the terminal
        """
        for comment in post["comments"]:
            self._fetchNextPrint(comment,1)

