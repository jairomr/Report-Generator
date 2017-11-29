#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Configuração da pasta do sistema report
"""
path="C:/Relatorio/"

"""
Cofiguração de envio de email
"""
emails=['contao@jairomr.com.br']
subject='Tanguro towers - Status report'
smtp_server = 'smtp.gmail.com'
smtp_user   = 'myemail@gmail.com'
smtp_pass   = ''
strFrom = 'myemail@gmail.com'



"""
Conteudo do Report
"""
imgs=[
	{'img':'gf1.jpg','cid':'image1'},
	{'img':'gf2.jpg','cid':'image2'},
]

"""
Ftp config
"""
ftpGetFiles=[
	{
	  'host':'192.168.1.11',
	  'user':'userftp',
	  'pass': 'passftp',
	  'port':'21',
	  'path':'Met_Tool/EddySoft/Eddydata/'
	  },
	{
	  'host':'192.168.1.12',
	  'user':'userftp',
	  'pass': 'passftp',
	  'port':'21',
	  'path':'MET_TOOL/EddySoft/EDDYDATA/'
	 },
	{
	  'host':'192.168.1.13',
	  'user':'userftp',
	  'pass': 'passftp',
	  'port':'21',
	  'path':'MET_TOOL/EddySoft/EDDYDATA/'
	},
]

"""
Configuração de tentativas de conexão
"""
waitingTime=60#Time for next second attempt
numberAttempts=120#Number of attempts




