from Program.NLP.ClassifierTrainning.Trainner import Trainner
import praw
from Program.Parameters.Secrets import secrets


# Initialisation of our reddit instance with our private id and key
reddit = praw.Reddit(
    client_id=secrets["client_id"],
    client_secret=secrets["client_secret"],
    user_agent="Ayrm",
)

trainner = Trainner(reddit)

trainner.loadClassifier("Classifier_0.json") # Loads a classifier to train

trainner.addListOfGroundTruth_FromLabelisedFolder() # Adds all labeled posts as ground truth data, needed for the LoopTestFunction 

trainner.loopTests_UpscaleToxicContent(upscaleStep=0.10) # Starts scaling up toxic contents,old overview method

#trainner.testClassifier_OverCurrentRawPosts() # Test the reaction of the loaded classifier over the current available crawled raw data