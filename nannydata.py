#!/usr/bin/python
#Using input data this script will monitor for new occurances and email intelligence to a specifice sender
#Last Updated: 26-11-2014
#Author: Ben McDowall 
#Requirements: Python 2.x
#
#See usage for help on arguments
#

__author__ = 'Ben McDowall'
import os, sys, shutil, time, logging, getpass, getopt, sqlite3
from urlparse import urlparse
from email.mime.text import MIMEText
from subprocess import Popen, PIPE

fromaddr = "sitenanny@example.com"
toaddr = "alertinbox@example.com"

logfile = "logger.log"

#Set up the logger
user = getpass.getuser()
logger = logging.getLogger('domainnanny')
hdlr = logging.FileHandler(logfile)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s '+user+' %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)

logger.debug("Script Started")

def processfile(filename, sitename):
#connect to DB - create one if it does not exist
	logger.debug("Opening database "+"dbs/"+sitename+".db")
	conn = sqlite3.connect('dbs/'+sitename+'.db')
	c = conn.cursor()

	# Create table if not exists
	c.execute('''CREATE TABLE if not exists domains
             (domain text)''')

	myarray = []
	msgstring = ""
	counter = 0
	newcounter = 0 
	print(filename)
	#Cut file up and extract all domains
	with open(filename) as f:

		for line in f:
			a_split = line.split(';')
			parsed_uri = urlparse( a_split[0] )
			domain = '{uri.netloc}'.format(uri=parsed_uri)
	
			if domain:
				if not domain in myarray:
					c.execute("SELECT * FROM domains where domain=?", (domain,))
					conn.commit()				
					counter+=1
					#if we didnt find this entry in the database, enter it and build a string for the email notification
					if len(c.fetchall()) == 0:
						c.execute("INSERT into domains (domain) VALUES (?)", (domain,))
					        conn.commit()
						newstring = "NEW: "+str(domain)+"\r\n"
						#print newstring
						msgstring += newstring
						newcounter+=1
				
					        myarray.append(domain)
						logger.debug("Unique domain found "+domain)

	if newcounter > 0:
		logger.info(str(newcounter)+" new domains found attempting to send email")
		msg = MIMEText(msgstring)
		msg["From"] = fromaddr
		msg["To"] = toaddr
		msg["Subject"] = "Site Nanny, new domains on "+sitename
		p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
		p.communicate(msg.as_string())	
	


#go through all domains see if they are in the database
#if new send email including detail of what URL they appear on
#add new domain to the database


###############################
# o == option
# a == argument passed to the o
###############################
# Cache an error with try..except 
# Note: options is the string of option letters that the script wants to recognize, with 
# options that require an argument followed by a colon (':') i.e. -i fileName
#
try:
    myopts, args = getopt.getopt(sys.argv[1:],"t:s:f:")
except getopt.GetoptError as e:
    print (str(e))
    print("Usage:  ./nannydata.py -t domain -s sitename -f <filename>")
    print("\t-f <filename> the filename to process")
    logger.error("Couldn't Run "+str(e))
    sys.exit(2)

#Determine the switches being used 
for o, a in myopts:
    logger.debug(o+" "+a)
    if o == '-t':
        mytype=a
    elif o == '-f':
        givenfile=a
    if o == '-s':
        sitename=a

if mytype=="domain":
	logger.info("Reading file "+givenfile)
	processfile(givenfile, sitename)


