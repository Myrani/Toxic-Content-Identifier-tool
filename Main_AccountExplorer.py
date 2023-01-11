import praw
from Program.RedditHarvester.Harvester import Harvester
from Program.RedditExplorer.AccountExplorer import AccountExplorer 
from Program.Parameters.Secrets import secrets



reddit = praw.Reddit(
    client_id=secrets["client_id"],
    client_secret=secrets["client_secret"],
    user_agent="Ayrm",
)

explorer = AccountExplorer(reddit=reddit)

explorer.harvestUserMetrics("Myrani")

