import tkinter as tk
import sv_ttk
from tkinter import *
from tkinter.ttk import *
import tkinter.ttk as ttk


class FlashTool(Tk):
    def __init__(self):
        super().__init__()
        self.title('MIO-KITCHEN-FLASH-TOOL')
        sv_ttk.use_dark_theme()


if __name__ == '__main__':
    app = FlashTool()
    app.mainloop()
