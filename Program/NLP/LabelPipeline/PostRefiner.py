import nltk
import json
import os
from Program.Utils.PathHandler import PathHandler
from Program.Utils.WindowsNamingConventionsHandler import WindowsNamingConventionsHandler

class PostRefiner():
    def __init__(self) -> None:
        """
        
            Transforms LabeledPosts into a RefinedPost Structure        
        
        """

        self.pathHandler = PathHandler()
        self.namingConventionsHandler = WindowsNamingConventionsHandler()

    def loadRawPost(self,name):
        """
            Loads a post from Raw Post
        """
        data = open(self.pathHandler.getRawPostsPath() +name+".json")
        return json.load(data)
    
    def loadLabeledPost(self,name):
        """
            Loads a post from Raw Post
        """
        data = open(self.pathHandler.getLabeledPostsPath()+name)
        return json.load(data)

    
    def _tokenizeComment(self,comment):

        """
            Transforms into a list of token a given string
        
        """
        return nltk.word_tokenize(comment)

    def tokenizeLabelizedPost(self,labeledPost):

        """
            Split into different tokens all comment within the passed LabeledPost then save it as a RefinedPost into 
            the user specified Folder 

            Args : LabeledPost

            return : None

        """
        tokenisedPost = {"title": labeledPost["title"],"content":[]}


        for labeledComment in labeledPost["content"]:

            tokenisedPost["content"].append({"label":labeledComment["label"] ,"comment":self._tokenizeComment(labeledComment["comment"])})
            

        
        self._dumpRefinedPostToJSON(tokenisedPost)

    def _dumpRefinedPostToJSON(self,post):
        """
            Internal function used to create a JSON file from refinedPost and dump it 
        """
        name = self.namingConventionsHandler._cleanName(string=post["title"],directory=self.pathHandler.getRefinedPostsPath())+""".json"""
        
        with open(name, 'w') as outfile:
            json.dump(post, outfile)


    def _getAllLabeledPosts(self):
        """
            Return a list of all available LabeledPosts 

            Args : None

            returns : A List of filename 
        
        """

        return os.listdir(self.pathHandler.getLabeledPostsPath())



    def refineAllLabelisedPosts(self):
        """
            Function to create a RefinedPost version of all Labelised Posts available
        
            Args : None 

            Returns : None
        """
        
        for post in self._getAllLabeledPosts():
            self.tokenizeLabelizedPost(self.loadLabeledPost(post))


    








            