# CentOS Security Update Checker
this project is my own version of windows update for Linux systems. 

## Description
The code checks the official site of CentOS operating system and notifies by email about the Critical and Important Security Updates for CentOS Linux.


Using SMTP protocol for sending emails from a GMAIL server and requesting data form the CentOS Official site.

### Prerequisites

the program use several public libraries:

json, datetime, calendar, sqlite3, re

And some that should be download to the machine

smmtplib , ssl, requests

```bash
pip install requests
```
##installation
runing the program is used in the Linux terminal
```bash
python3 /path-to-dir/Main.py
``` 

##Usage
using the crontab function to run it daily,
```bash
crontab -e

0 8 * * * python3 /path-to-dir/Main.py
```
these are the main classes that are been used in the project
```python
import SendEmail 
import runToWebsite 
```
SendEmail - opens a smtp server connection to GMAIL and sends emails
runToWebsite - checks the official website for updates 

**Before Using**
1. at SendEmail change the password and addresses to your own.
2. use the "rpm -qa" on your CentOS to get the Tech-List installed 
3. at userInput.Json fill the details to your own

## Authors
 **Ido Ziv**
