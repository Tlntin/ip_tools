import requests
import re
import socket
import platform
import PySimpleGUI as sg
import pyperclip
import time


def get_public_ip():
    """
    此函数用于获取当前设备下的公网ip
    :return:公网ip地址
    """
    public_ip1 = '0.0.0.0'
    for ii in range(3):
        try:
            response = requests.get('http://myip.kkcha.com/', timeout=10)
            html = response.text
            p = re.compile('var sRemoteAddr = \'(.*?)\'')
            result = p.search(html)
            public_ip1 = result.group(1)
            break
        except Exception as err:
            print(err)
            time.sleep(5)
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


if __name__ == "__main__":
    system_info, local_ip = get_sys_info()  # 获取系统信息和局域网ip
    public_ip = get_public_ip()   # 获取公网ip地址
    # -- 开始构件GUI --#
    # 设置自定义字体
    my_font = 'Deja_Vu_Sans_Mono.ttf'
    my_font_style1 = (my_font, 11, "normal")
    layout = [
        [sg.Text('当前系统：'), sg.Text(system_info)],
        [sg.Text('局域网ip:'), sg.Text(local_ip), sg.Button('复制1')],
        [sg.Text('公网ip:'), sg.Text(public_ip), sg.Button('复制2')],
        [sg.Button('退出')]
    ]
    windows = sg.Window('python网络查询工具', layout=layout, font=my_font_style1, size=(300, 140))
    for i in range(5):
        event, values = windows.read()
        if event in (None, '退出'):
            break
        if event == '复制1':
            try:
                pyperclip.copy(local_ip)
            except Exception as err:
                if system_info == 'Linux':
                    sg.popup('错误，你的系统可能缺少相应安装包',
                             '请输入以下指令安装相关依赖',
                             'sudo apt-get install xsel xclip', title='错误')
                else:
                    sg.popup(err)
        if event == '复制2':
            try:
                pyperclip.copy(public_ip)
            except Exception as err:
                if system_info == 'Linux':
                    sg.popup('错误，你的系统可能缺少相应安装包',
                             '请输入以下指令安装相关依赖',
                             'sudo apt-get install xsel xclip', title='错误')
                else:
                    sg.popup(err)
    windows.close()
