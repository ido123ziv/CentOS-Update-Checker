from datetime import datetime
class Notification:


    def __init__(self, client,cust, server, tech, link):
        self.client = client
        self.cust = cust
        self.server =server
        self.tech = tech
        self.link = link
        self.time = datetime.now()
        st = "Hi, I found a CentOS OS Update On \n"
        st += self.link
        st += f"\nThe Update is for {self.tech}"
        st += "\nGo Check It Out, it emplies to "
        st += f"{self.client} at {self.cust} enviorment, on {self.server}"
        st += f"\nUpdate from {self.time}"
        self.text = st

    def getNotificationtText(self):
        st = "Hi, I found a CentOS OS Update On \n"
        st += self.link
        st += f"\nThe Update is for {self.tech}"
        st +=  "\nGo Check It Out, it emplies to "
        st += f"{self.client} at {self.cust } enviorment, on {self.server}"
        st += f"\nUpdate from {self.time}"
        return st

    def getText(self):
        return self.text

    def __repr__(self):
        return f'Update On {self.tech} \nPlease see {self.link} \nemplies to {self.client} at {self.cust} enviorment, on {self.server}'
