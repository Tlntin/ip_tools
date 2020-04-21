import requests
import re
import socket
import platform
import PySimpleGUI as sg
import pyperclip
import time
import os
import json
import threading


class MyThread(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        pass

    @staticmethod
    def get_public_ip():
        """
        此函数用于获取当前设备下的公网ip
        :return:公网ip地址
        """
        public_ip1 = None
        for ii in range(4):
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
                                    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'
                }
                response = requests.get('http://myip.kkcha.com/', headers=headers, timeout=5)
                html = response.text
                p = re.compile('var sRemoteAddr = \'(.*?)\'')
                result = p.search(html)
                public_ip1 = result.group(1)
            except Exception as err:
                print(err)
        return public_ip1

    @staticmethod
    def get_public_ip2():
        """
        此函数用于获取当前公网下的ip,换了个接口
        :param
        """
        public_ip1 = '0.0.0.0'
        for i in range(4):
            try:
                url = 'https://www.ip.cn/'
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
                    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'
                }
                response = requests.get(url, headers=headers, timeout=5)
                html = response.text
                p = re.compile('<code>(.*?)</code>')
                result = p.search(html)
                public_ip1 = result.group(1)
            except Exception as err2:
                print(err2)
        return public_ip1


def get_private_ip():
    """
    此函数用于获取局域网Ip
    :return:
    """
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('www.baidu.com', 0))
        ip = s.getsockname()[0]
    except Exception as err:
        print(err)
        ip = "x.x.x.x"
    finally:
        s.close()
    return ip


def get_sys_info():
    """
    此函数用于返回当前设备系统信息，并且返回相应的局域网ip
    :return:sys_str，系统信息，ip_address,局域网ip地址
    """
    ip_address = "0.0.0.0"
    sys_str = platform.system()
    if sys_str == "Windows":
        ip_address = socket.gethostbyname(socket.gethostname())
    elif sys_str == "Linux":
        ip_address = get_private_ip()
    elif sys_str == "Darwin":
        ip_address = socket.gethostbyname(socket.gethostname())
    else:
        print("Other System @ some ip")
    return sys_str, ip_address


def load_data(path1='./data/data.json'):
    """
    用于加载公网ip列表
    :param path1: 保存路径
    :return:
    """
    dir_name = os.path.dirname(path1)
    if not os.path.exists(dir_name):  # 如果文件夹不存在
        os.mkdir(dir_name)  # 创建文件夹
    if not os.path.exists(path1):  # 如果文件路径不存在
        with open(path1, 'wt', encoding='utf-8') as f:
            list1 = []
            json.dump(obj=list1, fp=f)
            return []
    else:
        with open(path1, 'rt', encoding='utf-8') as f:
            list1 = json.load(f)
            f.close()
            return list1


def save_data(list1, path1='./data/data.json'):
    """
    此函数用于储存数据到json中
    :param list1: Ip数据
    :param path1: json路径
    :return:
    """
    with open(path1, 'wt+', encoding='utf-8') as f:
        json.dump(list1, f)
        f.close()


def start_check(style1='线路1'):
    """
    :param style1:选择抓取公网Ip的线路
    """
    a = time.time()
    layout0 = [[sg.Text('正在获取你的ip')],
              [sg.ProgressBar(100, orientation='h', key='progressbar', size=(40, 20)),
               sg.Text('', size=(2, 0), key='pct'),
               sg.Text('%')],
              [sg.Cancel()]]
    windows0 = sg.Window('python网络查询工具V1.02', layout0)
    progress_bar = windows0['progressbar']
    for iii in range(100):
        windows0.read(timeout=20)
        progress_bar.UpdateBar(iii + 1)
        windows0['pct'].update(iii)
    system_info1, local_ip1 = get_sys_info()  # 获取系统信息和局域网ip
    thread = MyThread()
    thread.start()
    thread.join()
    public_ip1 = '0.0.0.0'
    if style1 == '线路1':
        public_ip1 = thread.get_public_ip()  # 采用线路一检测
    elif style1 == '线路2':
        public_ip1 = thread.get_public_ip2()  # 采用线路二检测
    windows0.close()
    b = time.time()
    return system_info1, local_ip1, public_ip1, b-a


