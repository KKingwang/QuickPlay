import os
import sys

from PyQt6 import uic
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QToolBar, QTableWidget, QTableWidgetItem, QDialog, QFileDialog, \
    QPushButton, QLineEdit, QDialogButtonBox, QKeySequenceEdit, QMessageBox, QStatusBar, QLabel

import bin.ConfigOperation
from bin.EasterEgg import easter_egg


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
    b = setShortcutKeysText.keySequence().toString()
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


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 加载主窗口
    ui = uic.loadUi("./UI/QuickPlay.ui")
    # 生成配置文件
    bin.ConfigOperation.load_config()
    # print(bin.ConfigOperation.read_data_config()) # 测试读取配置文件
    # 加载子窗口
    newUi = uic.loadUi("./UI/NewlyBuild.ui")
    sunNewUi = QDialog(ui)
    newUi.setParent(sunNewUi)

    # 添加工具栏
    toolBar: QToolBar = ui.toolBar
    toolBar.addSeparator()
    newlyBuildToolBar = toolBar.addAction(QIcon("./Icon/1.png"), "新建")
    toolBar.addSeparator()
    modifyToolBar = toolBar.addAction(QIcon("./Icon/1.png"), "修改")
    toolBar.addSeparator()
    refreshToolBar = toolBar.addAction(QIcon("./Icon/1.png"), "刷新")
    toolBar.addSeparator()
    for i in range(6):  # 添加无效按键用于隔离
        toolBar.addAction("")
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
    deleteToolBar.triggered.connect(lambda: delete_tool_bar())  # 删除选中的表格
    # 初始化sunNewUi子窗口的控件
    openSoundEffectFile: QPushButton = newUi.pushButton  # 打开音效文件按钮
    okOrOn: QDialogButtonBox = newUi.buttonBox  # 确定或取消按钮
    newlyBuildToolBarText: QLineEdit = newUi.lineEdit  # 打开音效文件文本框
    setShortcutKeysText: QKeySequenceEdit = newUi.keySequenceEdit  # 设置快捷键文本框
    remarksText: QLineEdit = newUi.lineEdit_3  # 备注文本框
    # 打开音效文件按钮功能
    openSoundEffectFile.clicked.connect(select_file)
    okOrOn.accepted.connect(lambda: ok(sunNewUi))  # 确定按钮
    okOrOn.rejected.connect(lambda: no(sunNewUi))  # 取消按钮

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
    statusBar.addPermanentWidget(QLabel("作者：空白 , 🍟薯条"), 0)

    ui.show()
    sys.exit(app.exec())
