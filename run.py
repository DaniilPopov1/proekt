import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
import video
from video import Ui_MainWindow
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore, QtGui
import cv2
import numpy as np

class ThreadOpenCV(QThread):
    changePixmap = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self.video_stream = cv2.VideoCapture('https://s2.moidom-stream.ru/s/public/0000000973.m3u8')

    def run(self):
        while True:
            ret, frame = self.video_stream.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_expanded = np.expand_dims(frame_rgb, axis=0)
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(
                    rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(720, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

            self.msleep(20)
            cv2.destroyAllWindows()

class Window(QMainWindow, video.Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        video.Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.thread = ThreadOpenCV()
        self.thread.start()
        self.thread.changePixmap.connect(self.setImage)

    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())