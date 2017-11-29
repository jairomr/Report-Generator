#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This is a awesome
        python script!"""


# Import smtplib to provide email functions

# Send an HTML email with an embedded image and a plain text message for
# email clients that don't want to display the HTML.

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from datetime import datetime
import smtplib
from smtplib import SMTP_SSL
import configemail as config
import json


path=config.path
opneFileHTML = json.load(open(path+'openFileHTML.json'))


# Create the root message and fill in the from, to, and subject headers
msgRoot = MIMEMultipart('related')
msgRoot['Subject'] = config.subject
msgRoot['From'] = config.strFrom

msgRoot.preamble = 'This is a multi-part message in MIME format.'

# Encapsulate the plain and HTML versions of the message body in an
# 'alternative' part, so message agents can decide which they want to display.
msgAlternative = MIMEMultipart('alternative')
msgRoot.attach(msgAlternative)

msgText = MIMEText('This is the alternative plain text message.')
msgAlternative.attach(msgText)

# We reference the image in the IMG SRC attribute by the ID we give it below

reportTime=str(open(path+"reportTime", "r").read())
NetworkError=str(open(path+"erroSys.html", "r").read())
reportHtml=str(open(path+opneFileHTML['body'], "r").read()).replace('%REPORTTIME%',reportTime).replace('%NetworkError%',NetworkError)




msgText = MIMEText(reportHtml, 'html')
msgAlternative.attach(msgText)

def sendEmailTo(toEmail,numError):
	try:
		print 'Send '+str(datetime.now())+" "+toEmail
		smtp = SMTP_SSL(smtp_server,465)
		smtp.login(smtp_user, smtp_pass)
		smtp.sendmail(config.strFrom, toEmail, msgRoot.as_string())
		smtp.quit()
	except Exception as e:
		if (numError<config.numberAttempts):
			print("There was an error sending the email. Check the smtp settings.\n"+str(e))
			time.sleep(config.waitingTime)
			sendEmailTo(toEmail)

def setImage(img,cid):
	# This example assumes the image is in the current directory
	fp = open(path+img, 'rb')
	msgImage = MIMEImage(fp.read())
	fp.close()

	# Define the image's ID as referenced above
	msgImage.add_header('Content-ID', '<'+cid+'>')
	msgRoot.attach(msgImage)
	pass
if(opneFileHTML['error']!=True):
	for img in config.imgs:
		setImage(img['img'],img['cid'])
		pass


smtp_server = config.smtp_server
smtp_user   = config.smtp_user
smtp_pass   = config.smtp_pass
# Send the email (this example assumes SMTP authentication is required)

toEmails=config.emails

for toEmail in toEmails:
	msgRoot['To'] = toEmail

for toEmail in toEmails:
	sendEmailTo(toEmail,0)

