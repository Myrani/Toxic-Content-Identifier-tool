from PyQt6.QtWidgets import QLabel,QScrollArea,QGroupBox,QGridLayout,QScrollBar,QHBoxLayout,QWidget,QVBoxLayout,QFrame,QComboBox,QSizePolicy
from PyQt6.QtCore import Qt 


class SupplementLabel(QWidget):
    
    def __init__(self, parent) -> None:

        super(SupplementLabel,self).__init__(parent=parent)
        self.widgetLayout = QVBoxLayout(self)

        self.mainLabel = QLabel(self)
        self.comboBox =  QComboBox(self)
        self.mainLabel.setStyleSheet("background-color: grey")

        self.mainLabel.setMinimumSize(100,100)
        self.mainLabel.setMaximumSize(400,400)
        
        self.mainLabel.setWordWrap(True)
        self.mainLabel.setSizePolicy(QSizePolicy.Policy.Preferred,QSizePolicy.Policy.Preferred)
        self.mainLabel.adjustSize()
        
        self.comboBox.addItems(self.nativeParentWidget().currentActiveLabels)
        self.comboBox.setMaximumSize(200,25)



        self.widgetLayout.addWidget(self.mainLabel)
        self.widgetLayout.addWidget(self.comboBox)
        
        
        self.show()


    def setText(self,text):
        self.mainLabel.setText(text)
        self.mainLabel.adjustSize()
    
    def setComboBox(self,choice):
        self.comboBox.setCurrentText(choice)