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
        cmd = f'{getcwd()}{sep}bin{sep}{command}'
    else:
        cmd = command
    try:
        ret = subprocess.check_output(cmd, shell=sh_state, stderr=subprocess.STDOUT)
        output = ret
    except subprocess.CalledProcessError as e:
        output = e
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
                    out_t = i.decode("utf-8").strip()
                except UnicodeDecodeError:
                    out_t = i.decode("gbk").strip()
                print(out_t)
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

    @staticmethod
    def install_driver():
        for i in ['Win_Driver\\Google\\Driver\\android_winusb.inf', 'Win_Driver\\Qualcomm\\Driver\\qcser.inf']:
            call(f"pnputil /add-driver {i}", kz='N')


class FlashTool(Tk):
    def __init__(self):
        super().__init__()
        self.flash_button = None
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
        self.sweep_data = IntVar()
        self.sub_win = LabelFrame(self, text='功能')
        self.notepad = ttk.Notebook(self.sub_win)
        self.notepad.pack(fill=BOTH, expand=True)
        self.flash = ttk.Frame(self.notepad)
        self.notepad.add(self.flash, text="刷机")
        self.fast_cmd = ttk.Frame(self.notepad)
        self.init_fast_cmd()
        self.notepad.add(self.fast_cmd, text="快捷命令")
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

    def init_fast_cmd(self):
        Label(self.fast_cmd, text="快捷命令", font=(None, 20)).pack(padx=5, pady=5)
        Button(self.fast_cmd, text='FB重启手机', width=20, command=lambda: cz(call, 'fastboot reboot')).pack(padx=5,
                                                                                                             pady=5)

    def controls(self):
        Label(self, text="MIO-KITCHEN-FLASH-TOOL", font=(None, 20)).pack()

    def init_driver(self):
        Label(self.driver, text="驱动安装", font=(None, 20)).pack()
        Button(self.driver, text='刷机驱动', width=20, command=lambda: cz(utils().install_driver)).pack(padx=5, pady=5)

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
        Checkbutton(self.frame, text="删除用户数据", variable=self.sweep_data, onvalue=1, offvalue=0,
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
        self.frame = LabelFrame(self.flash, text="刷机选项")
        Checkbutton(self.frame, text="修补Boot", variable=self.patch_boot, onvalue=1, offvalue=0,
                    style='Switch.TCheckbutton').pack(padx=2, pady=2, side=BOTTOM)
        cs = 0
        for v in ['删除全部数据', '保留用户数据', '删除数据并上锁BL']:
            cs += 1
            ttk.Radiobutton(self.frame, text=v, variable=self.flash_cz, value=cs).pack(side=TOP, padx=2, pady=2)
        self.frame.pack(padx=5, pady=5)
        self.flash_button = Button(self.flash, text="开始刷机", command=lambda: cz(self.flash_official))
        self.flash_button.pack(side=BOTTOM, padx=4, pady=10, fill=X)

    def init_log(self):
        self.log.pack(padx=5, pady=5)
        frame = Frame(self.log_win)
        Button(frame, text='清空', command=lambda: cz(self.log.delete, 1.0, END)).pack(side=LEFT, padx=5, pady=5)
        frame.pack(side=BOTTOM)
        sys.stdout = StdoutRedirector(self.log)
        sys.stderr = StdoutRedirector(self.log)

    def disable(self):
        self.flash_button.configure(state='disabled', text="正在等待设备")
        for i in self.frame.winfo_children():
            i.configure(state='disabled')

    def enable(self):
        for i in self.frame.winfo_children():
            i.configure(state='normal')
        self.flash_button.config(state='normal', text="开始刷机")

    def flash_official(self):
        self.disable()
        try:
            device_id = run_command("fastboot devices").strip().split()[0]
        except IndexError:
            self.enable()
            print("未发现设备")
            return

        print(f"发现设备:{device_id}")
        try:
            self.get_device_info()
        except ValueError as e:
            print(e.__str__())
        self.enable()

    def flash_my_rom(self):
        self.disable()
        try:
            device_id = run_command("fastboot devices").strip().split()[0]
        except IndexError:
            self.enable()
            print("未发现设备")
            return
        print(f"发现设备:{device_id}")
        try:
            self.get_device_info()
        except ValueError as e:
            print(e.__str__())
        self.enable()

    def get_device_info(self):
        device = run_command('fastboot getvar product')
        lot_count = run_command("fastboot getvar slot-count")
        device = device.split("\n")[0].split(': ')[1].strip()
        lot_count = lot_count.split("\n")[0].split(': ')[1].strip()
        if not lot_count:
            lot_count = 0
        self.device.set(f"""设备代号：{device}\n\nSlot数量:{lot_count}""")
        self.device_code.set(device)
        self.slot.set(int(lot_count))


if __name__ == '__main__':
    app = FlashTool()
    app.mainloop()
