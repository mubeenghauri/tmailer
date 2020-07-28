import tkinter as tk
from tkinter import ttk as ttk
from email_tab import EmailTab
from setup_tab import SetupTab
from go_tab import GoTab
from config import Configuration

class MainApp(tk.Frame):

    def __init__(self, master):
        self.master = master     # master is root
        self.configuration = Configuration()

        tk.Frame.__init__(self, self.master)
        self.configure_gui()
        self.create_notebook(self.master)

    def create_notebook(self, master):
        self.notebook = ttk.Notebook(master)
        self.notebook.pack()
        self.init_tabs(self.notebook)
        self.notebook.add(self.setupTab, text="Setup")
        self.notebook.add(self.emailTab, text="Email",)
        self.notebook.add(self.goTab, text="GO !")
        self.notebook.enable_traversal()
        self.notebook.grid( row=1, column=1)
        # self.notebook.bind("<<NotebookTabChanged>>", self.initGoTab)

    def init_tabs(self, nb):
        self.setupTab = tk.Frame(nb, width=600, height=500, padx=50)
        SetupTab(self.setupTab, self.configuration).grid(row=2, column=1)
        self.emailTab = EmailTab(nb)
        self.goTab = GoTab(nb, self.configuration)

        

    def initGoTab(self, event):
        pass

        
    def configure_gui(self):
        self.master.title("Emailer")
        self.master.geometry("900x500") 

    

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    app.mainloop()