if __name__ == "__main__":
    # -- 开始构件GUI --#
    # 设置自定义字体
    my_font = 'Deja_Vu_Sans_Mono.ttf'
    my_font_style1 = (my_font, 11, "normal")
    layout_1 = [
        [sg.Text('选择线路：'), sg.InputCombo(values=['线路1', '线路2'], default_value='线路1', key='style', size=(10, 10))],
        [sg.Button('开始检测'), sg.Button('退出')]
    ]
    windows_1 = sg.Window('python网络查询工具V1.02', layout=layout_1, font=my_font_style1, size=(320, 80))
    system_info, local_ip, public_ip = (None, None, None)
    for i in range(2):
        event_1, value_1 = windows_1.read()
        if event_1 in ('退出', None):
            sg.popup('闲着你，干嘛打开我')
            break
        elif event_1 == '开始检测':
            style_1 = windows_1['style'].get()
            system_info, local_ip, public_ip, time1 = start_check(style_1)
            sg.popup('获取完成，共用时{}秒'.format(round(time1, 2)), auto_close=True, auto_close_duration=2)
            break
    windows_1.close()
    layout = [
        [sg.Text('当前系统：'), sg.Text(system_info)],
        [sg.Text('局域网ip:'), sg.Text(local_ip, key='local_ip'), sg.Button('复制1')],
        [sg.Text('公网ip:'), sg.Text(public_ip, key='public_ip'), sg.Button('复制2')],
        [sg.Button('检测ip变动'), sg.Button('重新检测ip'), sg.Button('退出')]
    ]
    windows = sg.Window('python网络查询工具V1.02', layout=layout, font=my_font_style1, size=(320, 140))
    for i in range(5):
        event, values = windows.read()
        if event in (None, '退出'):
            break
        elif event == '复制1':
            try:
                pyperclip.copy(local_ip)
            except Exception as err:
                if system_info == 'Linux':
                    sg.popup('错误，你的系统可能缺少相应安装包',
                             '请输入以下指令安装相关依赖',
                             'sudo apt-get install xsel xclip', title='错误', font=my_font_style1)
                else:
                    sg.popup(err)
        elif event == '复制2':
            try:
                pyperclip.copy(public_ip)
            except Exception as err:
                if system_info == 'Linux':
                    sg.popup('错误，你的系统可能缺少相应安装包',
                             '请输入以下指令安装相关依赖',
                             'sudo apt-get install xsel xclip', title='错误',font=my_font_style1)
                else:
                    sg.popup(err)
                    sg.popup(err)
        elif event == '检测ip变动':
            list2 = load_data()  # 加载ip列表
            if len(list2) == 0:  # 如果为空
                sg.popup('当前Ip列表为空，请重新点击', title='提示', auto_close=True,
                         auto_close_duration=3, font=my_font_style1)
                list2.append(public_ip)
                save_data(list2)
            elif public_ip in list2:  # 如果Ip在集合中
                sg.popup('ip未发生变动', auto_close=True, auto_close_duration=4, title='提示', font=my_font_style1)
                sg.popup('历史Ip为', list2, auto_close=True,
                         auto_close_duration=4, title='提示',
                         font=my_font_style1)
            elif public_ip not in list2:
                sg.popup('ip发生变化', auto_close=True, auto_close_duration=3, title='提示', font=my_font_style1)
                list2.append(public_ip)
                save_data(list2)
        elif event == '重新检测ip':
            system_info, local_ip, public_ip, time1 = start_check(style_1)
            sg.popup('获取完成，共用时{}秒'.format(round(time1, 2)), auto_close=True, auto_close_duration=2)
            windows['public_ip'].update(public_ip)
    windows.close()
