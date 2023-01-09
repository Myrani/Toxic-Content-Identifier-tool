from PyQt6.QtWidgets import QScrollArea,QGroupBox,QGridLayout,QScrollBar,QHBoxLayout,QWidget,QVBoxLayout,QFrame,QLabel,QPushButton
from PyQt6.QtCore import Qt,QSize
import typing

class ButtonPostHistoryWidget(QWidget):
    """
        Shown in the post history
        Loads its post back into the labeling UI If clicked 
    
    """


    def __init__(self,post, parent: typing.Optional['QWidget'] = ...) -> None:
        super().__init__(parent)
        self.post = post
        self._setupUI()

    def _setupUI(self):
        
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        
        self.setGeometry(0,0,400,200)


        self.creationButton = QPushButton(self.post["title"],self)
        self.creationButton.setMinimumSize(QSize(400,200))
        print(self.parent().parent())
        self.creationButton.clicked.connect(lambda : self.parent().parent()._redrawLabelingWindowWithSpecifiedPost(self.post))
        self.layout.addWidget(self.creationButton)

        self.show()