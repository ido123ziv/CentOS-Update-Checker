from SecurityNotification import SecurityNotification
import SendEmail
import runToWebsite
from message import Message
import re
import json
import sqlite3
from datetime import *
from pathlib import Path


dirOfProject = Path(__file__).resolve().parent



def getCurrentUNIXTime():
    return datetime.utcnow().strftime("%s")

'''find file path on server'''
userInput = dirOfProject / "userInput.json"
dbFilePath = dirOfProject / 'notification.db'
dbFile = str(dbFilePath)

'''connect to db'''
conn = sqlite3.connect(dbFile)
# conn = sqlite3.connect('notification.db')
c = conn.cursor()
'''
the initial creation of the DB
c.execute("""CREATE TABLE IF NOT EXISTS notifications(
        client TEXT,
        cust TEXT,
        server TEXT,
        tech TEXT,
        link TEXT,
        text TEXT,
        time TEXT)
        """)

c.execute("""CREATE TABLE IF NOT EXISTS updates(
        severity TEXT,
        type TEXT,
        tech TEXT,
        link TEXT,
        date INTEGER)
        """)

c.execute("""CREATE TABLE IF NOT EXISTS lastfiles(
        line TEXT,
        time INTEGER)
        """)
with conn:
    c.execute("INSERT INTO lastfiles VALUES (:line, :time)",
                  {'line': "CESA-2019:2836 Important CentOS 7 dovecot Security Update ", 'time': 1569693397})
'''

'''add a line to the table'''


def insertToDB(n):
    with conn:
        c.execute("INSERT INTO notifications VALUES (:client, :cust, :server, :tech, :link, :text, :time)",
                  {'client': n.client, 'cust': n.cust, 'server': n.server, 'tech': n.tech, 'link': n.link,
                   'text': n.text, 'time': n.time})
        conn.commit()


'''check if we already added to db'''


def ifInDatabase(n):
    with conn:
        c.execute("SELECT * FROM notifications WHERE tech=:tech AND link=:link AND cust=:cust",
                  {'tech': n.tech, 'link': n.link, 'cust': n.cust})
        b = c.fetchall()
        if not b:
            return False
    return True


def insertNewUpdate(severity, type, tech, link, date):
    with conn:
        c.execute("INSERT INTO updates VALUES (:severity, :type, :tech, :link, :date)",
                  {'severity': severity, 'type': type, 'tech': tech, 'link': link, 'date': date})
        conn.commit()

def getlatestUpdates(week_ago):
    output_list = []
    with conn:
        c.execute("SELECT * FROM updates WHERE severity=:s AND date>:date",
                  {'s': "Critical", 'date': week_ago})
        b = c.fetchall()
        output_list.append(b)
        c.execute("SELECT * FROM updates WHERE severity=:s AND date>:date",
                  {'s': "Important", 'date': week_ago})
        b = c.fetchall()
        output_list.append(b)
        c.execute("SELECT * FROM updates WHERE type=:s AND date>:date",
                  {'s': "OS", 'date': week_ago})
        b = c.fetchall()
        output_list.append(b)
        c.execute("SELECT * FROM updates WHERE type=:s AND date>:date",
                  {'s': "CentOS6", 'date': week_ago})
        b = c.fetchall()
        output_list.append(b)
        return output_list


def getlastFiles():
    with conn:
        c.execute("SELECT * FROM lastfiles")
        return c.fetchall()

def updateLast(line, time):
    with conn:
        c.execute("UPDATE lastfiles SET line=:line, time=:time", {'line': line, 'time': time})


def getReleventForTheEmail():
    with conn:
        c.execute("SELECT * FROM lastfiles")
        b = c.fetchall()
        txt = b[0]
        d = b[1]
        c.execute("SELECT * FROM updates WHERE date=:date",
                  {'date': d})
        e = c.fetchall()
        return e


conn.commit()

'''initializing all the list by their priority'''
listOfUpdates = runToWebsite.getMeTheUpdates()
minorSecUpdates = []
criticalUpdates = []
ImportantUpdates = []
OSUpdates = []
NONRelevent = []
UNIXtime =  getCurrentUNIXTime()


'''open configuration file'''
with open(userInput, 'r') as jdata:
    raw_data = json.load(jdata)


