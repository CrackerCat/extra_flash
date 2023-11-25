import os
import subprocess
from os import getcwd, sep
from threading import Thread

import sv_ttk
from tkinter import *
from tkinter.ttk import *

osname = os.name


def cz(func, *args):
    Thread(target=func, args=args, daemon=True).start()


def call(exe, kz='Y', out=0, shstate=False, sp=0):
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
        ret = subprocess.Popen(cmd, shell=shstate, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, creationflags=conf)
        for i in iter(ret.stdout.readline, b""):
            if out == 0:
                print(i.decode("utf-8", "ignore").strip())
    except subprocess.CalledProcessError as e:
        for i in iter(e.stdout.readline, b""):
            if out == 0:
                print(e.decode("utf-8", "ignore").strip())
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
        self.title('MIO-KITCHEN-FLASH-TOOL')
        sv_ttk.use_dark_theme()
        self.controls()
        Center_Show(self)

    def controls(self):
        Label(self, text="MIO-KITCHEN-FLASH-TOOL", font=(None, 20)).pack()


if __name__ == '__main__':
    app = FlashTool()
    app.mainloop()
