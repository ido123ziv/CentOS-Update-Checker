import requests
import re
from datetime import datetime
import calendar

url = "https://lists.centos.org/pipermail/centos-announce"
url2 = ""

def findCurrentAddition():
    mmonth = datetime.now().month
    month = calendar.month_name[mmonth]
    year = datetime.now().year
    return "/" + f"{year}" + "-"  +f"{month}"

def getMonthUrl():
    return url + findCurrentAddition() + "/" + "thread.html"


def getUpdateUrl(st):
    return url + findCurrentAddition() + "/" + st

def findUrlMonth():
    monthAddition = findCurrentAddition()
    a1 = "/thread.html"
    return url + monthAddition + a1

def findCurrentMonth():
    mmonth = datetime.now().month
    month = calendar.month_name[mmonth]
    year = datetime.now().year
    a1 =  "/thread.html"
    addition = "/" + f"{year}" + "-" + f"{month}"
    url2 = url + addition
    return url + addition + a1

url1 = findCurrentMonth()
response = requests.get(url1)
text = response.text
lines = text.split('\n')

def findUpdates():
    updates = []
    for line in lines:
        di = {}
        if re.search("CESA", line) or re.search("CEBA", line):
            x = line.find(']') + 1
            st1 = line
            x1 = line.find('=') + 2
            st1 = st1[x1:]
            x2 = st1.find('>') - 1
            st1 = st1[:x2]
            line = line[x:]
            di["update"] = line
            di["url"] = getUpdateUrl(st1)
            updates.append(di)
    return updates

def OnlyRelevent(updates):
    str1 = ""
    for i in updates:
        x = i.index(']')
        str1 +=i[x+1:] + '\n'
    return str1

def getMeTheUpdates():
	return findUpdates()

