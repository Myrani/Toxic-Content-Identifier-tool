from Program.NLP.LabelPipeline.PostBagger import PostBagger
from Program.NLP.LabelPipeline.PostRefiner import PostRefiner
from Program.NLP.LabelPipeline.ClassifierGenerator import ClassifierGenerator


postRefiner = PostRefiner()
postBagger = PostBagger()
classifierGenerator = ClassifierGenerator()


postRefiner.refineAllLabelisedPosts() # In charge of transforming a labeled post or comment into a sequence of tokens (refined post)
postBagger.bagAllRefinedPosts() # In Charge of transforming a refined post into a bag of words structure 
#classifierGenerator.generateClassifierFromAllBags() # In charge of generating a classifier with all the bag of words available
classifierGenerator.generateClassifierFromAllBags_WithToxicityUpScaleFactor() 