from Notification import Notification

class SecurityNotification(Notification):
    def __init__(self, severity, client,cust, server, tech, link):
        Notification.__init__(self, client,cust, server, tech, link)
        self.severity = severity

        st = "Hi, I found a"
        if self.severity == 'Important':
            st += "n "
        st+= f"{self.severity} security Update On \n"
        st += self.link
        st += f"\nThe Update is for {self.tech}"
        st += "\nGo Check It Out, it emplies to "
        st += f"{self.client} at {self.cust} enviorment, on {self.server}"

        self.text = st


    def __repr__(self):
        return f'{self.severity} security' + Notification.__repr__(self)

    def makeSubject(self):
        return f'{self.severity} Security Update ,App:<{self.client}> at Cust:<{self.cust}>  Server:<{self.server}> Component:<{self.tech}> (p-1)'
