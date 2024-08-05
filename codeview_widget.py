from tkinter import *
from customtkinter import *
import pyautogui
from idlelib.colorizer import ColorDelegator
from idlelib.percolator import Percolator


class CodeView(Text):
    def __init__(self, master=None, cnf={}, **kw):
        self.data = list(globals().keys())
        self.yscrollbar = Scrollbar(master, orient='vertical')
        self.yscrollbar.pack(side=RIGHT, fill='y')
        self.xscrollbar = Scrollbar(master, orient='horizontal')
        self.xscrollbar.pack(side=BOTTOM, fill='x')
        kw['yscrollcommand'] = self.yscrollbar.set
        kw['xscrollcommand'] = self.xscrollbar.set
        kw['wrap'] = NONE
        kw['background'] = '#1c1c1b'
        kw['foreground'] = 'white'
        super().__init__(master, cnf, **kw)
        self.yscrollbar.config(command=self.yview)
        self.xscrollbar.config(command=self.xview)
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

        Percolator(self).insertfilter(cdg)
        self.config(insertbackground='#FFFFFF')

    def bracket(self, event):
        if event.char == '(':
            self.insert(self.index(INSERT), ')')
            pyautogui.keyUp('shift')
            pyautogui.press('left')

    def string_quote(self, event):
        self.insert(self.index(INSERT), f'{event.char}')
        pyautogui.keyUp('shift')
        pyautogui.press('left')

    def refresh(self, event):
        self.data = list(globals().keys())
