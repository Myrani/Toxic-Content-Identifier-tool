class Strategy():
    """ 
        Parent class for any fetch strategy 
        provides all the basic methods for a working implementation 
    
    """
    def __init__(self) -> None:
        
        self.currentBuffer = [] # where posts are stocked 
        
    def getNextPost(self):
        """ 
        Function to call to get the next post
    
        """
        pass
    
    def _refillBuffer(self):
        """
        function to call when the post buffer is depleted and needs new posts
        """
        
        pass
    