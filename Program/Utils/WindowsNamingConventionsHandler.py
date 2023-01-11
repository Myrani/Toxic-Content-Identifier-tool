class WindowsNamingConventionsHandler():

    def __init__(self) -> None:
        pass

    def _cleanName(self,directory,string):
        """
            Clean the post name to fit the OS file name formatting 
        """

        string = directory+string.replace(":","colon").replace("?","questionmark").replace("\"","DoubleQuote").replace("/","SlashForward").replace("\\","SlashBackward").replace("<","inferior").replace(">","greater").replace("*","asterisk").replace("|","BarSymbol").replace(".","Dot").replace("'"," ")
        if len(string) > 253:
            string = string[0:220]
            return string
        
        return string 