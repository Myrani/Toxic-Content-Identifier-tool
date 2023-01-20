from Program.NLP.ClassifierTrainning.Trainner import Trainner
import praw
from Program.Parameters.Secrets import secrets


reddit = praw.Reddit(
    client_id=secrets["client_id"],
    client_secret=secrets["client_secret"],
    user_agent="Ayrm",
)

trainner = Trainner(reddit)

trainner.loadClassifier("Classifier_1.json")
trainner.addListOfGroundTruth_FromLabelisedFolder()
print(trainner.loopTests())