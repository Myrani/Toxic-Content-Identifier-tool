from Program.Parameters.paths import paths
from Program.Utils.PathHandler import PathHandler
from Program.Utils.WindowsNamingConventionsHandler import WindowsNamingConventionsHandler
import json
import os 

class PostBagger():
    def __init__(self) -> None:
        """ 

            Transforms into a BagOfWord a RefinedPost Structure
        
        """

        self.pathHandler = PathHandler()
        self.namingConventionsHandler = WindowsNamingConventionsHandler()

    def _dumpBagOfWordsToJSON(self,bag):
        """
            Internal function used to save a bag of words by creating a JSON file from the the passed bag 
            into the specified Folder 

            Args: Json

            returns: None
        
        
        """
        name = self.namingConventionsHandler._cleanName(string=bag["title"],directory=self.pathHandler.getBagOfWordsPath())+""".json"""
        
        print(name)

        with open(name, 'w') as outfile:
            json.dump(bag, outfile)

    def _getAllRefinedPosts(self):
        """
            Return all the RefinedPosts available in the RefinedPosts Folder

            Args: None

            returns : [A list of Filename] 
        """
        return os.listdir(self.pathHandler.getRefinedPostsPath())

    def _loadRefinedPost(self,name):
        """
            Loads a post from the RefinedPosts folder
        
            Args: name : String 
        
            return : Json file 
        """
        data = open(self.pathHandler.getRefinedPostsPath()+name)
        return json.load(data)


    def bagAllRefinedPosts(self):
        """
            Iterate over all refined posts in the specified refinedpost Folder and generate for each one a corresponding bag of words stocked in
            the BagOfWords Folder specified

            Args : None

            Returns : None 
        
        """
        for post in self._getAllRefinedPosts():
            print(post)
            bag = self.bagRefinedPost(self._loadRefinedPost(post))
            self._dumpBagOfWordsToJSON(bag)
  
    
    def _extractCommentContent(self,comment):
        """
            Creates a bag from the content of a refined comment

            Args : A refined comment Json

            Returns : a bag of words json
        """

        minibag = {}

        for word in comment:
            if word in minibag:
                minibag[word] = minibag[word]+ 1
            else:
                minibag[word] = 1

        return minibag

    def bagRefinedPost(self,refinedPost):

        """
            Parcours a refinedPosts comment list and create a bag of word containning the differents Label and bag of words associated to them 

            Arg : redinedPost : A refined Post Json

            return : A bag of Word Json 
        """
        bag = {"title": refinedPost["title"]}

        for labeledComment in refinedPost["content"]:
            
            for key,value in self._extractCommentContent(labeledComment["comment"]).items():

                if labeledComment["label"] in bag:
                    
                    if key in bag[labeledComment["label"]]:
                         bag[labeledComment["label"]][key] = bag[labeledComment["label"]][key] + value
                    else:
                        bag[labeledComment["label"]][key] = value        
                else:
                    
                    bag[labeledComment["label"]] = {key:value}
        
     
        return bag