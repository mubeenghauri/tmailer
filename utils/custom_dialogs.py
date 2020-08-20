#
# Custom Dialog Boxses
#
import tkinter as tk
from tkinter.simpledialog import Dialog

class GeneralDialog(Dialog):
    """ A generic Dialog to display given messages """
    
    def __init__(self, parent, title="Tmailer", message=""):
        self.message = message
        Dialog.__init__(self, parent, title)

    
    def body(self, master):
        tk.Label(master, text=self.message).pack()


class ConfigDialog(Dialog):
    """ Custom Dialog box to show configurations """

    def __init__(self, parent, title="Configurations", config=None):
        self.configuration = config
        self.status = False
        Dialog.__init__(self, parent, title)


    def body(self, master):
        """ Overiding method """
        tk.Label(master, text="Debug = {}".format(self.configuration["debug"])).pack()
        tk.Label(master, text="Input Type = {}".format(self.configuration["input_type"])).pack()
        tk.Label(master, text="Input Source = {}".format(self.configuration["source_csv"])).pack()
        tk.Label(master, text="Message Type = {}".format(self.configuration["message_type"])).pack()
        tk.Label(master, text="Subject = {}".format(self.configuration["subject"])).pack()
        tk.Label(master, text="Message Content = {}".format(self.configuration["message_content"])).pack()
        
    def ok(self, event=None):
        """ Overiding method, its the same, except it return true """
        self.withdraw()
        self.update_idletasks()
        self.status = True 

        try: 
            self.apply()
        finally:
            self.cancel()

    def get_status(self):
        return self.status

if __name__ == "__main__":

    # GeneralDialog(None, message="Hey there ;)")
    
    SimpleDialog(None, "Is this simple enough? ", ['OK']).go()