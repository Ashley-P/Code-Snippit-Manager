import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk
from tkinter import messagebox



BUTTON_WIDTH = 10
BOX_WIDTH = 50
LINE_HEIGHT = 15



class AutoScrollbar(tk.Scrollbar):
    '''Scrollbar that autohides when not needed'''
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.tk.call("grid", "remove", self)
        else:
            self.grid()

        tk.Scrollbar.set(self, lo, hi)
    
    def pack(self, **kwargs):
        pass

    def place(self, **kwargs):
        pass

class Manager(tk.Frame):
    
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky='nsew')
        self.init_gui()

    def init_gui(self):
        # Making the frame stick to the window
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=1)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=1)

        # Frames
        self.button_frame = tk.Frame(self, bd=2, relief=tk.SUNKEN)
        self.button_frame.grid(column=0, row=2, sticky='nw')

        self.listbox_frame = tk.Frame(self)
        self.listbox_frame.grid(column=1, row=2, sticky='nw')
        self.listbox_frame.grid_rowconfigure(0, weight=1)

        self.search_frame = tk.Frame(self)
        self.search_frame.grid(column=1, row=1, columnspan=2, sticky='new')
        self.search_frame.grid_columnconfigure(0, weight=1)

        self.text_frame = tk.Frame(self)
        self.text_frame.grid(column=2, row=2, sticky='nw')

        self.text_frame.columnconfigure(0, weight=1)
        self.text_frame.columnconfigure(1, weight=0)

        self.text_frame.rowconfigure(0, weight=1)
        self.text_frame.rowconfigure(1, weight=0)

        # Buttons
        tk.Button(self.button_frame, text='Add', width=BUTTON_WIDTH, command=None).pack()
        tk.Button(self.button_frame, text='Remove', width=BUTTON_WIDTH, command=None).pack()
        tk.Button(self.button_frame, text='Edit', width=BUTTON_WIDTH, command=None).pack()
        tk.Button(self.button_frame, text='Copy', width=BUTTON_WIDTH, command=None).pack()

        tk.Button(self.search_frame, text='Search', width=int(BUTTON_WIDTH/2), command=None).grid(column=1, row=0, sticky='e', padx=1, pady=1)
            
        # Listbox
        self.code_list_scroll = AutoScrollbar(self.listbox_frame, orient=tk.VERTICAL)
        self.code_list = tk.Listbox(self.listbox_frame, yscrollcommand=self.code_list_scroll.set, width=LINE_HEIGHT, height=LINE_HEIGHT)
        self.code_list_scroll.config(command=self.code_list.yview)

        self.code_list.pack(side=tk.LEFT)
        self.code_list_scroll.pack(side=tk.RIGHT)

        # Text Box
        self.code_text_yscroll = AutoScrollbar(self.text_frame, orient=tk.VERTICAL)
        self.code_text_xscroll = AutoScrollbar(self.text_frame, orient=tk.HORIZONTAL)

        self.code_text = tk.Text(self.text_frame, yscrollcommand=self.code_text_yscroll.set, xscrollcommand=self.code_text_xscroll.set, state=tk.DISABLED,
                width=BOX_WIDTH, height=LINE_HEIGHT)

        self.code_text_yscroll.config(command=self.code_text.yview)
        self.code_text_xscroll.config(command=self.code_text.xview)

        self.code_text.grid(column=0, row=0, sticky='nsew')
        self.code_text_yscroll.grid(column=1, row=0, sticky='e')
        self.code_text_xscroll.grid(column=0, row=1, sticky='s')

        # Entry
        self.search_bar = ttk.Entry(self.search_frame)
        self.search_bar.grid(column=0, row=0, sticky='ew', padx=1, pady=1)

        # Menu
        self.menubar = tk.Menu(top)
        top['menu'] = self.menubar

        self.filemenu = tk.Menu(self.menubar)
        self.menubar.add_cascade(label='File', menu=self.filemenu)
        self.filemenu.add_command(label='Open', command=None)
        self.filemenu.add_command(label='Save', command=None)

        # Formatting
        for child in self.winfo_children():
            try:
                child.grid_configure(padx=1, pady=1)
            except:
                pass

if __name__ == "__main__":
    app = Manager()
    app.master.title("Code Snippit Manager")
    app.mainloop()
