import platform


def is_windows_or_macos():
    """
    判断当前操作系统是否是 Windows 或 macOS
    :return:
    """
    system = platform.system()
    if system == "Windows":  # Windows 的平台名称是 "Windows"
        return True
    elif system == "Darwin":  # macOS 的平台名称是 "Darwin"
        return False
    else:
        raise ValueError("不支持的操作系统!")


# print(is_windows_or_macos())  # 如果是 Windows 则输出 True，macOS 则输出 False


def convert_shortcut(shortcut):
    """
    判断操作系统 并将快捷键字符串转换为目标格式
    :param shortcut:
    :return:
    """
    if is_windows_or_macos():
        return win_convert_shortcut(shortcut)
    else:
        return mac_convert_shortcut(shortcut)


def mac_convert_shortcut(shortcut):
    # 定义映射规则，将常见的修饰键转换为目标格式
    conversion_map = {
        "Meta": "<Ctrl>",
        "Alt": "<Alt>",
        "Shift": "<Shift>",
        "Ctrl": "<Cmd>",
        "Enter": "<Enter>",
        "Esc": "<Esc>",
        "F1": "<F1>",
        "F10": "<F10>",
        "F11": "<F11>",
        "F12": "<F12>",
        "F13": "<F13>",
        "F14": "<F14>",
        "F15": "<F15>",
        "F16": "<F16>",
        "F17": "<F17>",
        "F18": "<F18>",
        "F19": "<F19>",
        "F2": "<F2>",
        "F20": "<F20>",
        "F3": "<F3>",
        "F4": "<F4>",
        "F5": "<F5>",
        "F6": "<F6>",
        "F7": "<F7>",
        "F8": "<F8>",
        "F9": "<F9>",
        "Return": "<Enter>",
        "Backspace": "<Backspace>",
        "CapsLock": "<Caps_lock>",
        "Space": "<Space>",
    }

    # 分割原始快捷键字符串
    keys = shortcut.split('+')

    # 使用映射规则转换每个键
    converted_keys = [conversion_map.get(key, key) for key in keys]

    # 将转换后的键重新组合为字符串
    return '+'.join(converted_keys)


def win_convert_shortcut(shortcut):
    # 定义映射规则，将常见的修饰键转换为目标格式
    conversion_map = {
        "Alt": "<Alt>",
        "Alt_r": "<Alt_r>",
        "Backspace": "<Backspace>",
        "Caps_lock": "<Caps_lock>",
        "Cmd": "<Cmd>",
        "Cmd_r": "<Cmd_r>",
        "Ctrl": "<Ctrl>",
        "Ctrl_r": "<Ctrl_r>",
        "Delete": "<Delete>",
        "Down": "<Down>",
        "End": "<End>",
        "Enter": "<Enter>",
        "Esc": "<Esc>",
        "F1": "<F1>",
        "F10": "<F10>",
        "F11": "<F11>",
        "F12": "<F12>",
        "F13": "<F13>",
        "F14": "<F14>",
        "F15": "<F15>",
        "F16": "<F16>",
        "F17": "<F17>",
        "F18": "<F18>",
        "F19": "<F19>",
        "F2": "<F2>",
        "F20": "<F20>",
        "F3": "<F3>",
        "F4": "<F4>",
        "F5": "<F5>",
        "F6": "<F6>",
        "F7": "<F7>",
        "F8": "<F8>",
        "F9": "<F9>",
        "Home": "<Home>",
        "Left": "<Left>",
        "Media_next": "<Media_next>",
        "Media_play_pause": "<Media_play_pause>",
        "Media_previous": "<Media_previous>",
        "Media_volume_down": "<Media_volume_down>",
        "Media_volume_mute": "<Media_volume_mute>",
        "Media_volume_up": "<Media_volume_up>",
        "Page_down": "<Page_down>",
        "Page_up": "<Page_up>",
        "Right": "<Right>",
        "Shift": "<Shift>",
        "Shift_r": "<Shift_r>",
        "Space": "<Space>",
        "Tab": "<Tab>",
        "Up": "<Up>"
    }

    # 分割原始快捷键字符串
    keys = shortcut.split('+')

    # 使用映射规则转换每个键
    converted_keys = [conversion_map.get(key, key) for key in keys]

    # 将转换后的键重新组合为字符串
    return '+'.join(converted_keys)


if __name__ == '__main__':
    a = mac_convert_shortcut('a')
    print(a)
