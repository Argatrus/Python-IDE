import customtkinter as ctk
import subprocess
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

    def run(self):
        command = f'python {self.name}'
        return subprocess.run(command, shell=True, capture_output=True, text=True)

    def show_code(self):
        with open(f'{self.name}', 'r') as file:
            return file.read()


class ClientSide(ctk.CTk):
    def __init__(self, main= Processing):
        super().__init__()
        self.main = main()
        self.title('IDE')
        self.textbox = CodeView(self, font='Arial, 10')
        self.save_button = ctk.CTkButton(self, text='Save File', command=self.save)
        self.run_button = ctk.CTkButton(self, text='|>', command=self.run)
        self.open_file = ctk.CTkButton(self, text='Open File', command=self.open)
        self.output_text = ctk.CTkTextbox(self, wrap='word', width=300, font=ctk.CTkFont(family='Arial', size=20))
        self.open_file.pack()
        self.save_button.pack()
        self.run_button.pack()
        self.output_text.pack(side ='left', fill='both')
        self.textbox.pack(fill='both')


    def run(self):
        if self.main.name == 'nil':
            self.main = Processing(ctk.filedialog.asksaveasfile().name)
            self.main.save(self.textbox.get('1.0', ctk.END))
        else:
            result = self.main.run()
            self.output_text.insert(ctk.END, result.stdout)
            self.output_text.insert(ctk.END, result.stderr)
            self.output_text.insert(ctk.END, '\n\n')


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
