import os
import sys

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from pynput import keyboard
from PyQt6.QtWidgets import QApplication, QToolBar, QTableWidget, QTableWidgetItem, QDialog, QFileDialog, \
    QPushButton, QLineEdit, QDialogButtonBox, QKeySequenceEdit, QMessageBox, QStatusBar, QLabel, QComboBox, QSlider

import bin.Audio
import bin.ConfigOperation
from bin.EasterEgg import easter_egg
from bin.Shortcut import convert_shortcut, is_windows_or_macos

gSoundVolume = 50  # 音量
gAudioDriverText = None  # 音频驱动
gAudioDriverId = None  # 音频驱动索引


def select_file():
    """
    选择文件
    :return:
    """
    fd = QFileDialog()
    fd.setFileMode(QFileDialog.FileMode.ExistingFile)
    fd.setNameFilter("音频文件(*.mp3 *.wav)")
    fd.setDirectory('./music')
    fd.exec()
    selected_file = fd.selectedFiles()[0]
    selected_file = os.path.basename(selected_file)
    newlyBuildToolBarText.setText(selected_file)


def sun_new_ui_show():
    """
    显示子窗口
    :return:
    """
    sunNewUi.show()  # 显示子窗口
    newlyBuildToolBarText.clear()  # 初始化打开音效文件文本框
    setShortcutKeysText.clear()  # 初始化快捷键文本框


def ok(window):
    """
    确定按钮
    :param window:
    :return:
    """
    a = newlyBuildToolBarText.text()
    b = convert_shortcut(setShortcutKeysText.keySequence().toString())
    c = remarksText.text()
    if a == "" or b == "" or c == "":
        QMessageBox.critical(None, '错误', '选项的值不能为空', QMessageBox.StandardButton.Ok)
    else:
        list = [a, b, c]
        # print(list) # 测试输出
        d = bin.ConfigOperation.write_data_config(list)
        if d:
            QMessageBox.critical(None, '错误', f'{d}重复', QMessageBox.StandardButton.Ok)
        else:
            window.hide()
            load_table()


def no(window):
    """
    取消按钮
    :param window:
    :return:
    """
    window.hide()


def load_table():
    """
    加载表格
    :return:
    """
    tableWidget.clearContents()  # 只清空内容，保留表头
    data = bin.ConfigOperation.read_data_config()  # 读取配置文件
    tableWidget.setRowCount(0)  # 重置行数
    for i, songInfo in enumerate(data):  # 遍历数据并写入表格
        tableWidget.insertRow(i)  # 插入新行
        for j in range(3):
            tableWidget.setItem(i, j, QTableWidgetItem(songInfo[j]))  # 插入数据


def delete_tool_bar():
    """
    删除工具栏
    :return:
    """
    selected_items = tableWidget.selectedItems()  # 获取选中的项目
    list = []
    for item in selected_items:  # 遍历选中的项目
        list.append(item.text())
    if list:  # 判断是否有项目
        if bin.ConfigOperation.delete_data_config(list):
            QMessageBox.critical(None, '错误', '没有项目', QMessageBox.StandardButton.Ok)
        else:
            bin.ConfigOperation.delete_data_config(list)
            statusBar.showMessage(f"已删除{list}，重新加载完毕", 2000)
            load_table()


def refresh_tool_bar():
    """
    刷新工具栏
    :return:
    """
    load_table()
    statusBar.showMessage(easter_egg(), 2000)


def sun_audio_driver_ui_show():
    """
    显示子窗口   音频驱动选择
    :return:
    """
    # 显示子窗口
    sunAudioDriverUi.show()
    # 获取音频驱动
    audio_drivers = bin.Audio.query_audio_drivers()
    outputDriver.addItems(audio_drivers)


def sun_audio_driver_ui_ok():
    """
    音频驱动选择子窗口 确定按钮
    :return:
    """

    audio_driver_text = outputDriver.currentText()
    currentAudioDriver.setText(audio_driver_text)
    audio_driver_selection(audio_driver_text)
    outputDriver.clear()
    sunAudioDriverUi.hide()


def sun_audio_driver_ui_no():
    """
    音频驱动选择子窗口 取消按钮
    :return:
    """
    outputDriver.clear()
    sunAudioDriverUi.hide()


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


def volume_control():
    """
    音量控制
    :return:
    """
    global gSoundVolume
    gSoundVolume = volume_slider.value()
    statusBar.showMessage(f"音量：{gSoundVolume}%", 1000)


def registration_shortcuts():
    """
    注册快捷键
    :return:
    """
    # config_data_list = bin.ConfigOperation.load_config()
    # for entry in config_data_list:
    #     audio_file_path = "./music/" + entry[0]
    #     keyboard.register_hotkey(bin.Shortcutnew.convert_shortcut(entry[1]), None,
    #                              lambda: bin.Audio.play_sound_effects(audio_file_path, gSoundVolume, gAudioDriverId))
    config_data_list = bin.ConfigOperation.load_config()  # 读取配置文件
    hotkeys = {}  # 创建一个字典用于存储所有快捷键和对应的操作
    for entry in config_data_list:  # 遍历配置列表，将每个快捷键和其对应的操作添加到字典中
        hotkeys[entry[1]] = lambda e=entry: bin.Audio.play_sound_effects("./music/" + e[0], gSoundVolume,
                                                                         gAudioDriverId)

    with keyboard.GlobalHotKeys(hotkeys) as listener:  # 在所有快捷键注册完成后，创建一个 GlobalHotKeys 实例
        listener.join()  # 启动全局监听器


