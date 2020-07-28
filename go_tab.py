import tkinter as tk
import tkinter.ttk as ttk
import tkinter.scrolledtext as scrolledtext
import logging
from email_handler import _Emailer



#https://stackoverflow.com/questions/13318742/python-logging-to-tkinter-text-widget
class TextHandler(logging.Handler):
    # This class allows you to log to a Tkinter Text or ScrolledText widget
    # Adapted from Moshe Kaplan: https://gist.github.com/moshekaplan/c425f861de7bbf28ef06

    def __init__(self, text):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Store a reference to the Text it will log to
        self.text = text

    def emit(self, record):
        msg = self.format(record)
        def append():
            self.text.configure(state='normal')
            self.text.insert(tk.END, msg + '\n')
            self.text.configure(state='disabled')
            # Autoscroll to the bottom
            self.text.yview(tk.END)
        # This is necessary because we can't modify the Text from other threads
        self.text.after(0, append)

class GoTab(tk.Frame):
    def __init__(self, master, config):
        tk.Frame.__init__(self, master)
        self.config = config
        print("hereeee")
        print(self.config.get_input_type())
        ### show config data
        # self.grid_columnconfigure(0, weight = 1)
        # self.grid_rowconfigure(0, weight = 1)
        # print(master.identify())

        self.intyp = tk.StringVar()
        self.intyp.set(self.config.input_type)

        self.config_frame = tk.Frame(self, width=150, height=150, borderwidth=5, relief="sunken")
        self.config_frame.grid(row=0, column=0)
        self.config_frame.grid_columnconfigure(0, weight = 1)
        self.config_frame.grid_rowconfigure(0, weight = 1)
        # main Label
        print(self.config.get_input_type())


        self.heading = tk.Label(self.config_frame, text="Configurations: ")
        self.heading.grid(row=0, column=2, sticky="nswes")

        self.label1 = tk.Label(self.config_frame, text="Input Type: ")
        self.label1.grid(row=1, column=1)
        self.label1v = tk.Label(self.config_frame, textvariable=self.intyp)
        self.label1v.grid(row=1, column=2)

        self.label2 = tk.Label(self.config_frame, text="Source : ")
        self.label2.grid(row=2, column=1)
        self.label2v = tk.Label(self.config_frame, text="")
        self.label2v.grid(row=2, column=2)

        self.label3 = tk.Label(self.config_frame, text="Message Type: ")
        self.label3.grid(row=3, column=1)
        self.label3v = tk.Label(self.config_frame, text="")
        self.label3v.grid(row=3, column=2)

        self.label4 = tk.Label(self.config_frame, text="Message Content: ")
        self.label4.grid(row=4, column=1)

        self.go_button = tk.Button(self, text="GO!", command=self.init)
        self.go_button.grid(row=5, column=3, sticky="nswe")

        self.DEBUG = tk.IntVar()
        self.DEBUG.set(0)
        self.test_checkbox = tk.Checkbutton(self.config_frame, text="DEBUG", variable=self.DEBUG )
        self.test_checkbox.grid(row=5, column=2)

        self.log_frame = ttk.Frame(self, width=100, heigh=100, padding=(3, 3, 12, 12))
        self.log_frame.grid(row=1, column=0, sticky="swe")

        self.st = scrolledtext.ScrolledText(self.log_frame, state='disabled', width=100, height=16)
        self.st.configure(font='TkFixedFont')
        self.st.grid(column=2, row=1, sticky='nse', columnspan=6)


        #Create textLogger
        text_handler = TextHandler(self.st)

        # Logging configuration
        logging.basicConfig(filename='logs.log',
            level=logging.INFO, 
            format='%(asctime)s - %(levelname)s - %(message)s')        

        # Add the handler to logger
        logger = logging.getLogger()        
        logger.addHandler(text_handler)


    def init(self):


        logging.info("Initiated")
        logging.info("~ [CONFIG] ~")
        logging.info("[*] Input Type : {}".format(self.config.input_type))
        logging.info("[*] Input Source : {}".format(self.config.source_csv))
        logging.info("[*] Message Type : {}".format(self.config.message_type))
        logging.info("[*] Message Content : {}".format(self.config.message_content))
        logging.info("[*] DEBUG : {}".format(self.DEBUG.get()))
        logging.info("~ [CONFIG] ~")

        if self.config.source_csv == '':
            logging.warning("[WARRNING] NO PATH SUPPLIED FOR TARGET EMAILS !")
            return

        emailer = _Emailer() 
        emailer.load_emails()
        emailer.load_target_emails(self.config.source_csv)
        emailer.send_mails(self.config.message_content, self.DEBUG)