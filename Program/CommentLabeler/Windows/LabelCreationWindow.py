
import typing
from PyQt6.QtWidgets import QLabel,QScrollArea,QGroupBox,QGridLayout,QScrollBar,QHBoxLayout,QWidget,QVBoxLayout,QFrame,QComboBox,QSizePolicy,QPushButton
from PyQt6.QtCore import Qt 
from Program.CommentLabeler .Widgets.LabelSetCreationWidget import LabelSetCreationWidget
from Program.CommentLabeler .Widgets.LabelSetLabelFieldWidget import LabelSetLabelFieldWidget
from Program.CommentLabeler .Widgets.LabelSetShortcutWidget import LabelSetShortcutWidget
from Program.Utils.PathHandler import PathHandler
from Program.Parameters.paths import paths
import json

class LabelCreationWindow(QWidget):

    def __init__(self, parent: typing.Optional['QWidget']) -> None:
        super(LabelCreationWindow,self).__init__(parent)
        self.pathHandler = PathHandler(paths=paths)
        self.labelList = self.nativeParentWidget().labelSet_LabelList
        if not self.labelList:
            self.labelList.append(LabelSetLabelFieldWidget("Name of the set : ",self))

        self.setupUI()


    def _callRedraw(self):
        self.labelList.append(LabelSetLabelFieldWidget("Label : ",self))
        self.nativeParentWidget()._redrawLabelCreationWindow()

    def _dumpLabelSet(self,labelSet):
        name = self.pathHandler.getParametersPath()+"LabelSets/"+labelSet["setName"]+""".json"""
        
        with open(name, 'w') as outfile:
            json.dump(labelSet, outfile)
        

    def _saveAndCallRedraw(self):
        self.pathHandler.getParametersPath()

        finalSet = {"setName":self.labelList[0].lineEdit.text(),"labelList":[]}
        for label in self.labelList[1:]:
            finalSet["labelList"].append(label.lineEdit.text())
               
        self._dumpLabelSet(finalSet)

        
        self.nativeParentWidget().labelSet_LabelList = []
        self.nativeParentWidget()._redrawLabelMenuWindow()

    def setupUI(self):
        
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)
        x = 0 
        for label in self.labelList:
            self.layout.addWidget(label,x,0,1,1)
            x+=1

        self.addNewFieldButton = QPushButton("Add a new field")
        self.addNewFieldButton.clicked.connect(self._callRedraw)
        self.layout.addWidget(self.addNewFieldButton,x+1,0,1,1)

        self.addNewFieldButton = QPushButton("Save this set")
        self.addNewFieldButton.clicked.connect(self._saveAndCallRedraw)
        self.layout.addWidget(self.addNewFieldButton,x+2,0,1,1)


        self.show()
