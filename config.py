""" Class to hold all Configurations """

# import logging
# logging.getLogger(__name__)

class Configuration:

    def __init__(self):

        self.input_type = "csv"    # by default
        self.source_csv = ""
        self.message_type = "html" # by default
        self.message_content = "" 
        self.subject_line = "Quick Question"
    
    def set_subject_line(self, s):
        print("[config] subject line updated: "+s)
        self.subject_line = s

    def set_input_type(self, t):
        print("Configuration Updated")
        # logging.info("[CONFIIGURATION][INPUT TYPE] Changed to : {}".format(t))
        self.input_type = t

    def set_source_csv(self, s):
        print("Configuration Updated")
        # logging.info("[CONFIIGURATION] Source csv : {}".format(s))
        self.source_csv = s

    def set_message_type(self, t):
        # logging.info("[CONFIIGURATION] Message type : {}".format(t))

        print("Configuration Updated")

        self.message_type = t

    def set_message_content(self, c):
        # logging.info("[CONFIIGURATION] Message content Changed to : {}".format(c))
        print("Configuration Updated")
        self.message_content = c
    
    def get_input_type(self):
        return self.input_type
    
    def get_source_csv(self):
        return self.source_csv

    def get_message_type(self):
        return self.message_type
    
    def get_message_content(self):
        return self.message_content

    def get_subject_line(self):
        return self.subject_line