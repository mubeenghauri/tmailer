import os

class EmailSheetHandler:

    def __init__(self, filename="email.csv"):
        self.filename = filename

    def file_exists(self, file):
        return os.path.exists(file)
    
    def isCSV(self, file):
        # print("[isCSV] "+file+" : ", ("csv" in file))
        return "csv" in file

    def append_to_file(self, data):
        if len(data) != 3: 
            print("[append to file] data given is corrupted")
            return False
        
        with open(self.filename, 'a') as w:
            w.write(",".join(data)) 
        
        print("[append to file] Appended to file '{}' !!".format(",".join(data)))
        return True
    
    def update_email_file(self, data):
        if type(data) != list or type(data[0]) != list:
            print("[Update Email List] Data given should be a list of list")
            return False
        
        with open(self.filename, 'w') as w:
            for i in data:
                print("Writing ", i)
                w.writelines(",".join(i)+"\n")
        
        print("[Update Email List] Done !")
        return True

    def merge_with_emails(self, file):
        L = []
        with open(file, 'r') as f:
            L = f.readlines()
        d = self.get_email_file_contents()

        for i in L: d.append(i)
        self.update_email_file(d)
        print("[Merge with Emails] Done Merging !!")
        return True
        
    def get_email_file_contents(self):
        with open(self.filename, 'r') as f:
            return f.readlines()

    def get_processed_email(self):
        L = self.get_email_file_contents()
        return [i.strip("\n").split(",") for i in L]

    def validate(self, file):
        # performs all checks
        print(file)
        if self.file_exists(file) and self.isCSV(file):
            return True
        return False