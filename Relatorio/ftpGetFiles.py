#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This is a awesome
        python script!"""

from ftplib import FTP
import re
import os
import csv
import subprocess
import time
from datetime import datetime 
import configemail as config
#import MultiFTP as MultiFTP

def limparFiles():
	r=re.compile(".*\.csv")
	jpg=re.compile(".*\.jpg")
	allFile=os.listdir(config.path)
	files=filter(r.match, allFile)
	filesJPG=filter(jpg.match, allFile)
	for file in files:
		os.remove(config.path+file)
		
	for file in filesJPG:
		os.remove(config.path+file)

def getFileFTP(host,port,user,password,pasta,numError):
	r = re.compile(".*\.csv")
	try:
		ftp = FTP() 
		ftp.connect(host,port)    # connect to host, default port
		ftp.login(user,password) 
		ftp.cwd(pasta)
		files=ftp.nlst()
		file = filter(r.match, files)
		for f in file:
			getFile(ftp,f,0)
		#MultiFTP
	except :
		if (numError<config.numberAttempts):
			print str(datetime.now())+" Tentativa rede "+str(numError)
			time.sleep(config.waitingTime)
			getFileFTP(host,port,user,password,pasta,numError+1)
	

def getFile(ftp, filename,numError):
    try:
    	print str(datetime.now())+' save file '+config.path+filename
        ftp.retrbinary("RETR " + filename ,open(config.path+filename, 'wb').write)
    except:
        if (numError<config.numberAttempts):
			print str(datetime.now())+" Tentativa file "+str(numError)
			time.sleep(config.waitingTime)
			getFile(ftp, filename,numError+1)


limparFiles()
print str(datetime.now())+" baixado dados"


for ftpRota in config.ftpGetFiles:
	print str(datetime.now())+" connect "+ftpRota['port']
	getFileFTP(ftpRota['host'],ftpRota['port'],ftpRota['user'],ftpRota['pass'], ftpRota['path'],0)
	pass



print str(datetime.now())+" Gerando Grafico"
proc = subprocess.call ("Rscript "+config.path+"CreateTorres.R",  shell=True)
proc = subprocess.call ("python "+config.path+"sendEmail.py",  shell=True)
