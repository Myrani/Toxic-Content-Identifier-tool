from Program.RedditExplorer.ExplorerDatahandler import ExplorerDataHandler

class AccountExplorer():

    def __init__(self,reddit) -> None:
        """
            Initialisation of the Account explorer
        
        
        """
        self.reddit = reddit
        self.explorerDataHandler = ExplorerDataHandler()

    def harvestUserMetrics(self,username):


        commentList = self._getAllUserCommentsIds(username)

        
        currentUserCommentMetrics = {"username":username} 


        for comment in commentList:

            if str(comment.subreddit.display_name) not in currentUserCommentMetrics.keys() :
                currentUserCommentMetrics[str(comment.subreddit.display_name)] = [comment.body]
            else:
                currentUserCommentMetrics[str(comment.subreddit.display_name)].append(comment.body)
            
        self.explorerDataHandler._dumpToJSON(currentUserCommentMetrics)



    def getAllUserPosts(self,user):
        """
            Returns all the posts of a passed user    
        
        """

    
    def _getAllUserCommentsIds(self,user):
        """
            Returns all the comments of a passed user    
        
        """

        return [comment for comment in self.reddit.redditor(user).comments.new(limit=None)]