'''makes a list of all Notifications that need to be made from the website'''
def makeNotificationsList(listOfImportantSecurityUpdates):
    listOfNotifications = []
    for i in listOfImportantSecurityUpdates:
        for j in raw_data:
            mnn = {}
            di = i['split']
            if di[4] in j['Tech']:
                n = SecurityNotification(di[1], j['client'], j['Cust'], j['Server'], di[4], i['url'])
                mnn['Notification'] = n
                m = Message(j['recipent'], n.makeSubject(), n.text)
                mnn['messege'] = m
                listOfNotifications.append(mnn)
    return listOfNotifications

def checkforReleventInConfig(tech):
    j = raw_data[0]
    return tech in j['Tech']


def addToDBnewUpdates():
    for i in criticalUpdates:
        if checkforReleventInConfig(i['tech']):
            insertNewUpdate("Critical", "Security", i['tech'], i['url'], UNIXtime)
    for i in ImportantUpdates:
        if checkforReleventInConfig(i['tech']):
            insertNewUpdate("Important", "Security", i['tech'], i['url'], UNIXtime)
    for i in OSUpdates:
        if checkforReleventInConfig(i['tech']):
            insertNewUpdate("none", "OS", i['tech'], i['url'], UNIXtime)
    for i in NONRelevent:
        insertNewUpdate("nonissue", "CentOS6", i['tech'], i['url'], UNIXtime)

''' returns a list of dictionaris that fit our description'''
def checkForUpdatesOnSite():
    listOfSecurityUpdates = []
    for i in listOfUpdates:
        if re.search(".*OS 7", i['update']):
            if re.search(".*Security*.", i['update']):
                splited = i['update'].split()
                i['split'] = splited
                i['tech'] = splited[4]
                listOfSecurityUpdates.append(i)
            else:
                splited = i['update'].split()
                i['split'] = splited
                i['tech'] = splited[3]
                OSUpdates.append(i)
        else:
            splited = i['update'].split()
            i['split'] = splited
            x = splited.index('6') +1
            i['tech'] = splited[x]
            NONRelevent.append(i)
    for i in listOfSecurityUpdates:
        if re.search("Critical", i['update']):
            criticalUpdates.append(i)
        elif re.search("Important", i['update']):
            ImportantUpdates.append(i)
        else:
            minorSecUpdates.append(i)
    addToDBnewUpdates()


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
    if datetime.now().day % 6 == 0:
        if time(9, 00) < datetime.now().time() < time(19, 00):
            return True
    return False


def techSender():
    newlist = []
    for i in listOfUpdates:
        newlist.append(i['update'])
    return "\r\n".join(newlist)


def getUpdateNumber(update):
    splited = update.split()
    raw = splited[0]
    x = raw.index(":") + 1
    return raw[x:]


def getListOfUpdateNums(lis):
    new_lis = []
    for i in lis:
        new_lis.append(getUpdateNumber(i['update']))
    return new_lis


def getListOfUpdatesUpdated():
    lastline = getlastFiles()
    l1 = lastline[0]
    lastlinesplited = getUpdateNumber(l1[0])
    if listOfUpdates:
        balagan = getListOfUpdateNums(listOfUpdates)
        if lastlinesplited in balagan:
            x = balagan.index(lastlinesplited) + 1
            new_list = listOfUpdates[x:]
            nt = UNIXtime
            if new_list:
                lastItem = new_list[-1]
                updateLast(lastItem['update'],nt)
                return new_list
            else:
                return []
        else:
            return listOfUpdates
    return []


listOfUpdates = getListOfUpdatesUpdated()

def cleaner(mess):
    new_lis = []
    for l in mess:
        new_lis.append(l[2])
    return new_lis

def sendweeklyUpdate(ur):
    week_ago = datetime.today() - timedelta(days=7)
    week_ago = week_ago.strftime("%s")
    updatelist = getlatestUpdates(week_ago)
    SendEmail.Alive(ur,cleaner(updatelist[0]),cleaner(updatelist[1]),cleaner(updatelist[2]),cleaner(updatelist[3]))


def MoneyMaker():
    ur = runToWebsite.getMonthUrl()
    SendEmail.SendEmailToido(ur)
    checkForUpdatesOnSite()
    # start = ImportantUpdates + criticalUpdates
    start = criticalUpdates
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
        if listOfUpdates:
            lastLineDict = listOfUpdates[-1]
            newlastLine = lastLineDict['update']
            with open(lastLine, 'w+') as saver:
                saver.write(newlastLine)
        sendweeklyUpdate(ur)


MoneyMaker()


conn.close()
