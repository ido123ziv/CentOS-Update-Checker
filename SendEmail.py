import smtplib
import ssl
from datetime import *
from message import Message

port = 465
password = "enter-password-here"

context = ssl.create_default_context()
sender_email = "enter-email"
receiver_email = "enter-email"

def sendMessage(message):
    with smtplib.SMTP_SSL("smtp.gmail.com",port,context=context) as server:
        server.login(sender_email,password)
        s = "\r\n".join(["From: sender",
                  	 "To: receiever",
                         f"Subject: {message.subject}",
                         "",
                         message.msg])
        server.sendmail(sender_email,receiver_email,s)

def sendTech(techlist):
    with smtplib.SMTP_SSL("smtp.gmail.com",port,context=context) as server:
        server.login(sender_email,password)
        s = "\r\n".join(["From: sender-email",
                         "To: receiver-email",
                         f"Subject: Updates Available for CentOS",
                         "",
                         techlist])
        #msg1 = s + "\n" + techlist
        server.sendmail(sender_email,"receiver-email",s)


def sendNotification(reciever_email, msg):
    with smtplib.SMTP_SSL("smtp.gmail.com",port,context=context) as server:
        server.login("sender-email",password)
        server.sendmail(sender_email,receiver_email,msg)


def sendAlive(msg):
    with smtplib.SMTP_SSL("smtp.gmail.com",port,context=context) as server:
        server.login(sender_email,password)
        server.sendmail(sender_email,receiver_email,msg)


def strFromList(lis):
    return '\r\n'.join(lis)


def Alive(url, CritSecUpdates, ImpSecUpdates, OSUpdates,NonRelevent):
    csString = strFromList(CritSecUpdates)
    isString = strFromList(ImpSecUpdates)
    oString = strFromList(OSUpdates)
    nString= strFromList(NonRelevent)
    msg = "\r\n".join(["From: sender-email",
	                   "To: reciever-email",
        	           f"Subject: Weekly OS/Security Update Summary Report <{datetime.now().date()}>"
                           "",
                       f"Relevant Critical Security Updates(Total: {len(CritSecUpdates)}):",
                       csString,
                       f"Relevant Important Security Updates(Total: {len(ImpSecUpdates)}):",
                       isString,
                       f"\nRelevant OS Updates(Total: {len(OSUpdates)}):",
                       oString,
                       f"\nNon - Relevant Updates(Total: {len(NonRelevent)}):",
                       nString,
                        "For the complete list of updates:",
                       url])
    sendAlive(msg)

def SendEmailToido(url):
    msg = "\r\n".join(["From: sender-email",
                       "To: reciever-email",
                       f"Subject: CentOS Security Update Checker - Daily Alive Massage"
                       "",
                       "Hi, \nthere are no new CentOS Critical/Important security updates",
                       "you can check it at:\n",
                       url])
    with smtplib.SMTP_SSL("smtp.gmail.com",port,context=context) as server:
        server.login(sender_email,password)
        server.sendmail(sender_email,"check-up-email",msg)