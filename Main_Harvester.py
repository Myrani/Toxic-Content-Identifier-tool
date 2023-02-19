import praw
from Program.RedditHarvester.Harvester import Harvester
from Program.Parameters.Secrets import secrets

# Initialisation of the reddit instance with our secret id and key

reddit = praw.Reddit(
    client_id=secrets["client_id"],
    client_secret=secrets["client_secret"],
    user_agent="Ayrm",
)

harvester = Harvester(reddit=reddit) # Passing that instance to our crawler 


harvester.harvestSubredditFrom(subreddit="leagueoflegends", # Specified subreddit to crawl 
                                timedict={"year": 2022, "month": 12, "day": 1}, # Starting day, will crawl until the current day is reached
                                minimumScore=10) # Specified minimum post score,  

