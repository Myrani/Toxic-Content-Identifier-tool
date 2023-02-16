from Program.NLP.ClassifierTrainning.Trainner import Trainner
import praw
from Program.Parameters.Secrets import secrets


reddit = praw.Reddit(
    client_id=secrets["client_id"],
    client_secret=secrets["client_secret"],
    user_agent="Ayrm",
)

trainner = Trainner(reddit)

trainner.loadClassifier("Classifier_2.json") # Loads a classifier to train
#trainner.addListOfGroundTruth_FromLabelisedFolder() # Adds all labeled posts as ground truth data
#trainner.loopTests_UpscaleToxicContent() # Starts scaling up toxic contents 

print(trainner.testClassifier_OverCurrentRawPosts())