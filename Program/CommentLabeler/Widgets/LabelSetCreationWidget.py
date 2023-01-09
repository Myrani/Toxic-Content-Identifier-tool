from PyQt6.QtWidgets import QScrollArea,QGroupBox,QGridLayout,QScrollBar,QHBoxLayout,QWidget,QVBoxLayout,QFrame,QLabel,QPushButton
from PyQt6.QtCore import Qt,QSize
import typing

class LabelSetCreationWidget(QWidget):
    def __init__(self, parent: typing.Optional['QWidget'] = ...) -> None:
        super().__init__(parent)


        self._setupUI()

    def _setupUI(self):
        
        self.layout = QHBoxLayout(self)
        self.setLayout(self.layout)
        
        self.setGeometry(0,0,400,200)


        self.creationButton = QPushButton("Create New Label set ",self)
        self.creationButton.setMinimumSize(QSize(400,200))
        print(self.parent().parent())
        self.creationButton.clicked.connect(self.parent().parent()._redrawLabelCreationWindow)
        self.layout.addWidget(self.creationButton)

        self.show()