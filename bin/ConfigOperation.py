import os

config_file_path = 'data.config'


def load_config():
    """
    加载配置文件，如果不存在则创建一个空文件。
    """
    if not os.path.exists(config_file_path):
        with open(config_file_path, 'w') as f:
            f.write("")  # 创建空文件
        return []

    with open(config_file_path, 'r') as f:
        lines = f.readlines()
        config_data = [eval(line.strip()) for line in lines]
    return config_data


def read_data_config():
    """
    读取配置文件并返回一个包含所有数据的二维列表。
    """
    song_infos = []
    with open(config_file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            # 将每一行的字符串转换为列表
            song_info = eval(line.strip())
            song_infos.append(song_info)
    return song_infos


def check_duplicates(config_data, new_entry):
    """
    检查新条目的前两个元素是否在配置数据中重复。
    如果第一个元素重复，返回 "音效文件"；
    如果第二个元素重复，返回 "快捷键"；
    如果没有重复，返回 None。
    """
    for entry in config_data:
        if new_entry[0] == entry[0]:
            return "音效文件"  # 第一个元素重复
        if new_entry[1] == entry[1]:
            return "快捷键"  # 第二个元素重复
    return None  # 没有重复


def save_to_config(file_path, data):
    """
    将数据写入配置文件。
    """
    with open(file_path, 'a') as f:
        f.write(str(data) + "\n")


def write_data_config(new_entry):
    """
    将新条目写入配置文件。
    """
    # 加载现有的配置数据
    config_data = load_config()

    # 检查是否有重复项
    duplicate = check_duplicates(config_data, new_entry)
    if duplicate:
        print(f"重复的项目: {duplicate}")  # 测试输出重复的项目
        return duplicate
    else:
        save_to_config(config_file_path, new_entry)
        print("数据已写入配置文件。")
    print("配置文件已更新")


def delete_data_config(delete_entry):
    """
    从配置文件中删除指定的条目。
    :param delete_entry: 需要删除的条目，格式为 ['2.mp3', 'Q', '无']
    """
    # 加载现有的配置数据
    config_data = load_config()
    for entry in config_data:
        if delete_entry[0] == entry[0] and delete_entry[1] == entry[1]:
            # 读取配置文件中的所有数据
            with open(config_file_path, 'r') as file:
                lines = file.readlines()
            # 过滤掉要删除的条目
            new_lines = [line for line in lines if eval(line.strip()) != delete_entry]
            # 将新的数据写回文件
            with open(config_file_path, 'w') as file:
                file.writelines(new_lines)
    return None  # 没有项目
