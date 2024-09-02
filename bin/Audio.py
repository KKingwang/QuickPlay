import sounddevice as sd
import soundfile as sf


def query_audio_drivers():
    """
    查询本机全部音频驱动
    :return audio_drivers: 音频驱动列表
    """
    devices = sd.query_devices()
    audio_drivers = [f"{index + 1}. {device['name']}" for index, device in enumerate(devices)]
    audio_driver_list = ['- None -'] + audio_drivers
    return audio_driver_list


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
        print(sd.query_devices())  # 打印选定音频设备信息

    # 读取音效文件
    data, fs = sf.read(file)

    # 调整音量
    data *= volume / 100

    # 播放音效
    sd.play(data, fs)
    # sd.wait()  # 等待播放结束
