from Program.NLP.ToxicitySearch.ToxicityAnalyser import ToxicityAnalyser
import praw
from Program.Parameters.Secrets import secrets


reddit = praw.Reddit(
    client_id=secrets["client_id"],
    client_secret=secrets["client_secret"],
    user_agent="Ayrm",
)


analyer = ToxicityAnalyser(reddit)

analyer.loadSpecifiedClassifier("Classifier_2_modified.json") # Loads a given classifer to analyse new contents with 
 
analyer.judgeToxicContent_SubscribeToSubredditComments("DotA2") # Subscribe to a subreddit new comments stream