def information_about():
    """
    关于信息
    :return:
    """
    # print(gSoundVolume)
    pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 生成配置文件
    bin.ConfigOperation.load_config()
    # print(bin.ConfigOperation.read_data_config()) # 测试读取配置文件
    # 加载主窗口 ui
    ui = uic.loadUi("./UI/QuickPlay.ui")
    # 加载子窗口 newUi
    newUi = uic.loadUi("./UI/NewlyBuild.ui")
    sunNewUi = QDialog(ui)
    newUi.setParent(sunNewUi)
    # 加载子窗口 audioDriverUi
    audioDriverUi = uic.loadUi("./UI/AudioDriver.ui")
    sunAudioDriverUi = QDialog(ui)
    audioDriverUi.setParent(sunAudioDriverUi)

    # 在工具栏创建音量滑块
    volume_slider = QSlider(Qt.Orientation.Horizontal)
    volume_slider.setMinimum(0)
    volume_slider.setMaximum(100)
    volume_slider.setTickInterval(10)
    volume_slider.setPageStep(10)
    volume_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
    volume_slider.setValue(50)  # 设置初始音量为 50%
    volume_slider.setFixedWidth(200)  # 设置滑块的宽度

    # 添加工具栏
    toolBar: QToolBar = ui.toolBar
    toolBar.addSeparator()
    newlyBuildToolBar = toolBar.addAction(QIcon("./Icon/1.png"), "新建")
    toolBar.addSeparator()
    modifyToolBar = toolBar.addAction(QIcon("./Icon/1.png"), "修改")
    toolBar.addSeparator()
    refreshToolBar = toolBar.addAction(QIcon("./Icon/1.png"), "刷新")
    toolBar.addSeparator()
    toolBar.addAction("")  # 添加无效按键用于隔离
    toolBar.addWidget(volume_slider)  # 将滑动条添加到工具栏
    toolBar.addAction("")  # 添加无效按键用于隔离
    toolBar.addSeparator()
    deleteToolBar = toolBar.addAction(QIcon("./Icon/1.png"), "删除")
    toolBar.addSeparator()
    audioDriverToolBar = toolBar.addAction(QIcon("./Icon/1.png"), "音频驱动选择")
    toolBar.addSeparator()
    aboutToolBar = toolBar.addAction(QIcon("./Icon/1.png"), "关于")
    toolBar.addSeparator()

    # 加载状态栏
    statusBar: QStatusBar = ui.statusBar

    # 工具栏功能
    newlyBuildToolBar.triggered.connect(lambda: sun_new_ui_show())  # 显示 “新建” 窗口
    refreshToolBar.triggered.connect(lambda: refresh_tool_bar())  # 刷新表格
    volume_slider.valueChanged.connect(lambda: volume_control())  # 连接音量条的值变化信号到处理函数
    deleteToolBar.triggered.connect(lambda: delete_tool_bar())  # 删除选中的表格
    audioDriverToolBar.triggered.connect(lambda: sun_audio_driver_ui_show())  # 显示 “音频驱动选择” 窗口
    aboutToolBar.triggered.connect(lambda: registration_shortcuts())  # 显示关于信息

    # 初始化sunNewUi子窗口的控件
    openSoundEffectFile: QPushButton = newUi.pushButton  # 打开音效文件按钮
    newlyBuildOkOrOn: QDialogButtonBox = newUi.buttonBox  # 确定或取消按钮
    newlyBuildToolBarText: QLineEdit = newUi.lineEdit  # 打开音效文件文本框
    setShortcutKeysText: QKeySequenceEdit = newUi.keySequenceEdit  # 设置快捷键文本框
    remarksText: QLineEdit = newUi.lineEdit_3  # 备注文本框
    # sunNewUi子窗口内控件功能设置
    openSoundEffectFile.clicked.connect(select_file)  # 打开音效文件
    newlyBuildOkOrOn.accepted.connect(lambda: ok(sunNewUi))  # 确定按钮
    newlyBuildOkOrOn.rejected.connect(lambda: no(sunNewUi))  # 取消按钮
    # 初始化sunAudioDriverUi子窗口的控件
    currentAudioDriver: QLineEdit = audioDriverUi.lineEdit  # 当前音频驱动
    audioDriverOkOrOn: QDialogButtonBox = audioDriverUi.buttonBox  # 确定或取消按钮
    outputDriver: QComboBox = audioDriverUi.comboBox  # 输出驱动下拉框
    # sunAudioDriverUi子窗口内控件功能设置
    audioDriverOkOrOn.accepted.connect(lambda: sun_audio_driver_ui_ok())  # 确定按钮
    audioDriverOkOrOn.rejected.connect(lambda: sun_audio_driver_ui_no())  # 取消按钮

    # 设置表格
    tableWidget: QTableWidget = ui.tableWidget  # 获取表格
    tableWidget.setShowGrid(True)  # 显示网格
    tableWidget.horizontalHeader().setStretchLastSection(True)  # 最后一列拉伸
    tableWidget.horizontalHeader().setDefaultSectionSize(200)  # 设置列的默认宽度
    tableWidget.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)  # 设置只能选中一行
    # tableWidget.horizontalHeader().setFixedHeight(25)  # 设置列表头的高度
    # tableWidget.horizontalHeader().setMinimumSectionSize(100)  # 设置列的最小宽度
    tableWidget.setColumnCount(3)  # 设置列数
    tableWidget.setHorizontalHeaderLabels(["音效", "快捷键", "备注"])

    # 添加数据
    load_table()
    statusBar.showMessage("初始化完毕", 3000)
    if is_windows_or_macos():
        statusBar.addPermanentWidget(QLabel("系统：Windows｜作者：空白 , 🍟薯条"), 0)
    else:
        statusBar.addPermanentWidget(QLabel("系统：macOS｜作者：空白 , 🍟薯条"), 0)

    ui.show()
    sun_audio_driver_ui_show()
    sys.exit(app.exec())
