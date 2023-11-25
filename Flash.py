import tkinter as tk
import sv_ttk
from tkinter import *
from tkinter.ttk import *
import tkinter.ttk as ttk


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
