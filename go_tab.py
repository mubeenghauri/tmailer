import logging
import queue
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.scrolledtext as scrolledtext
from email_handler import ThreadedEmaler
from utils.custom_dialogs import GeneralDialog, ConfigDialog

class QueueHandler(logging.Handler):
    """Class to send logging records to a queue

    It can be used from different threads
    """

    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(record)


class GoTab(tk.Frame):
    def __init__(self, master, config):
        tk.Frame.__init__(self, master)
        self.config = config
        self.master = master
        self.source = tk.StringVar()

        self.config_frame = tk.Frame(self, width=150, height=150, borderwidth=5, relief="sunken")
        self.config_frame.grid(row=0, column=0)
        self.config_frame.grid_columnconfigure(0, weight = 1)
        self.config_frame.grid_rowconfigure(0, weight = 1)
    
        self.heading = tk.Label(self.config_frame, text="Configurations: ")
        self.heading.grid(row=0, column=2, sticky="nswes")

        self.go_button = tk.Button(self, text="GO!", command=self.init)
        self.go_button.grid(row=5, column=3, sticky="nswe")

        self.DEBUG = tk.IntVar()
        self.DEBUG.set(0)
        self.test_checkbox = tk.Checkbutton(self.config_frame, text="DEBUG", variable=self.DEBUG )
        self.test_checkbox.grid(row=6, column=2)
       
        self.log_frame = ttk.Frame(self, width=100, heigh=100, padding=(3, 3, 12, 12))
        self.log_frame.grid(row=1, column=0, sticky="swe")

        self.st = scrolledtext.ScrolledText(self.log_frame, state='disabled', width=100, height=16)
        self.st.configure(font='TkFixedFont')
        self.st.grid(column=2, row=1, sticky='nse', columnspan=6)

        #Create textLogger
        self.log_queue = queue.Queue()
        self.queue_handler = QueueHandler(self.log_queue)
        # Logging configuration
        logging.basicConfig(filename='logs.log',
            level=logging.INFO, 
            format='%(asctime)s - %(levelname)s - %(message)s')        

        # Add the handler to logger
        logger = logging.getLogger()        
        logger.addHandler(self.queue_handler)
        self.log_frame.after(20, self.poll_log_queue)

    def display(self, record):
        try:
            msg = self.queue_handler.format(record)
            self.st.configure(state='normal')
            self.st.insert(tk.END, msg + '\n', record.levelname)
            self.st.configure(state='disabled')
            # Autoscroll to the bottom
            self.st.yview(tk.END)
        except tk.TclError:
            print("[ERROR LOGGING] {}".format(record))

    def poll_log_queue(self):
        # Check every 100ms if there is a new message in the queue to display
        while True:
            try:
                record = self.log_queue.get(block=False)
            except queue.Empty:
                break
            else:
                self.display(record)
        self.log_frame.after(25, self.poll_log_queue)

    def init(self):
        logging.info("Initiated")
        logging.info("~ [CONFIG] ~")
        logging.info("[*] Input Type : {}".format(self.config.input_type))
        logging.info("[*] Input Source : {}".format(self.config.source_csv))
        logging.info("[*] Message Type : {}".format(self.config.message_type))
        logging.info("[*] Message Content : {}".format(self.config.message_content))
        logging.info("[*] Subject Line : {}".format(self.config.subject_line))
        logging.info("[*] DEBUG : {}".format(self.DEBUG.get()))
        logging.info("~ [CONFIG] ~")

        config = {
            "input_type": self.config.input_type,
            "source_csv": self.config.source_csv,
            "message_content": self.config.message_content,
            "message_type": self.config.message_type,
            "subject": self.config.subject_line,
            "debug": self.DEBUG.get()
        }
        
        # tells us if the user accepted or rejected the config displayed
        status = ConfigDialog(self, config=config).get_status()

        if status:
            print("status okay")
            if self.config.source_csv == "":
                GeneralDialog(self.master, title="Warning", message="[WARRNING] NO PATH SUPPLIED FOR TARGET EMAILS !") 
                return
            elif self.config.subject_line == "":
                GeneralDialog(self.master, title="Warning", message="[WARRNING] NO Subject Line GIVEN !")
                return
            else:
                emailer = ThreadedEmaler(self.config.message_content, self.config.subject_line,  self.DEBUG.get()) 
                emailer.load_emails()
                emailer.load_target_emails(self.config.source_csv)
                emailer.start()
