import praw 
from Program.RedditHarvester.Harvester import Harvester
from Program.Parameters.Secrets import secrets


reddit = praw.Reddit(
    client_id=secrets["client_id"],
    client_secret=secrets["client_secret"],
    user_agent="Ayrm",
)

harvester = Harvester(reddit=reddit)

url = "https://www.reddit.com/r/pushshift/comments/zqjfgv/how_to_change_paras_with_psaw_or_pmaw/"

# harvester.harvestSubmission(url) Works
harvester.harvestSubredditFrom(subreddit="ProgrammerHumor",timedict={"year":2020,"month":1,"day":1},minimumScore=10)

