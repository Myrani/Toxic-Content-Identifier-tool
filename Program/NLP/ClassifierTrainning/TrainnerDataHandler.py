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

    def convertSubmissionToJSONwithDayFolder(self, submission, timestamp):
        """
            Convert a reddit submission comments into a JSON object with a timestamp

        """
        try:
            if submission.author is not None:

                post = {"title": submission.title, "author": submission.author.name,
                        "score": submission.score, "id": submission.id, "url": submission.url, "comments": []}
                submission.comments.replace_more(limit=0)
                comment_queue = submission.comments[:]  # Seed with top-level

                while comment_queue:
                    comment = comment_queue.pop(0)
                    post["comments"].append(self._fetchReplies(comment))

                self._dumpToJSONWithDay(post, timestamp)
        except Exception as e:
            print(e)
            pass

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

        

        