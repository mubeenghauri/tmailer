import tkinter.filedialog as filedialog
import tkinter.scrolledtext as scrolledtext
from tkinter.simpledialog import _QueryDialog
import tkinter as tk
from tkinter import ttk as ttk
from tksheet import Sheet
from email_sheet_handler import EmailSheetHandler

FILENAME = "email.csv"

class AddDialogue(_QueryDialog):
    def __init__(self,p, *args, **kw):
        self.p = p        
        _QueryDialog.__init__(self, *args, **kw)
        
    def body(self, master):

        self.label1 = tk.Label(master, text="Email : ", justify=tk.LEFT)
        self.label1.grid(row=0, column=0, sticky="w")

        self.entry = tk.Entry(master, name="")
        self.entry.grid(row=0, column=1, stick="e" )

        self.label2 = tk.Label(master, text="Password : ", justify=tk.LEFT)
        self.label2.grid(row=1, column=0, sticky="w")

        self.entry2 = tk.Entry(master, name="")
        self.entry2.grid(row=1, column=1, stick="e" )

        self.label2 = tk.Label(master, text="Limit : ", justify=tk.LEFT)
        self.label2.grid(row=2, column=0, sticky="w")

        self.entry3 = tk.Entry(master, name="")
        self.entry3.grid(row=2, column=1, stick="e" )
        return self.entry

    def getresult(self):
        print("Getting result")
        self.p.append(self.entry.get())
        self.p.append(self.entry2.get())
        self.p.append(self.entry3.get())
        print(self.p)
        return self.entry.get()
        

class EmailTab(tk.Frame):

    def __init__(self, master):
        self.emailHandler = EmailSheetHandler(FILENAME)
        tk.Frame.__init__(self, master)
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)
        self.frame = ttk.Frame(self, height=450, width=400)
        self.frame.grid_columnconfigure(0, weight = 1)
        self.frame.grid_rowconfigure(0, weight = 1)
        self.sheet = Sheet(self.frame,
                           page_up_down_select_row = True,
                           #empty_vertical = 0,
                           column_width = 300,
                           startup_select = (0,1,"rows"),
                           data=self.populate_sheet(),
                            total_columns = 3, #if you want to set empty sheet dimensions at startup
                            height = 450, #height and width arguments are optional
                            width = 600 #For full startup arguments see DOCUMENTATION.md
                            )
        self.sheet.enable_bindings(("single_select", #"single_select" or "toggle_select"
                                         "drag_select",   #enables shift click selection as well
                                         "column_drag_and_drop",
                                         "row_drag_and_drop",
                                         "column_select",
                                         "row_select",
                                         "column_width_resize",
                                         "double_click_column_resize",
                                         "arrowkeys",
                                         "row_height_resize",
                                         "double_click_row_resize",
                                         "right_click_popup_menu",
                                         "rc_select",
                                         "edit_cell"))

        self.sheet.extra_bindings("end_edit_cell", self.end_edit_cell)

        self.frame.grid(row = 0, column = 0, sticky = "nsw")
        self.sheet.grid(row = 0, column = 0, sticky = "nw")

        self.email_button_frame = ttk.Frame(self.frame, padding=(3,3,12,12), borderwidth=5, width=100, heigh=200)
        self.email_add_button = tk.Button(self.email_button_frame, text="Add email", command=self.add_email)
        self.email_merge_button = tk.Button(self.email_button_frame, text="Merge email (with file)", command=self.merge_mails)
        self.email_update_button = tk.Button(self.email_button_frame, text="Update file with table", command=self.email_file_update )
        self.email_button_frame.grid(row=0, column=2, sticky="nswe")
        self.email_add_button.grid(row=1, column=1)
        self.email_merge_button.grid(row=2, column=1)
        self.email_update_button.grid(row=3, column=1)

        # print(self.sheet.get_sheet_data(get_index=0, get_header=0))

    def end_edit_cell(self, event):
        print(event)
        print(self.sheet.get_cell_data(event[0], event[1    ]))

    def add_email(self):
        package = []
        AddDialogue(package, "Add Email", "Add Email")
        print("Rsult: ", package)
        self.emailHandler.append_to_file(package)
        self.update_table()
        
    def email_file_update(self):
        self.emailHandler.update_email_file(self.sheet.get_sheet_data())

    def update_table(self):
        data = self.populate_sheet()
        self.sheet.set_sheet_data(data)
        
    def merge_mails(self):
        file = filedialog.askopenfile().name
        print(file)
        # TODO: handle merge
        print(self.emailHandler.validate(file))

    def populate_sheet(self):
        self.data = []
        try:
            with open(FILENAME, 'r') as f:
                L = f.readlines()
            self.data = [i.strip("\n").split(",") for i in L]
            # for i in self.data: i.append("50")
            return self.data
        except FileNotFoundError:
            return self.data