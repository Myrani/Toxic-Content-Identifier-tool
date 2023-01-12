from Program.NLP.LabelPipeline.PostBagger import PostBagger
from Program.NLP.LabelPipeline.PostRefiner import PostRefiner
from Program.NLP.LabelPipeline.ClassifierGenerator import ClassifierGenerator


postRefiner = PostRefiner()
postBagger = PostBagger()
classifierGenerator = ClassifierGenerator()


postRefiner.refineAllLabelisedPosts()
postBagger.bagAllRefinedPosts()
classifierGenerator.generateClassifierFromAllBags()