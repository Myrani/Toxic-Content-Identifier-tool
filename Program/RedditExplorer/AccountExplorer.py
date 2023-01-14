from Program.RedditExplorer.ExplorerDatahandler import ExplorerDataHandler

class AccountExplorer():

    def __init__(self,reddit) -> None:
        """
            Initialisation of the Account explorer
        
        
        """
        self.reddit = reddit
        self.explorerDataHandler = ExplorerDataHandler()

    def harvestUserMetrics(self,username):

        currentUserMetrics = {"username":username,"comments":{},"posts":{}} 
        
        commentList = self._getAllUserCommentsIds(username)


        for comment in commentList:

            if str(comment.subreddit.display_name) not in  currentUserMetrics["comments"] :
                currentUserMetrics["comments"][str(comment.subreddit.display_name)] = [{"timestamp":comment.created_utc,"content":comment.body}]
            
            else:
                currentUserMetrics["comments"][str(comment.subreddit.display_name)].append({"timestamp":comment.created_utc,"content":comment.body})
            

        postList = self.getAllUserPosts(username)

        for post in postList:

            if str(comment.subreddit.display_name) not in currentUserMetrics["posts"]:

                currentUserMetrics["posts"][str(post.subreddit.display_name)] = [{"timestamp":post.created_utc,"content":post.title}]

            else:
                currentUserMetrics["posts"][str(post.subreddit.display_name)].append({"timestamp":post.created_utc,"content":post.title})


        self.explorerDataHandler._dumpToJSON(currentUserMetrics)

    def getUserMetrics(self,username):
        return self.explorerDataHandler._loadUserMetrics(username)


    def getAllUserPosts(self,user):
        """
            Returns all the posts of a passed user    
        
        """
        return [comment for comment in self.reddit.redditor(user).submissions.new(limit=None)]
    
    def _getAllUserCommentsIds(self,user):
        """
            Returns all the comments of a passed user    
        
        """

        return [comment for comment in self.reddit.redditor(user).comments.new(limit=None)]
