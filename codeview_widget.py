import tkinter as tk
import tkinter.font as tkfont
import customtkinter as ctk
import pyautogui
from idlelib.colorizer import ColorDelegator
from idlelib.percolator import Percolator


class CodeView(tk.Text):
    def __init__(self, master=None, cnf={}, **kw):
        self.data = list(globals().keys())
        self.yscrollbar = ctk.CTkScrollbar(master, orientation='vertical')
        self.yscrollbar.pack(side=tk.RIGHT, fill='y')
        self.xscrollbar = ctk.CTkScrollbar(master, orientation='horizontal')
        self.xscrollbar.pack(side=tk.BOTTOM, fill='x')
        kw['yscrollcommand'] = self.yscrollbar.set
        kw['xscrollcommand'] = self.xscrollbar.set
        kw['wrap'] = tk.NONE
        kw['background'] = '#1c1c1b'
        kw['foreground'] = 'white'
        super().__init__(master, cnf, **kw)
        self.yscrollbar.configure(command=self.yview)
        self.xscrollbar.configure(command=self.xview)
        master.bind("(", self.bracket)
        master.bind('"', self.string_quote)
        master.bind("'", self.string_quote)
        master.bind("<space>", self.refresh)
        cdg = ColorDelegator()
        cdg.tagdefs['COMMENT'] = {'foreground': '#FF0000', 'background': '#1c1c1b'}
        cdg.tagdefs['KEYWORD'] = {'foreground': '#007F00', 'background': '#1c1c1b'}
        cdg.tagdefs['BUILTIN'] = {'foreground': '#7F7F00', 'background': '#1c1c1b'}
        cdg.tagdefs['STRING'] = {'foreground': '#7F3F00', 'background': '#1c1c1b'}
        cdg.tagdefs['DEFINITION'] = {'foreground': '#007F7F', 'background': '#1c1c1b'}
        cdg.tagdefs['FUNCTION'] = {'foreground': '#FF0000', 'background': '#1c1c1b'}
        cdg.tagdefs['CLASS'] = {'foreground': '#FF0000', 'background': '#1c1c1b'}
        self.configure(font=tkfont.Font(family='Consolas', size=24), tabs=tkfont.Font().measure('222222'))
        Percolator(self).insertfilter(cdg)
        self.config(insertbackground='#FFFFFF')

    def bracket(self, event):
        if event.char == '(':
            self.insert(self.index(tk.INSERT), ')')
            pyautogui.keyUp('shift')
            pyautogui.press('left')

    def string_quote(self, event):
        self.insert(self.index(tk.INSERT), f'{event.char}')
        pyautogui.keyUp('shift')
        pyautogui.press('left')

    def refresh(self, event):
        self.data = list(globals().keys())
