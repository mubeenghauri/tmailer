import tkinter.filedialog as filedialog
import tkinter.scrolledtext as scrolledtext
import tkinter as tk
from tkinter import ttk as ttk
from tksheet import Sheet


class EmailTab(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.label = tk.Label(self, text="Hey")
        self.label.pack()