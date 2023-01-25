import random
from Program.Utils.PathHandler import PathHandler
from Program.Parameters.paths import paths
from Program.RedditExplorer.AccountExplorer import AccountExplorer
import json
import os 
import nltk

class ToxicityAnalyser():

    def __init__(self,reddit) -> None:
        
        """
            Bridge class over the NLP side and Reddit API .
            Once a classifier is loaded, this class serves as a comment analyser
            of a given profile .
        
        """


        # Basic info setup 
        self.pathHandler = PathHandler()
        self.accountExplorer = AccountExplorer(reddit=reddit)
        self.reddit = reddit
        # PlaceHolder 
        self.classifier = None
        self.loadedFile = None
        self.priors = {}
        self.uniqueWordsSet = {}
        self.lexiconSize = 0



    def loadSpecifiedClassifier(self,name):
        """
            Loads a classifier with the given name
            
        """
        
        data = open(self.pathHandler.getClassifiersPath()+name)
        
        self.loadedFile =  json.load(data)

        self._setUpClassifier()


    
    def _judgeUseretrics(self,username):
        """
            Harvest all public specific user data 
        
        """
        ### self.accountExplorer.harvestUserMetrics(username)
        ###self.accountExplorer.explorerDataHandler._dumpBaggedProfileToJSON(self._convertRawUserMetricsToBagOfWords(username))
        self.naiveBayes_overProfile(self.accountExplorer.explorerDataHandler._loadUserBaggedMetrics(username))        


    def _setUpClassifier(self):

        """
            Loads all the specs of a classifier : name, priors, uniquewords, lexiconsize, Classifier 
        
        """

    
        self.classifier = self.loadedFile["classifier"]
        self.priors = self.loadedFile["priors"]
        print(self.priors)
        self.uniqueWordsSet = set(self.loadedFile["uniqueWords"])
        self.lexiconSize = self.loadedFile["lexiconSize"]


    def _tokenizeComment(self,comment):

        """
            Transforms into a list of token a given string
        
        """
        return nltk.word_tokenize(comment)

    def _fetchReplies(self, comment):
        """
            Internal function used to fetch comments in a Depth First manners .
        """
        try:
            commentDict = {"commentId": comment.id, "author": comment.author.name,
                           "body": self._tokenizeComment(comment.body), "score": comment.score, "replies": []}

            if comment.replies:
                for reply in comment.replies:
                    commentDict["replies"].append(self._fetchReplies(reply))

            return commentDict
        except Exception as e:
            pass

    def convertSubmissionToJSON(self, submission):
        """
            Convert a reddit submission comments into a JSON object

        """

        post = {"title": submission.title, "author": submission.author.name, "score": submission.score,
                "id": submission.id, "url": submission.url, "content": self._tokenizeComment(submission.selftext), "comments": []}
        submission.comments.replace_more(limit=0)
        comment_queue = submission.comments[:]  # Seed with top-level

        while comment_queue:
            comment = comment_queue.pop(0)
            post["comments"].append(self._fetchReplies(comment))

        return post



    def _convertRawUserMetricsToBagOfWords(self,username):
        """
            Convert an harvester user profile content to a bag of word structure
        
        """

        bag = {"username": username,"bag":{}}

        usermetrics = self.accountExplorer.getRawUserMetrics(username)

        for key,value in usermetrics["comments"].items():
            for comment in value:
                for word in self._tokenizeComment(comment["content"]):

                    if word in bag["bag"]:
                        bag["bag"][word] = bag["bag"][word] + 1
                    else:
                        bag["bag"][word] = 1        
        
        for key,value in usermetrics["posts"].items():
            for comment in value:
                for word in self._tokenizeComment(comment["content"]):

                    if word in bag["bag"]:
                        bag["bag"][word] = bag["bag"][word] + 1
                    else:
                        bag["bag"][word] = 1             
 
        
        
        return bag
    
    ### Different version of naive bayes depending of the passed format 


    def naiveBayes_overProfile(self,baggedUserProfile):
        """
            Operates a naive bayes over a bag of words passed in argument with the loaded classifier

        """    

        results = dict.fromkeys(self.priors,1.0)

        for word,count in baggedUserProfile["bag"].items(): 
            for prior in results.keys():
                if word in self.classifier[prior]:
                    results[prior] = results[prior] * self.priors[prior] * ( (self.classifier[prior][word] + 1) / (self.lexiconSize + len(self.uniqueWordsSet.union(set(baggedUserProfile["bag"].values())))))
                else:
                     results[prior] = results[prior] * self.priors[prior] * ( 1 / (self.lexiconSize + len(self.uniqueWordsSet.union(set(baggedUserProfile["bag"].values())))))
                
                if results[prior] == 0:
                    return results
        
        return results


    def naiveBayes_overPost_Bagged(self,baggedUserPost):
        """
            Operates a naive bayes over a bag of words passed in argument with the loaded classifier

        """    

        results = dict.fromkeys(self.priors,1.0)

        for word,count in baggedUserPost.items(): 
            
            for prior in results.keys():
                if word in self.classifier[prior]:
                    results[prior] = results[prior] * self.priors[prior] * ( (count + 1) / (self.lexiconSize + len(self.uniqueWordsSet.union(set(baggedUserPost.keys())))))
                else:
                     results[prior] = results[prior] * self.priors[prior] * ( 1 / (self.lexiconSize + len(self.uniqueWordsSet.union(set(baggedUserPost.keys())))))
                
                if results[prior] == 0:
                    return results
        
        return results

    def naiveBayes_overPost(self,baggedUserPost):
        """
            Operates a naive bayes over a bag of words passed in argument with the loaded classifier
        """    

        results = dict.fromkeys(self.priors,1.0)

        for word,count in baggedUserPost.items(): 
            
            for prior in results.keys():
                if word in self.classifier[prior]:
                    results[prior] = results[prior] * self.priors[prior] * ( (count + 1) / (self.lexiconSize + len(self.uniqueWordsSet.union(set(baggedUserPost.keys())))))
                else:
                     results[prior] = results[prior] * self.priors[prior] * ( 1 / (self.lexiconSize + len(self.uniqueWordsSet.union(set(baggedUserPost.keys())))))
                
                if results[prior] == 0:
                    return results
        
        return results

    def naiveBayes_overComment(self,baggedContent):
        """
            Operates a naive bayes over a bag of words passed in argument with the loaded classifier

        """    

        results = dict.fromkeys(self.priors,1.0)

        for key in results:
            results[key] = self.priors[key]

        for word in baggedContent: 
            
            for prior in results.keys():
                if word in self.classifier[prior]:
                    results[prior] = results[prior] * ( (self.classifier[prior][word] + 1) / (len(self.uniqueWordsSet.union(set(baggedContent)))))
                else:
                     results[prior] = results[prior] * ( 1 / (len(self.uniqueWordsSet.union(set(baggedContent)))))
                
                if results[prior] == 0:
                    return results
        
        return results


    def _toxicityFlagging(self,comment):
        print("Toxicity identified",comment)

    def _judgeNextDeepness(self,commentStructure):
        if commentStructure:
            results = self.naiveBayes_overComment(commentStructure["body"])
            if results["Toxic"] > results["Not Toxic"]:
                self._toxicityFlagging((commentStructure["author"],commentStructure["body"]))

            if commentStructure["replies"]:
                for comment in commentStructure["replies"]:
                    self._judgeNextDeepness(comment)


    def judgeToxicContent_OverCurrentSubreddit_withLimit(self,subbredditName,limit=100):
        
        subreddit = self.reddit.subreddit(subbredditName)

        for submission in subreddit.new(limit=limit):
            
            post = self.convertSubmissionToJSON(submission)
            
            self.naiveBayes_overComment(post["content"])

            if post["comments"]:
                for comment in post["comments"]:
                    self._judgeNextDeepness(comment)

    def judgeToxicContent_SubscribeToSubredditSubmissions(self,subbredditName):
        """
        
            Function subscribing the analyser to a submission stream of a subreddit, and judge each new posts
            TO DO 
        
        """   
        subreddit = self.reddit.subreddit(subbredditName)
        submission_stream = subreddit.stream.submissions(pause_after=-1)


    def judgeToxicContent_SubscribeToSubredditComments(self,subbredditName):
        """
        
            Function subscribing the analyser to a comment stream of a subreddit, and judge each new comments
        
        """
        subreddit = self.reddit.subreddit(subbredditName)
        comment_stream = subreddit.stream.comments(pause_after=-1)

        for comment in comment_stream:
            if comment:
                results = self.naiveBayes_overComment(self._tokenizeComment(comment.body))
                if results["Toxic"] > results["Not Toxic"]:
                    self._toxicityFlagging((comment.author,comment.body))