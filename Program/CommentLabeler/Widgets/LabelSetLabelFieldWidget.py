from PyQt6.QtWidgets import QScrollArea,QGroupBox,QGridLayout,QScrollBar,QHBoxLayout,QWidget,QVBoxLayout,QFrame,QLabel,QPushButton,QLineEdit
from PyQt6.QtCore import Qt,QSize
import typing

class LabelSetLabelFieldWidget(QWidget):
    def __init__(self ,descriptionText,parent: typing.Optional['QWidget'] = ...) -> None:
        super(LabelSetLabelFieldWidget,self).__init__(parent)
        self.descriptionText = descriptionText
        self._setupUI()


    def _setupUI(self):
        
        self.layout = QHBoxLayout(self)
        self.setLayout(self.layout)
        
        self.setGeometry(0,0,400,200)

        self.descriptionLabel = QLabel(self.descriptionText,self)
        self.descriptionLabel.setMinimumSize(QSize(100,50))
        self.layout.addWidget(self.descriptionLabel)

        self.lineEdit = QLineEdit("",self)
        self.lineEdit.setMinimumSize(QSize(100,50))
        self.layout.addWidget(self.lineEdit)



        self.show()