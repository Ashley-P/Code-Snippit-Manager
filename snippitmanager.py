import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import subprocess



BUTTON_WIDTH = 10
BOX_WIDTH = 50
LINE_HEIGHT = 15
CODE_LIST = {}



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


class CodeClass(object):
    '''Class which holds the info for each code snippit'''
    __slots__ = ['name', 'description', 'code', 'code_type']
    def __init__(self, name, description, code, code_type):
        self.name = name
        self.description = description
        self.code = code
        self.code_type = code_type


class Manager(tk.Frame):
    
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky='nsew')
        self.init_gui()

    def new_window(self, code_class=None):
        self.win = AddEditWindow(code_class)
        self.win.grab_set()
        self.update_list()

    def update_list(self):
        self.code_list.delete(0, 'end')
        for i in CODE_LIST.keys():
            self.code_list.insert('end', i)

    def on_listbox_select(self, *args):
        self.i = self.code_list.curselection()
        self.code_text['state'] = tk.NORMAL
        try:
            self.code_text.delete(1.0, 'end')
            self.code_text.insert('end', CODE_LIST[self.code_list.get(self.i[0])].code)
        except IndexError:
            pass
        self.code_text['state'] = tk.DISABLED

    def remove(self):
        self.x = self.code_list.curselection()
        del CODE_LIST[self.code_list.get(self.x[0])]
        self.code_list.delete(self.x[0])
        self.code_text['state'] = tk.NORMAL
        self.code_text.delete(1.0, 'end')
        self.code_text['state'] = tk.DISABLED

    def copy_to_clipboard(self, word):
        subprocess.run(['clip.exe'], input=word.strip().encode('utf-8'), check=True)
        print("Done!")


    def init_gui(self):
        # Making the frame stick to the window
        self.top = self.winfo_toplevel()
        self.top.rowconfigure(0, weight=1)
        self.top.columnconfigure(0, weight=1)

        # Making the widgets stretch correctly
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=1)

        # Frames
        self.button_frame = tk.Frame(self, bd=2, relief=tk.SUNKEN, pady=2)
        self.button_frame.grid(column=0, row=1, sticky='nw')

        self.listbox_frame = tk.Frame(self, pady=2)
        self.listbox_frame.grid(column=1, row=1, sticky='ns')
        self.listbox_frame.grid_rowconfigure(0, weight=1)

        self.search_frame = tk.Frame(self)
        self.search_frame.grid(column=1, row=0, columnspan=2, sticky='new')
        self.search_frame.grid_columnconfigure(0, weight=1)

        self.text_frame = tk.Frame(self, padx=2, pady=2)
        self.text_frame.grid(column=2, row=1, sticky='nsew')

        self.text_frame.grid_columnconfigure(0, weight=1)
        self.text_frame.grid_columnconfigure(1, weight=0)

        self.text_frame.grid_rowconfigure(0, weight=1)
        self.text_frame.grid_rowconfigure(1, weight=0)

        # Buttons
        tk.Button(self.button_frame, text='Add', width=BUTTON_WIDTH, command=self.new_window).pack()
        tk.Button(self.button_frame, text='Remove', width=BUTTON_WIDTH, command=self.remove).pack()
        tk.Button(self.button_frame, text='Edit', width=BUTTON_WIDTH, command=lambda:self.new_window(CODE_LIST[self.code_list.get(self.code_list.curselection()[0])])).pack()
        tk.Button(self.button_frame, text='Copy', width=BUTTON_WIDTH, command=lambda:self.copy_to_clipboard(self.code_text.get('1.0', 'end'))).pack()

        tk.Button(self.search_frame, text='Search', width=int(BUTTON_WIDTH/2), command=None).grid(column=1, row=0, sticky='e', padx=1, pady=1)
            
        # Listbox
        self.code_list_scroll = AutoScrollbar(self.listbox_frame, orient=tk.VERTICAL)
        self.code_list = tk.Listbox(self.listbox_frame, yscrollcommand=self.code_list_scroll.set, selectmode=tk.SINGLE, width=LINE_HEIGHT, height=LINE_HEIGHT)
        self.code_list.bind("<<ListboxSelect>>", self.on_listbox_select)
        self.code_list_scroll.config(command=self.code_list.yview)

        self.code_list.grid(column=0, row=0, sticky='ns')
        self.code_list_scroll.grid(column=1, row=0, sticky='nse')

        # Text Box
        self.code_text_yscroll = AutoScrollbar(self.text_frame, orient=tk.VERTICAL)
        self.code_text_xscroll = AutoScrollbar(self.text_frame, orient=tk.HORIZONTAL)

        self.code_text = tk.Text(self.text_frame, yscrollcommand=self.code_text_yscroll.set,
                                                  xscrollcommand=self.code_text_xscroll.set, 
                                                  wrap="none",
                                                  width=BOX_WIDTH,
                                                  height=LINE_HEIGHT)

        self.font = tkfont.Font(font=self.code_text['font'])
        self.tab_width = self.font.measure(' ' * 4)
        self.code_text.config(tabs=(self.tab_width,))

        self.code_text['state'] = tk.DISABLED

        self.code_text_yscroll.config(command=self.code_text.yview)
        self.code_text_xscroll.config(command=self.code_text.xview)

        self.code_text.grid(column=0, row=0, sticky='nsew')
        self.code_text_yscroll.grid(column=1, row=0, sticky='nse')
        self.code_text_xscroll.grid(column=0, row=1, sticky='sew')

        # Entry
        self.search_bar = ttk.Entry(self.search_frame)
        self.search_bar.grid(column=0, row=0, sticky='ew', padx=1, pady=1)

        # Menu
        self.menubar = tk.Menu(self.top)
        self.top['menu'] = self.menubar

        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='File', menu=self.filemenu)
        self.filemenu.add_command(label='Open', command=None)
        self.filemenu.add_command(label='Save', command=None)

        # Formatting
        for child in self.winfo_children():
            try:
                child.grid_configure(padx=1, pady=1)
            except:
                pass





