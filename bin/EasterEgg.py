import threading

# 全局变量 n 和定时器
n = 0
timer = None


def reset_n():
    global n
    n = 0


def easter_egg():
    global n, timer

    # 每次调用时增加 n
    n += 1
    # print(f"n 的当前值: {n}")

    # 如果有定时器正在运行，取消它
    if timer is not None:
        timer.cancel()

    # 重新启动定时器，3 秒后重置 n
    timer = threading.Timer(2.0, reset_n)
    timer.start()
    if n > 100:
        return f"哎呀，不要这样嘛～你已经刷新了{n}次了，再这样的话……人家会坏掉的啦～"
    else:
        return f"你已经刷新了{n}次了。"
