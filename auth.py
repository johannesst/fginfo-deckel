# !/usr/bin/env python
# -*- coding: UTF-8 -*-
import web
from web import form
import hashlib


db = web.database(dbn='postgres', host='localhost',db='fginfo-deckel', user='fginfo',pw='fginfo')

class auth:

#        def __init__(self, *inputs, **kw):
        def __init__(self):
		self.authdata = dict(id=None,login=None,isAuthed=False)	
		self.authform = form.Form(
			form.Textbox('login',form.notnull,description='Login: '),
			form.Password('password',form.notnull,description='Passwort: ')
			)

	def isAuthed(self):
		return self.authdata["isAuthed"]

	def getAuthform(self):
		return self.authform


	def getAuth():
		return self.authdata()

	def authenticate(self,login,password):
		hashedpw=hashlib.sha256()
		hashedpw.update(password)
		try:
			dbpasswd = db.query('SELECT * FROM auth WHERE login=$login',vars=dict(login=str(login)))[0]
		except IndexError:
			return False
		else:
			pass
		if dbpasswd['pass'] ==  hashedpw.hexdigest():
			self.authdata['login']    = dbpasswd['login']
			self.authdata['id']       = dbpasswd['id']
			self.authdata['isAuthed'] = True
	 	return self.authdata['isAuthed']

