from Program.Parameters.paths import paths
from Program.Utils.PathHandler import PathHandler
from Program.Utils.WindowsNamingConventionsHandler import WindowsNamingConventionsHandler
import json
import os 

class UserMetricsBagger():
    def __init__(self) -> None:
        """ 

            Depricated / not used in our project

            Aimed to harvest all of a user activity and stock it in one file 
        
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
        

        with open(name, 'w') as outfile:
            json.dump(bag, outfile)


    
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