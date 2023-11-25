import os
import subprocess
import sys
from os import getcwd, sep
from threading import Thread

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
        self.title('MIO-KITCHEN-FLASH-TOOL')
        self.sub_win = LabelFrame(self, text='功能')
        self.log_win = LabelFrame(self, text='日志')
        self.log = Text(self.log_win)
        self.init_log()
        self.init_sub()
        self.controls()
        Center_Show(self)
        self.log_win.pack(fill=BOTH, side=LEFT, pady=5, padx=5)
        self.sub_win.pack(fill=BOTH, side=LEFT, expand=True, padx=5)

    def controls(self):
        Label(self, text="MIO-KITCHEN-FLASH-TOOL", font=(None, 20)).pack()

    def init_sub(self):
        frame = LabelFrame(self.sub_win)
        frame.pack(padx=5, pady=5)

    def init_log(self):
        self.log.pack(padx=5, pady=5)
        frame = Frame(self.log_win)
        Button(frame, text='清空', command=lambda: cz(self.log.delete, 1.0, END)).pack(side=LEFT, padx=5, pady=5)
        frame.pack(fill=X, side=BOTTOM)
        sys.stdout = StdoutRedirector(self.log)
        sys.stderr = StdoutRedirector(self.log)


if __name__ == '__main__':
    app = FlashTool()
    app.mainloop()
