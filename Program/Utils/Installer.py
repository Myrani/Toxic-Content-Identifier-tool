import os
from Program.Utils.PathHandler import PathHandler
class Installer():

    def __init__(self) -> None:
        self.patHandler = PathHandler()

    def createAllFolders(self):
        if not os.path.isdir("Results"):
            os.mkdir("Results")

        for path in self.patHandler.path.values():
            if not os.path.isdir(path):
                os.mkdir(path)

