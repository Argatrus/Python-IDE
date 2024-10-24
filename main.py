import customtkinter as ctk
import os
from codeview_widget import CodeView

ctk.set_appearance_mode('Dark')
ctk.set_default_color_theme('blue')


class Processing:
    def __init__(self, name='nil'):
        self.codefile = []
        self.name = name
        self.currentcodefile = []

    def save(self, codefile):
        with open(f'{self.name}', 'w') as file:
            for line in codefile: file.write(line)
        self.currentcodefile = self.codefile
        return 'done'

    def run(self, code):
        os.system('cls')
        exec(code)

    def show_code(self):
        with open(f'{self.name}', 'r') as file:
            return file.read()


class ClientSide(ctk.CTk):
    def __init__(self, main= Processing):
        super().__init__()
        self.main = main()
        self.title('AS_IDE')
        self.textbox = CodeView(self, font='Arial, 16')
        self.save_button = ctk.CTkButton(self, text='Save', command=self.save)
        self.run_button = ctk.CTkButton(self, text='Run', command=self.run)
        self.open_file = ctk.CTkButton(self, text='Open File', command=self.open)
        self.run_button.pack()
        self.save_button.pack()
        self.open_file.pack()
        self.textbox.pack(fill='both')

    def run(self):
        self.main.run(self.textbox.get('1.0', ctk.END))

    def save(self):
        if self.main.name != 'nil':
            self.main.save(self.textbox.get('1.0', ctk.END))
        else:
            self.main = Processing(ctk.filedialog.asksaveasfile().name)
            self.main.save(self.textbox.get('1.0', ctk.END))

    def open(self):
        self.main = Processing(ctk.filedialog.askopenfilename())
        self.textbox.delete('0.0', ctk.END)
        self.textbox.insert('0.0', self.main.show_code())


if __name__ == '__main__':
    ClientSide().mainloop()
