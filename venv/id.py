from SecurityNotification import SecurityNotification
import SendEmail
import runToWebsite
from message import Message
import re
import json
import sqlite3
from datetime import datetime, time

conn = sqlite3.connect('notification.db')
c = conn.cursor()


def insertToDB(n):
    with conn:
        c.execute("INSERT INTO notifications VALUES (:client, :cust, :server, :tech, :link, :text, :time)",
                  {'client':n.client, 'cust':n.cust, 'server': n.server, 'tech':n.tech, 'link':n.link, 'text':n.text, 'time':n.time})

def ifInDatabase(n):
    with conn:
        c.execute("SELECT * FROM notifications WHERE tech=:tech AND link=:link", {'tech': n.tech, 'link': n.link})
        b = c.fetchall()
        if not b:
            return False
    return True

conn.commit()

listOfUpdates = runToWebsite.getMeTheUpdates()

''' returns a list of dictionaris that fit our description'''
def checkForUpdatesOnSite():
    listOfSecurityUpdates = []
    for i in listOfUpdates:
        if re.search("Important.*7.*Security", i['update']) or re.search("Critical.*7.*Security", i['update']):
            splited = i['update'].split()
            i['split'] = splited
            listOfSecurityUpdates.append(i)
    return listOfSecurityUpdates

ido = checkForUpdatesOnSite()

with open('userInput.json', 'r') as jdata:
    raw_data = json.load(jdata)

def makeNotificationsList(listOfSecurityUpdates):
    listOfNotifications = []
    for i in listOfSecurityUpdates:
        for j in raw_data:
            mnn = {}
            di = i['split']
            if di[4] in j['Tech']:
                n = SecurityNotification(di[1],j['client'],j['Cust'],j['Server'],di[4],i['url'])
                mnn['Notification'] = n
                m = Message(j['recipent'],n.makeSubject(),n.text)
                mnn['messege'] = m
                listOfNotifications.append(mnn)
    return listOfNotifications

def checkReleventInDB(relevent):
    forsend = []
    for i in relevent:
        ido = ifInDatabase(i['Notification'])
        if not ido:
            forsend.append(i)
    return forsend

def addNewToDB(saves):
        for i in saves:
            insertToDB(i['Notification'])

def sendEmailsOfRelevent(relevent):
        for i in relevent:
            SendEmail.sendMessage(i['messege'])

def AliveMaterial():
        if datetime.now().day % 7 == 0:
            if datetime.now().time() > time(9, 00) and datetime.now.time() < time(17, 00):
                return True
        return False

def MoneyMaker():
        start = checkForUpdatesOnSite()
        cond1 = not start
        if not cond1:
            next = makeNotificationsList(start)
            cond1 = not next
            if not cond1:
                filtered = checkReleventInDB(next)
                cond1 = not filtered
                if not cond1:
                    addNewToDB(filtered)
                    sendEmailsOfRelevent(filtered)
        alive = AliveMaterial()
        if alive:
            sendEmail.Alive()


MoneyMaker()

conn.close()


