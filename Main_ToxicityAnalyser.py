from Program.NLP.ToxicitySearch.ToxicityAnalyser import ToxicityAnalyser
import praw
from Program.Parameters.Secrets import secrets


reddit = praw.Reddit(
    client_id=secrets["client_id"],
    client_secret=secrets["client_secret"],
    user_agent="Ayrm",
)


analyer = ToxicityAnalyser(reddit)
analyer.loadSpecifiedClassifier("Classifier_2_modified.json")


#analyer.judgeToxicContent_OverCurrentSubreddit_withLimit("leagueoflegends",limit=100)
analyer.judgeToxicContent_SubscribeToSubredditComments("leagueoflegends")
#analyer.judgeToxicContent_SubscribeToSubredditSubmissions("leagueoflegends")
