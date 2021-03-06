import time
import logging
import datetime
import smtplib, ssl
import requests
from threading import Thread
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email_sheet_handler import EmailSheetHandler

class _Emailer:
    """ Manage sending emails. """
    def __init__(self):
        self.emailHandler = EmailSheetHandler()
    
    def load_emails(self):
        self.emails = self.emailHandler.get_processed_email()
        # for i in self.emails: logging.info("[Emailer] Got email : {}".format(i))

    def clean(self, file):
        with open(file, 'r') as f:
            L = f.readlines()
        cleaned = []
        count = 0
        for i in L:
            l = i.strip("\n").split(",")
            temp = []
            count += 1
            for j in l:
                if len(j) > 2:
                    temp.append(j)
            if len(temp)  >= 2:
                cleaned.append(temp)

        with open(file, 'w') as f:
            for i in cleaned:
                f.writelines(",".join(i)+"\n")

    def load_target_emails(self, csv):
        """ @param csv: path to csv file """
        
        if csv == "" or csv == None:
            raise FileNotFoundError

        L = []
        self.csv = csv
        with open(csv, 'r') as f:
            L = f.readlines()
        self.target_emails = [i.strip('\n').split(",") for i in L]
        # for i in self.target_emails: logging.info("[Emailer] Got Target email : {}, len = {}".format(i, len(i)))

    def update_file(self, e):
        L = []
        with open(self.csv, "r") as f:
            L = f.readlines()
        x = None
        for i in range(len(L)):
            if e in L[i]:
                print("got line : "+L[i])
                t = L[i].strip('\n')
                t += ",SENT\n"
                L[i] = t
                print("updated i : "+L[i])
                x = i
                break
        print(L[x])
        with open(self.csv, 'w') as f:
            f.writelines(L)


class ThreadedEmaler(Thread, _Emailer):
    """ Thread wrapper for Emailer. """
    def __init__(self, msg, subject, debug):
        Thread.__init__(self)
        _Emailer.__init__(self)
        self.msg = msg 
        self.debug = debug
        self.subject = subject

    def notifyApi(self, to, frm, name, date):
        param = {
            "to": to,
            "from" : frm,
            "name" : name,
            "date" : date
        }
        headers = {
            'User-Agent': "TmailerPy/0.1",
            'Accept': "application/json",
            'Cache-Control': "no-cache",
            'Host': "api.jumpstartsol.com",
            'Accept-Encoding': "gzip, deflate",
            'Content-Length': "0",
            'Connection': "keep-alive",
            'cache-control': "no-cache"
        }
        logging.info("[notifyApi] Notifying Api with : {}".format(param))
        r = requests.post('http://api.jumpstartsol.com/api/sent', json=param, headers=headers)
        logging.info("[notifyApi] Response code from api = {}".format(r))
        if r.status_code != 200:
            logging.warning("[notifyApi][WARNING] error in notify request : {}".format(r.text))

    def run(self):
        mail_index = 0
        already_sent = 0
        sent_count = 0
        for creds in self.emails:
            count = 0
            sender_email = creds[0]
            password = creds[1]
            logging.info("[*] Going through : "+creds[0]+" max-mails -> {}".format(creds[2]))
            logging.info("[*] email -> {} pass -> {}".format(sender_email, password))
            while count < int(creds[2]) and mail_index < len(self.target_emails):
                logging.info("mail_count = {} & count = {} & sent = {} & already_sent = {} & total_mails= {}".format(mail_index, count, sent_count, already_sent, len(self.target_emails) ))
                
                try:
                    current = self.target_emails[mail_index]
                    reciever_name = current[0].strip('\n').strip(" ")
                    reciever_mail = current[1].strip('\n').strip(" ")
                except IndexError:
                    logging.warning("[WARNING] invalid entry : {}".format(current))
                    print("[WARNING] invalid entry : {}".format(current))
                    mail_index+=1
                    continue

                if reciever_mail == '' or reciever_name == '' or len(reciever_mail) == 0 or len(reciever_name) == 0 or '@' not in reciever_mail:
                    logging.info("[WARNING] Skipping invalid values : {}".format(current))
                    mail_index+=1
                    continue

                if "SENT" in current or " SENT" in current:
                    print("Already sent")
                    logging.info("[INFO] {} :  already sent".format( reciever_mail))
                    already_sent +=1
                    mail_index+=1
                    continue

                logging.info("[*] Got mail : {} , name: {}".format(reciever_mail, reciever_name))
                message = MIMEMultipart("alternative")
                message["Subject"] = self.subject.format(reciever_name)
                message["From"] = "Nabeel Ahmad Ghauri"
                message["To"] = reciever_mail

                m = MIMEText(self.msg.format(reciever_name, reciever_mail, sender_email, reciever_name, str(datetime.date.today())), 'html')
                message.attach(m)
                context = ssl.create_default_context()
                
                if self.debug == 0:
                    try:
                        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
                            server.login(sender_email, password)
                            server.sendmail( sender_email, reciever_mail, message.as_string() )
                            logging.info("Mail Sent to : "+reciever_mail)
                            self.notifyApi(reciever_mail, sender_email, reciever_name, str(datetime.date.today()))
                            self.update_file(reciever_mail)
                    except Exception as e:
                            logging.exception("message")
                            print("[WARNING] Some exception ....")
                            print(e)
                else: 
                    logging.info("[*] Sent to : {}".format(current))
                    time.sleep(2)
                
                count+=1
                mail_index+=1
                sent_count +=1
                
            if mail_index >= len(self.target_emails): break
        logging.info( "[DONE] Finished Sending mails !" )
