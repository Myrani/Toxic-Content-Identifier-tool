import typing


import typing
from PyQt6.QtWidgets import QLabel,QScrollArea,QGroupBox,QGridLayout,QScrollBar,QHBoxLayout,QWidget,QVBoxLayout,QFrame,QComboBox,QSizePolicy,QPushButton
from PyQt6.QtCore import Qt
from Program.Utils.PathHandler import PathHandler
from Program.CommentLabeler.Widgets.ButtonPostHistoryWidget import ButtonPostHistoryWidget 
from Program.CommentLabeler.Widgets.LabelSetCreationWidget import LabelSetCreationWidget
from Program.CommentLabeler.Widgets.LabelSetShortcutWidget import LabelSetShortcutWidget
import os
import json 
from Program.Parameters.paths import paths

class PostHistoryWindow(QWidget):

    def __init__(self, parent: typing.Optional['QWidget'] = ...) -> None:
        super().__init__(parent)

        self._initUI()

    def _initUI(self):
        
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        for post in self.nativeParentWidget().postHistory:
            self.layout.addWidget(ButtonPostHistoryWidget(post,self))

        self.show()

