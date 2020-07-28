import time
import logging
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email_sheet_handler import EmailSheetHandler

class Emailer:

    def __init__(self):
        self.emailHandler = EmailSheetHandler()
    
    def load_emails(self):
        self.emails = self.emailHandler.get_processed_email()
        for i in self.emails: logging.info("[Emailer] Got email : {}".format(i))

    def load_target_emails(self, csv):
        L = []
        self.csv = csv
        with open(csv, 'r') as f:
            L = f.readlines()
        self.target_emails = [i.strip('\n').split(",") for i in L]
        for i in self.target_emails: logging.info("[Emailer] Got Target email : {}".format(i))

    def update_file(self, e):
        L = []
        with open(self.csv, "r") as f:
            L = f.readlines()
        x = None
        for i in range(len(L)):
            if e in L[i]:
                print("got line : "+L[i])
                t = L[i].strip('\n')
                t += ", SENT\n"
                L[i] = t
                print("updated i : "+L[i])
                x = i
                break
        print(L[x])
        with open(self.csv, 'w') as f:
            f.writelines(L)

    def send_mails(self, msg, type="html"):

        mail_index = 0
        for creds in self.emails:
            count = 0
            logging.info("[*] Going through : "+creds[0]+" max-mails -> {}".format(creds[2]))
            while count < int(creds[2]):
                logging.info("mail_count = {} & count = {}".format(mail_index, count))
                sender_email = creds[0]
                password = creds[1]
                logging.info("[*] email -> {} pass -> {}".format(sender_email, password))
                current = self.target_emails[mail_index]
                reciever_name = current[0].strip('\n')
                reciever_mail = current[1].strip('\n')
                if reciever_mail == '' or reciever_name == '' or len(reciever_mail) == 0 or len(reciever_name) == 0:
                    mail_index+=1
                    continue
                logging.info("[*] Got mail : {} , name: {}".format(reciever_mail, reciever_name))
                message = MIMEMultipart("alternative")
                message["Subject"] = "Quick Question"
                message["From"] = "Nabeel Ahmad Ghauri"
                message["To"] = reciever_mail

                m = MIMEText(msg.format(reciever_name), 'html')
                print(m)
                message.attach(m)
                context = ssl.create_default_context()
                try:
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
                        server.login(sender_email, password)
                        server.sendmail( sender_email, reciever_mail, message.as_string() )
                        logging.info("Mail Sent to : "+reciever_mail)
                        self.update_file(reciever_mail)
                except Exception as e:
                        logging.exception("message")
                        print("[WARNING] Some exception ....")
                        print(e)
            
                
                count+=1
                mail_index+=1