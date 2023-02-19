from Program.NLP.ToxicitySearch.ToxicityAnalyser import ToxicityAnalyser
import praw
from Program.Parameters.Secrets import secrets


# Initialisation of our reddit instance with our private id and key
reddit = praw.Reddit(
    client_id=secrets["client_id"],
    client_secret=secrets["client_secret"],
    user_agent="Ayrm",
)


analyer = ToxicityAnalyser(reddit)

analyer.loadSpecifiedClassifier("Classifier_1_modified.json") # Loads a given classifer to analyse new contents with 
 
analyer.judgeToxicContent_SubscribeToSubredditComments("DotA2") # Subscribe to a subreddit new comments stream
