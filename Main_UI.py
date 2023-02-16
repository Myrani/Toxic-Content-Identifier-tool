from PyQt6.QtWidgets import QApplication, QWidget
from Program.CommentLabeler.Windows.MainWindow import MainWindow
import sys


# Main entry Point of our UI

app = QApplication(sys.argv)

MainWindow = MainWindow()

sys.exit(app.exec())

