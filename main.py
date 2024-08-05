from customtkinter import *
from tkinter import *
import os
from codeview_widget import CodeView

set_appearance_mode('Dark')
set_default_color_theme('blue')

class Processing:
    def __init__(self, name='testing'):
        self.codefile = []
        self.name = name
        self.currentcodefile = []

    def save(self, codefile):
        with open(f'{self.name}.py', 'w') as file:
            for line in codefile: file.write(line)
        self.currentcodefile = self.codefile
        return 'done'

    def run(self, code):
        os.system('cls')
        exec(code)

    def show_code(self):
        with open(f'{self.name}.py', 'r') as file:
            return file.read()


class ClientSide(CTk):
    def __init__(self, main= Processing):
        super().__init__()
        self.main = main()
        self.title('AS_IDE')
        self.textbox = CodeView(self, font='Arial, 16')
        self.save_button = CTkButton(self, text='Save', command=self.save)
        self.run_button = CTkButton(self, text='Run', command=self.run)
        self.open_file = CTkButton(self, text='Open File', command=self.open)
        self.run_button.pack()
        self.save_button.pack()
        self.open_file.pack()
        self.textbox.pack()

    def run(self):
        self.main.run(self.textbox.get('1.0', END))

    def save(self):
        if self.main.name != 'testing':
            self.main.save(self.textbox.get('1.0', END))
        else:
            pass

    def open(self):
        self.main = OpenFile(self)
        self.main.mainloop()

class OpenFile(CTk):
    def __init__(self, m: ClientSide):
        super().__init__()
        self.title('Open File')
        self.geometry('300x100')
        self.label = CTkLabel(self, text='Enter Path Below...')
        self.text = CTkEntry(self)
        self.button = CTkButton(self, text='Press Here to Open File', command=self.path_take)
        self.label.pack()
        self.text.pack()
        self.button.pack()
        self.m = m

    def path_take(self):
        self.m.main = Processing(self.text.get())
        self.m.textbox.delete('0.0', END)
        self.m.textbox.insert(self.m.textbox.index(INSERT), self.m.main.show_code())
        self.destroy()

class SaveFile(CTk):
    def __init__(self):
        super().__init__()
        self.geometry('200x100')

if __name__ == '__main__':
    app = ClientSide()
    app.mainloop()