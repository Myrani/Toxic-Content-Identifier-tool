import praw
from Program.RedditHarvester.DataHandler import DataHandler

from psaw import PushshiftAPI
import datetime as dt

class Harvester():
    def __init__(self,reddit) -> None:
        
        self.reddit = reddit
        self.api = PushshiftAPI(reddit)
        self.datahandler = DataHandler()

    def _generateScrapingManifest(self):
        """
            Todo : Function keeping track of where and what task the harvester has done and what was left to do in case of emergency shutdow

            To stock into Parameters/Manifests/ ... 
        
        """
        pass

    def harvestSubredditFrom(self,subreddit,timedict,minimumScore):

        """
            subreddit : str  , subreddit to harvest (case sensitive)
            timedict : {day,month,year} the day you want to start 
            minimumScore : int , Minimum score needed to be harvested

        """

        currentday = dt.datetime(timedict["year"],timedict["month"] , timedict["day"])

        while currentday != dt.datetime.today():
            
            start_epoch=int(currentday.timestamp())
            nextDay = currentday + dt.timedelta(days = 1)
            end_epoch=int(nextDay.timestamp())


            listOfIDs = list(self.api.search_submissions(after=start_epoch,
                            before=end_epoch,
                            subreddit=subreddit,
                            score = str(">"+str(minimumScore)),
                            limit=None))

            self.harvestFromIdList(listOfIDs,start_epoch)

            currentday = currentday+dt.timedelta(days = 1)

    def harvestFromIdList(self,listOfIDs,timestamp):
        """
            Harvest a submissions by looping over a given list of submission Id
        """
        for id in listOfIDs:
            submission = self.reddit.submission(id)
            self.datahandler.convertSubmissionToJSONwithDayFolder(submission,timestamp)

    def harvestSubreddit(self,subreddit,mode,limit):
        """
            Harvest a subreddit top post of the day within the set limit
        """

        for submission in self.reddit.subreddit(subreddit).hot(limit=limit):
            self.datahandler.convertSubmissionToJSON(submission)

    def harvestSubmission(self,url):
        """
            Harvest a peculiar submission from a reddit url
        """

        submission = self.reddit.submission(url=url)
        self.datahandler.convertSubmissionToJSON(submission)
