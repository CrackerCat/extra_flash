import os
import subprocess
import sys
from os import getcwd, sep
from threading import Thread
from tkinter import ttk

from ttkbootstrap.constants import *
from tkinter import *
from tkinter.ttk import *

osname = os.name
bin_dir = os.path.join(os.getcwd(), 'bin')


def cz(func, *args):
    Thread(target=func, args=args, daemon=True).start()


def call(exe, kz='Y', out=0, sh_state=False, sp=0):
    if kz == "Y":
        cmd = f'{getcwd()}{sep}{exe}'
    else:
        cmd = exe
    if osname != 'posix':
        conf = subprocess.CREATE_NO_WINDOW
    else:
        if sp == 0:
            cmd = cmd.split()
        conf = 0
    try:
        ret = subprocess.Popen(cmd, shell=sh_state, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, creationflags=conf)
        for i in iter(ret.stdout.readline, b""):
            if out == 0:
                print(i.decode("utf-8", "ignore").strip())
    except subprocess.CalledProcessError as e:
        print(e.__str__())
    else:
        ret = None
    ret.wait()
    return ret.returncode


class StdoutRedirector(object):
    def __init__(self, text_widget):
        self.text_space = text_widget

    def write(self, string):
        self.text_space.insert(END, string)
        self.text_space.yview('end')

    @staticmethod
    def flush():
        pass

    def __exit__(self):
        pass


class Center_Show(object):
    def __init__(self, master):
        self.master = master
        self.set()

    def set(self):
        self.master.geometry('+{}+{}'.
                             format(int(self.master.winfo_screenwidth() / 2 - self.master.winfo_width() / 2),
                                    int(self.master.winfo_screenheight() / 2 - self.master.winfo_height() / 2)))


class FlashTool(Tk):
    def __init__(self):
        super().__init__()
        self.flash_cz = IntVar()
        self.flash_cz.set(1)
        self.code = self.get_code()
        self.title('MIO-KITCHEN-FLASH-TOOL')
        self.sub_win = LabelFrame(self, text='功能')
        self.notepad = ttk.Notebook(self.sub_win)
        self.notepad.pack(fill=BOTH, expand=True)
        self.flash = ttk.Frame(self.notepad)
        self.notepad.add(self.flash, text="刷机")
        self.driver = ttk.Frame(self.notepad)
        self.init_driver()
        self.notepad.add(self.driver, text="安装驱动")
        self.log_win = LabelFrame(self, text='日志')
        self.log = Text(self.log_win, width=50, height=20)
        self.init_log()
        if self.code:
            self.init_sub_my_rom()
        else:
            self.init_sub_official_rom()
        self.controls()
        self.sub_win.pack(fill=BOTH, side=LEFT, expand=True, padx=5)
        self.log_win.pack(fill=BOTH, side=LEFT, expand=True, pady=5)
        Center_Show(self)
        print("欢迎！")

    @staticmethod
    def get_code():
        right_code = os.path.join(bin_dir, 'right_device')
        if os.path.exists(right_code):
            with open(right_code, 'r', encoding='gbk', newline='\n') as f:
                return f.read().strip()
        else:
            return None

    def controls(self):
        Label(self, text="MIO-KITCHEN-FLASH-TOOL", font=(None, 20)).pack()

    def init_driver(self):
        Label(self.driver, text="驱动安装", font=(None, 20)).pack()
        Button(self.driver, text='')

    def init_sub_my_rom(self):
        frame = LabelFrame(self.flash, text="ROM信息")
        Label(frame, text=f"此ROM只适用于{self.code}", font=(None, 15)).pack()
        frame.pack(padx=5, pady=5)

    def init_sub_official_rom(self):
        frame = LabelFrame(self.flash, text="ROM信息")
        Label(frame, text=f"小米官方ROM", font=(None, 15)).pack()
        frame.pack(padx=5, pady=5)
        frame = LabelFrame(self.flash, text="刷机选项")
        cs = 0
        for v in ['删除全部数据并刷机', '保留用户数据并刷机', '删除全部数据并刷机和上锁BL']:
            cs += 1
            ttk.Radiobutton(frame, text=v, variable=self.flash_cz, value=cs).pack(side=TOP, padx=2, pady=2)
        frame.pack(padx=5, pady=5)

    def init_log(self):
        self.log.pack(padx=5, pady=5)
        frame = Frame(self.log_win)
        Button(frame, text='清空', command=lambda: cz(self.log.delete, 1.0, END)).pack(side=LEFT, padx=5, pady=5)
        frame.pack(side=BOTTOM)
        sys.stdout = StdoutRedirector(self.log)
        sys.stderr = StdoutRedirector(self.log)


if __name__ == '__main__':
    app = FlashTool()
    app.mainloop()
