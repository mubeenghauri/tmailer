import time
import logging
import smtplib, ssl
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
        # self.clean(csv)
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
    def __init__(self, msg, debug):
        Thread.__init__(self)
        _Emailer.__init__(self)
        self.msg = msg 
        self.debug = debug

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
            while count < int(creds[2]):
                logging.info("mail_count = {} & count = {} & sent = {} & already_sent = {} & total_mails= {}".format(mail_index, count, sent_count, already_sent, len(self.target_emails) ))
                current = self.target_emails[mail_index]
                reciever_name = current[0].strip('\n')
                reciever_mail = current[1].strip('\n')
                
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
                message["Subject"] = "Quick Question"
                message["From"] = "Nabeel Ahmad Ghauri"
                message["To"] = reciever_mail

                m = MIMEText(self.msg.format(reciever_name), 'html')
                message.attach(m)
                context = ssl.create_default_context()
                
                if self.debug == 0:
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
                else: 
                    logging.info("[*] Sent to : {}".format(current))
                    time.sleep(2)
                
                count+=1
                mail_index+=1
                sent_count +=1
        logging.info( "[DONE] Finished Sending mails !" )
