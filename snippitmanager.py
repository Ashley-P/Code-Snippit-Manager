import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk
from tkinter import messagebox



BUTTON_WIDTH = 10
BOX_WIDTH = 50
LINE_HEIGHT = 15
TEST = list('abcdefghijklmnopqrstuvwxyz')

class Manager(ttk.Frame):
    
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.grid(sticky='nsew')
        self.initgui()

    def deletefromlist(self):
        if messagebox.askokcancel(title="Delete Snippit", message="Do you really want to delete this code snippit?") == True:
            self.code_list.delete(self.code_list.curselection())
        else:
            pass

    def initgui(self):
        # Making the frame stick to the window
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Buttons
        tk.Button(self, text='Add', width=BUTTON_WIDTH).grid(column=0, row=1, sticky='w')
        tk.Button(self, text='Remove', width=BUTTON_WIDTH, command=self.deletefromlist).grid(column=0, row=2, sticky='w')
        tk.Button(self, text='Edit', width=BUTTON_WIDTH).grid(column=0, row=3, sticky='w')

        # Entry
        ttk.Entry(self, text='weed', width=BOX_WIDTH*2).grid(column=1, row=0, columnspan=3, sticky='w')

        # Listbox
        self.y_scroll = tk.Scrollbar(self, orient=tk.VERTICAL) # Scrolling
        self.y_scroll.grid(column=2, row=1, rowspan=4, sticky='nsw')

        self.code_list = tk.Listbox(self, selectmode=tk.SINGLE, yscrollcommand=self.y_scroll.set, width=15, height=LINE_HEIGHT)
        self.code_list.grid(column=1, row=1, rowspan=4)
        
        self.y_scroll['command'] = self.code_list.yview

        # Text
        self.code_text = tk.Text(self, width=BOX_WIDTH, height=LINE_HEIGHT)
        self.code_text.grid(column=3, row=1, rowspan=3)

        self.font=tkfont.Font(font=self.code_text['font'])
        self.code_text.config(tabs=(self.font.measure('    ')), state=tk.DISABLED) # Disabling editing the text on the main window

        # Formatting
        for child in self.winfo_children():
            child.grid_configure(padx=2, pady=2)

        for i in TEST:
            self.code_list.insert(tk.END, i)

if __name__ == "__main__":
    app = Manager()
    app.mainloop()
