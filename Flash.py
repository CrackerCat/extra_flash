import os
import subprocess
import sys
from os import getcwd, sep
from threading import Thread
from tkinter import ttk

import sv_ttk
from tkinter import *
from tkinter.ttk import *

osname = os.name
bin_dir = os.path.join(os.getcwd(), 'bin')
if osname == 'nt':
    from ctypes import windll


def cz(func, *args):
    Thread(target=func, args=args, daemon=True).start()


def run_command(command, kz='Y', sh_state=False):
    if kz == "Y":
        cmd = f'{getcwd()}{sep}{command}'
    else:
        cmd = command
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=sh_state)
    output, error = process.communicate()
    try:
        output_ = output.decode('utf-8').strip()
    except UnicodeDecodeError:
        output_ = output.decode('gbk').strip()
    return output_


def call(exe, kz='Y', out=0, sh_state=False, sp=0):
    if kz == "Y":
        cmd = f'{getcwd()}{sep}bin{sep}{exe}'
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
                try:
                    outt = i.decode("utf-8").strip()
                except UnicodeDecodeError:
                    outt = i.decode("gbk").strip()
                print(outt)
    except subprocess.CalledProcessError as e:
        print(e.__str__())
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


class utils:
    def __init__(self):
        pass

    def install_driver(self):
        for i in ['Win_Driver\\Google\\Driver\\android_winusb.inf', 'Win_Driver\\Qualcomm\\Driver\\qcser.inf']:
            call(f"pnputil /add-driver {i}", kz='N')


class FlashTool(Tk):
    def __init__(self):
        super().__init__()
        self.flash_cz = IntVar()
        self.flash_cz.set(1)
        sv_ttk.use_dark_theme()
        self.code = self.get_code()
        self.title('MIO-KITCHEN-FLASH-TOOL')
        self.patch_boot = IntVar()
        self.device = StringVar()
        self.device.set("Unknown")
        self.device_code = StringVar()
        self.slot = IntVar()
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
        if not self.code:
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
        Button(self.driver, text='刷机驱动', width=20, command=lambda: utils().install_driver()).pack(padx=5, pady=5)

    def init_sub_my_rom(self):
        frame = LabelFrame(self.flash, text="ROM信息")
        Label(frame, text=f"此ROM只适用于{self.code}", font=(None, 15)).pack(padx=5, pady=5)
        frame.pack(padx=5, pady=5)
        frame = LabelFrame(self.flash, text="设备信息")
        Label(frame, textvariable=self.device, font=(None, 15)).pack(padx=5, pady=5)
        frame.pack(padx=5, pady=5)
        self.frame = LabelFrame(self.flash, text="刷机选项")
        Checkbutton(self.frame, text="修补Boot", variable=self.patch_boot, onvalue=1, offvalue=0,
                    style='Switch.TCheckbutton').pack(padx=2, pady=2, side=BOTTOM)
        self.frame.pack(padx=5, pady=5)
        self.flash_button = Button(self.flash, text="开始刷机", command=lambda: cz(self.flash_my_rom))
        self.flash_button.pack(side=BOTTOM, padx=4, pady=10, fill=X)

    def init_sub_official_rom(self):
        frame = LabelFrame(self.flash, text="ROM信息")
        Label(frame, text=f"小米官方ROM", font=(None, 15)).pack()
        frame.pack(padx=5, pady=5)
        frame = LabelFrame(self.flash, text="设备信息")
        Label(frame, textvariable=self.device, font=(None, 15)).pack(padx=5, pady=5)
        frame.pack(padx=5, pady=5)
        frame = LabelFrame(self.flash, text="刷机选项")
        Checkbutton(frame, text="修补Boot", variable=self.patch_boot, onvalue=1, offvalue=0,
                    style='Switch.TCheckbutton').pack(padx=2, pady=2, side=BOTTOM)
        cs = 0
        for v in ['删除全部数据', '保留用户数据', '删除数据并上锁BL']:
            cs += 1
            ttk.Radiobutton(frame, text=v, variable=self.flash_cz, value=cs).pack(side=TOP, padx=2, pady=2)
        frame.pack(padx=5, pady=5)
        Button(self.flash, text="开始刷机").pack(side=BOTTOM, padx=4, pady=10, fill=X)

    def init_log(self):
        self.log.pack(padx=5, pady=5)
        frame = Frame(self.log_win)
        Button(frame, text='清空', command=lambda: cz(self.log.delete, 1.0, END)).pack(side=LEFT, padx=5, pady=5)
        frame.pack(side=BOTTOM)
        sys.stdout = StdoutRedirector(self.log)
        sys.stderr = StdoutRedirector(self.log)

    def flash_official(self):
        pass

    def flash_my_rom(self):
        self.flash_button.config(state='disabled', text="正在等待设备")
        call("fastboot getvar product")
        self.get_device_info()
        self.flash_button.config(state='normal', text="开始刷机")

    def get_device_info(self):
        device = run_command('fastboot getvar product')
        lot_count = run_command("fastboot getvar slot-count")
        self.device.set(f"""设备代号：{device}\nSlot数量:{lot_count}""")
        self.device_code.set(device)
        self.slot.set(int(lot_count))


if __name__ == '__main__':
    app = FlashTool()
    app.mainloop()
