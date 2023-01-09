from PyQt6.QtWidgets import QScrollArea,QGroupBox,QGridLayout,QScrollBar,QHBoxLayout,QWidget,QVBoxLayout,QFrame,QLabel,QPushButton
from PyQt6.QtCore import Qt,QSize
import typing

class LabelSetShortcutWidget(QWidget):
    def __init__(self, labelsetName,labelsetLabelList ,parent: typing.Optional['QWidget'] = ...) -> None:
        super(LabelSetShortcutWidget,self).__init__(parent)
        self.labelsetName = labelsetName
        self.labelsetList = labelsetLabelList
        self._setupUI()
    
    def _changeCurrentActiveLabelSet(self):
        self.nativeParentWidget().currentActiveLabels = self.labelsetList
    
    def _setupUI(self):
        
        self.layout = QHBoxLayout(self)
        self.setLayout(self.layout)
        
        self.setGeometry(0,0,400,200)

        self.descriptionLabel = QLabel(self.labelsetName,self)
        self.descriptionLabel.setMinimumSize(QSize(200,50))
        self.layout.addWidget(self.descriptionLabel)

        self.quickBindSelect = QPushButton("Select")
        self.quickBindSelect.clicked.connect(self._changeCurrentActiveLabelSet)
        self.layout.addWidget(self.quickBindSelect)

        self.quickBindModify = QPushButton("Modify")
        self.layout.addWidget(self.quickBindModify)

        self.quickBindDelete = QPushButton("Delete label set")
        self.layout.addWidget(self.quickBindDelete)


        self.show()