class AddEditWindow(tk.Toplevel):
    '''Joint window for adding and editing code snippits'''
    def __init__(self, code_class, master=None):
        tk.Toplevel.__init__(self, master)
        self.code_class = code_class
        self.grid()
        self.init_gui()
        if self.code_class != None:
            self.name_entry.insert("end", self.code_class.name)
            self.description_text.insert("end", self.code_class.description)
            self.code_text.insert("end", self.code_class.code)
            self.code_type.set(self.code_class.code_type)
        else:
            pass

    def create_class(self):
        CODE_LIST[self.name_entry.get()] = CodeClass(name=self.name_entry.get(),
                                           description=self.description_text.get('1.0', 'end'),
                                           code=self.code_text.get('1.0', 'end'),
                                           code_type=self.code_type.get())
        app.update_list()
        self.destroy()

    def edit_class(self):
        del CODE_LIST[self.code_class.name]
        CODE_LIST[self.name_entry.get()] = self.code_class
        self.code_class.name = self.name_entry.get()
        self.code_class.description = self.description_text.get('1.0', 'end')
        self.code_class.code = self.code_text.get('1.0', 'end')
        self.code_class.code_type = self.code_type.get()
        app.update_list()
        self.destroy()

    def choose_create_edit(self, *args, **kwargs):
        if self.code_class == None:
            self.create_class()
        else:
            self.edit_class()

    def init_gui(self):
        self.top = self.winfo_toplevel()
        self.top.grid_rowconfigure(0, weight=1)
        self.top.grid_columnconfigure(0, weight=1)

        # Frames
        self.main_frame = tk.Frame(self)
        self.main_frame.grid(column=0, row=0, padx=5, pady=5, sticky='nsew')

        self.main_frame.grid_columnconfigure(0, weight=0)
        self.main_frame.grid_columnconfigure(1, weight=1)

        self.main_frame.grid_rowconfigure(0, weight=0)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)

        
        self.description_frame = tk.Frame(self.main_frame)
        self.description_frame.grid(column=1, row=1, pady=5, sticky='nsew')

        self.description_frame.grid_columnconfigure(0, weight=1)
        self.description_frame.grid_rowconfigure(0, weight=1)


        self.code_frame = tk.Frame(self.main_frame)
        self.code_frame.grid(column=1, row=2, pady=5, sticky='nsew')

        self.code_frame.grid_columnconfigure(0, weight=1)
        self.code_frame.grid_rowconfigure(0, weight=1)

        self.radio_frame = tk.Frame(self.main_frame, bd=2, relief=tk.SUNKEN)
        self.radio_frame.grid(column=0, row=3, columnspan=2)

        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.grid(column=0, row=4, pady=5, columnspan=2)

        # Labels
        tk.Label(self.main_frame, text='Name:').grid(column=0, row=0, padx=5)
        tk.Label(self.main_frame, text='Description:').grid(column=0, row=1, padx=5)
        tk.Label(self.main_frame, text='Code:').grid(column=0, row=2, padx=5)
        
        tk.Label(self.radio_frame, text='Code Type:').grid(column=0, row=0, columnspan=3)
        
        # Entry
        self.name_entry = tk.Entry(self.main_frame)
        self.name_entry.grid(column=1, row=0, sticky='ew')

        # Description Text box
        self.description_text_yscroll = tk.Scrollbar(self.description_frame, orient=tk.VERTICAL)
        self.description_text_xscroll = tk.Scrollbar(self.description_frame, orient=tk.HORIZONTAL)

        self.description_text = tk.Text(self.description_frame, yscrollcommand=self.description_text_yscroll.set,
                                                                xscrollcommand=self.description_text_xscroll.set, 
                                                                wrap="none",
                                                                width=BOX_WIDTH,
                                                                height=int(LINE_HEIGHT/2))

        self.description_text_yscroll.config(command=self.description_text.yview)
        self.description_text_xscroll.config(command=self.description_text.xview)

        self.description_text.grid(column=0, row=0, sticky='nsew')
        self.description_text_yscroll.grid(column=1, row=0, sticky='nse')
        self.description_text_xscroll.grid(column=0, row=1, sticky='sew')

        # Code Text Box
        self.code_text_yscroll = tk.Scrollbar(self.code_frame, orient=tk.VERTICAL)
        self.code_text_xscroll = tk.Scrollbar(self.code_frame, orient=tk.HORIZONTAL)

        self.code_text = tk.Text(self.code_frame, yscrollcommand=self.code_text_yscroll.set,
                                                  xscrollcommand=self.code_text_xscroll.set, 
                                                  wrap="none",
                                                  width=BOX_WIDTH,
                                                  height=int(LINE_HEIGHT/2))

        self.font = tkfont.Font(font=self.code_text['font'])
        self.tab_width = self.font.measure(' ' * 4)
        self.code_text.config(tabs=(self.tab_width,))

        self.code_text_yscroll.config(command=self.code_text.yview)
        self.code_text_xscroll.config(command=self.code_text.xview)

        self.code_text.grid(column=0, row=0, sticky='nsew')
        self.code_text_yscroll.grid(column=1, row=0, sticky='nse')
        self.code_text_xscroll.grid(column=0, row=1, sticky='sew')

        # Radio Buttons
        self.code_type = tk.StringVar()

        ttk.Radiobutton(self.radio_frame, text='Class', variable=self.code_type, value='Class').grid(column=0, row=1)
        ttk.Radiobutton(self.radio_frame, text='Function', variable=self.code_type, value='Function').grid(column=1, row=1)
        ttk.Radiobutton(self.radio_frame, text='Other', variable=self.code_type, value='Other').grid(column=2, row=1)

        # Buttons
        tk.Button(self.button_frame, text='Ok', width=BUTTON_WIDTH, command=self.choose_create_edit).pack(side=tk.LEFT)
        tk.Button(self.button_frame, text='Cancel', width=BUTTON_WIDTH, command=self.destroy).pack(side=tk.RIGHT)



if __name__ == "__main__":
    app = Manager()
    app.master.title("Code Snippit Manager")
    app.mainloop()
