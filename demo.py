from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtWidgets import QFileDialog, QPushButton, QMainWindow, QApplication
import os


class SignalEmitter(QObject):
    file_selected = pyqtSignal(str)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建信号发射器
        self.signal_emitter = SignalEmitter()

        # 连接信号和槽函数
        self.signal_emitter.file_selected.connect(self.handle_file_selected)

        # 创建一个按钮并连接槽函数
        self.openSoundEffectFile = QPushButton("Open Sound Effect File", self)
        self.openSoundEffectFile.clicked.connect(self.select_file)

    def select_file(self):
        fd = QFileDialog()
        fd.setFileMode(QFileDialog.FileMode.ExistingFile)
        fd.setNameFilter("音频文件 (*.mp3 *.wav)")
        fd.setDirectory('./music')

        if fd.exec():
            selected_file = fd.selectedFiles()[0]
            file_name = os.path.basename(selected_file)
            self.signal_emitter.file_selected.emit(file_name)  # 发射信号，传递文件名

    def handle_file_selected(self, file_name):
        print(f"Selected file: {file_name}")  # 在这里处理文件名


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
