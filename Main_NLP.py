from Program.NLP.PostBagger import PostBagger
from Program.NLP.PostRefiner import PostRefiner
from Program.NLP.ClassifierGenerator import ClassifierGenerator


postRefiner = PostRefiner()
postBagger = PostBagger()
classifierGenerator = ClassifierGenerator()


postRefiner.refineAllLabelisedPosts()
postBagger.bagAllRefinedPosts()
classifierGenerator.generateClassifierFromAllBags()