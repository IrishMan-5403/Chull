from PyQt5.QtWidgets import QApplication, QMainWindow
from CHullViewer import ConvexHullViewer
import sys

class MainWindow(QMainWindow):
    def __init__(self, faces, points,edges):
        super().__init__()

        # Set up the window
        self.setWindowTitle("3D Convex Hull Visualization")
        self.setGeometry(100, 100, 800, 600)

        # Add the OpenGL widget to the window
        self.viewer = ConvexHullViewer(faces, points,edges)
        self.setCentralWidget(self.viewer)

def viewer(faces,points,edges):
    app = QApplication(sys.argv)
    window = MainWindow(faces, points,edges)
    window.show()
    sys.exit(app.exec_())
