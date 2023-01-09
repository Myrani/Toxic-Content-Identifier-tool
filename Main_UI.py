from PyQt6.QtWidgets import QApplication, QWidget
from Program.CommentLabeler.Windows.MainWindow import MainWindow
# Only needed for access to command line arguments
import sys
# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([])
#works too.
app = QApplication(sys.argv)
# Create a Qt widget, which will be our window.
MainWindow = MainWindow()
# IMPORTANT!!!!! Windows are hidden by default.
# Start the event loop.
sys.exit(app.exec())
