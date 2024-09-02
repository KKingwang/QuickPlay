import sys

import sounddevice as sd
import soundfile as sf
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from pynput import keyboard
import bin.Audio
import bin.ConfigOperation
from bin.Shortcut import convert_shortcut

gVolume = 50
gAudioDriverId = None


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口标题
        self.setWindowTitle('我的第一个PyQt6窗口')

        # 设置窗口大小
        self.setGeometry(100, 100, 600, 400)

        # 创建一个标签，并将其设置为主窗口的中央部件
        label = QLabel('你好，PyQt6！', self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(label)


def query_audio_drivers():
    """
    查询本机全部音频驱动
    :return audio_drivers: 音频驱动列表
    """
    devices = sd.query_devices()
    audio_drivers = [f"{index + 1}. {device['name']}" for index, device in enumerate(devices)]
    audio_driver_list = ['- None -'] + audio_drivers
    print(audio_driver_list)
    return audio_driver_list


def audio_driver_selection(audio_driver_name):
    """
    设置音频驱动ID
    :param audio_driver_name:
    :return:
    """
    global gAudioDriverId
    audio_driver_list = bin.Audio.query_audio_drivers()
    for i in range(len(audio_driver_list)):
        if audio_driver_name == audio_driver_list[i]:
            gAudioDriverId = i


def play_sound_effects(file, volume, audio_driver_index):
    """
    播放音效文件
    :param file: 音效文件路径
    :param volume: 音量，范围 0.0 到 1.0
    :param audio_driver_index: 选择的音频驱动的索引
    :return:
    """

    if audio_driver_index is not None:
        # 设置选定的音频设备
        sd.default.device = audio_driver_index - 1
        # print(sd.query_devices())  # 打印选定音频设备信息

    # 读取音效文件
    data, fs = sf.read(file)

    # 调整音量
    data *= volume / 100

    # 播放音效
    sd.play(data, fs)
    # sd.wait()  # 等待播放结束


def audio_driver_selection(audio_driver_name):
    """
    选择音频驱动
    :param audio_driver_name:
    :return:
    """
    global gAudioDriverId
    audio_driver_list = query_audio_drivers()
    for i in range(len(audio_driver_list)):
        if audio_driver_name == audio_driver_list[i]:
            gAudioDriverId = i


def registration_shortcuts():
    """
    注册快捷键
    :param sound: 音效文件名
    :param shortcut: 快捷键
    :return:
    """
    config_data_list = bin.ConfigOperation.load_config()
    for entry in config_data_list:
        with keyboard.GlobalHotKeys({
            entry[1]: lambda: bin.Audio.play_sound_effects("./music/" + entry[0],
                                                           gVolume, gAudioDriverId)
        }) as listener:
            listener.join()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # 假设选择索引为 2 的音频驱动，并播放一个音频文件
    # play_sound_effects('./music/你好.mp3', volume=0.8, audio_driver_name=1)
    print(sd.query_devices())
    query_audio_drivers()

    print(audio_driver_selection('3. MacBook Air扬声器'))
    print(gAudioDriverId)
    registration_shortcuts()

    # 进入应用程序的主事件循环
    # exec() 会阻塞当前线程，直到应用程序退出
    sys.exit(app.exec())
