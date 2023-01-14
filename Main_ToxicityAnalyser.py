from Program.NLP.ToxicityAnalyser import ToxicityAnalyser
import praw
from Program.Parameters.Secrets import secrets


reddit = praw.Reddit(
    client_id=secrets["client_id"],
    client_secret=secrets["client_secret"],
    user_agent="Ayrm",
)


analyer = ToxicityAnalyser("Classifier_0.json",reddit)

analyer._judgeUseretrics("Myrani")