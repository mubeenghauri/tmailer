import tkinter.filedialog as filedialog
import tkinter.scrolledtext as scrolledtext
import tkinter as tk

class SetupTab(tk.Frame):
    def __init__(self, master, config, **kw):
        self.config = config
        print(self.config)
        tk.Frame.__init__(self, master, **kw)
        self.text_message = tk.StringVar()
        self.text_message.set("""\
        Hi {},
        Do you have the capacity .....
        """)

        self.subject_line = tk.StringVar()
        self.subject_line.set(self.config.subject_line)
        self.html_message = tk.StringVar()
        self.html_message.set("""\
<html>
<body>
<p>
    Hey {},<br> 
    <br>
    Do you have capacity for more leads?<br>
    <br>
    If I generate exclusive leads for you in return for a small fee, would you be interested?<br>
    <br>
    Regards,<br>
    Nabeel    
</p>
<img src="" width="1" height="1">
<body>
</html>
        """)

        self.setup_radio_choice = tk.IntVar()
        self.setup_path_to_csv = tk.StringVar()
        self.setup_message_choice = tk.IntVar()
        self.setup_message_choice.set(1)
        self.setup_radio_choice.set(1)

        self.setup_label1 = tk.Label(self, text="Choose input type: ", pady=5)
        self.setup_label1.grid(row=0, column=0)
        
        self.setup_file_loc = tk.Entry(self, textvariable=self.setup_path_to_csv)
        self.setup_file_loc.grid(row=1, column=2)
        self.setup_file_loc.grid_forget()

        self.setup_csv_radio = tk.Radiobutton(self, text="From CSV", pady=5, 
                                                value=1, variable=self.setup_radio_choice, command=lambda: self.setup_process_radio(self.setup_file_loc))
        self.setup_csv_radio.grid(row=0, column=1)

        self.setup_sheets_radio = tk.Radiobutton(self, text="From Google Sheets", pady=5,
                                                     value=2, variable=self.setup_radio_choice, command= lambda: self.setup_process_radio(self.setup_file_loc))
        self.setup_sheets_radio.grid(row=0, column=2)


        self.setup_label2 = tk.Label(self, text="Source for CSV : ")
        self.setup_label2.grid(row=1, column=0) 

        self.setup_upload_button = tk.Button(self, text="Upload CSV", command=self.setup_on_upload)
        self.setup_upload_button.grid(row=1, column=2)

        ## message details

        self.setup_label3 = tk.Label(self, text="Message type: ", pady=10)
        self.setup_label3.grid(row=3, column=0)

        self.setup_text_radio = tk.Radiobutton(self, text="Text", value=2, variable=self.setup_message_choice, pady=10, command=self.change_message_type)
        self.setup_text_radio.grid(row=3, column=1)

        self.setup_html_radio = tk.Radiobutton(self, text="HTML", value=1, variable=self.setup_message_choice, pady=10, command=self.change_message_type)
        self.setup_html_radio.grid(row=3, column=2)

        self.subject_label = tk.Label(self, text="Enter Subject Line : ")
        self.subject_entry = tk.Entry(self, textvariable=self.subject_line)
        self.subject_label.grid(row=4, column=0)
        self.subject_entry.grid(row=4, column=1, columnspan=2)
        self.subject_entry.bind("<Return>", self.update_subject_line)

        self.message_frame = tk.Frame(self)
        self.setup_text_message = scrolledtext.ScrolledText(self, height=20, width=100)
        self.setup_text_message.grid(row=5, column=0, columnspan=5, stick='nw')
        self.setup_text_message.insert('1.0', self.html_message.get())

        self.setup_text_message.bind("<Return>", self.update_message_content)

        self.config.set_message_content(self.html_message.get())
        print("Done")
        

    def update_subject_line(self, event):
        print("Updated: Subject : {}".format(self.subject_line.get()))
        self.config.set_subject_line(self.subject_line.get())
        

    def update_message_content(self, event):
        self.config.set_message_content(self.setup_text_message.get("1.0", "end"))
        

    def setup_process_radio(self, w):
        # print("here")
        # print(w)
        if self.setup_radio_choice.get() == 1 :
            self.setup_label2['text'] = "Source for CSV"
            self.setup_file_loc.grid_forget()
            self.setup_upload_button.grid(row=1, column=2)
            self.config.set_input_type("csv")
        else:
            self.setup_label2['text'] = "Source for Google Sheets"
            self.setup_file_loc.grid(row=1, column=2)
            self.setup_upload_button.grid_forget()
            self.config.set_input_type("google-sheets")


    def setup_on_upload(self):
        file = filedialog.askopenfile()
        print(file.name)
        # self.setup_path_to_csv.set(file.name)
        self.config.set_source_csv(file.name)

    def change_message_type(self):
        # print(self.setup_message_choice.get())
        if self.setup_message_choice.get() == 1:
            ### html
            print("in html  {}".format(self.html_message.get()))
            self.setup_text_message.delete("1.0", "end")
            self.setup_text_message.insert('1.0', self.html_message.get())
            self.config.set_message_type("html")
            self.config.set_message_content(self.html_message.get())

        else:
            self.setup_text_message.delete("1.0", "end")
            self.setup_text_message.insert('1.0', self.text_message.get())
            self.config.set_message_type("text")
            self.config.set_message_content(self.text_message.get())

        print(self.setup_text_message.get("1.0", "end"))
