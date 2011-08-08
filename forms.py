# !/usr/bin/env python
# -*- coding: UTF-8 -*-
import web
from web import form


db = web.database(dbn='postgres', host='localhost',db='fginfo-deckel', user='fginfo',pw='fginfo')



def editform(mode,values):
	if mode=='editprodukt':
		for i in values:
			f= form.Form(
					form.Hidden('id',value=i.id),
					form.Hidden('values',value=i),
					form.Textbox('bezeichnung',form.notnull,description='Produktbezeichnung: ',value=i.bezeichnung),
					form.Textbox('einkaufspreis',form.notnull,description='Einkauspreis: ',value=i.einkaufspreis),
		        	        form.Textbox('verkaufspreis',form.notnull,description='Verkaufspreis: ',value=i.verkaufspreis)
				    )
			return f
	elif mode=='editdeckel':
		for i in values:
			f=form.Form(
					form.Hidden('mode',value=mode),
					form.Textbox('nachname',form.notnull,description='Nachname: ',value=i.nachname),
					form.Textbox('vorname',form.notnull,description='Vorname: ',value=i.vorname),
					form.Textbox('email',form.notnull,description='Email: ',value=i.email),
					form.Textarea('adresse',form.notnull,description='Adresse: ',value=i.adresse),
					form.Textbox('buchungsfaktor',form.notnull,description='Rabatt: ',value=i.buchungsfaktor),
					form.Checkbox('einkaufsdeckel',checked=i.einkaufspreis,value=True,description='Einkaufspreis: '),
					form.Textbox('kredit',form.notnull,description='Kredit: ',value=i.kredit)
				    )
			return f
	else:
		return None


def newform(mode):
	if mode=='newprodukt':
		f=form.Form(
				form.Hidden('mode',value=mode),
				form.Textbox('bezeichnung',form.notnull,description='Produktbezeichnung: '),
				form.Textbox('einkaufspreis',form.notnull,description='Einkauspreis: '),
		                form.Textbox('verkaufspreis',form.notnull,description='Verkaufspreis: ')
			    )
		return f
	elif mode=='newdeckel':
		f=form.Form(
				form.Hidden('mode',value=mode),
				form.Textbox('nachname',form.notnull,description='Nachname: '),
				form.Textbox('vorname',form.notnull,description='Vorname: '),
				form.Textbox('email',form.notnull,description='Email: '),
				form.Textarea('adresse',form.notnull,description='Adresse: '),
				form.Textbox('buchungsfaktor',form.notnull,description='Rabatt: '),
				form.Checkbox('einkaufsdeckel',checked=False,value=True,description='Einkaufspreis: '),
				form.Textbox('kredit',form.notnull,description='Kredit: '),
			    )
		return f

	elif mode=='einzahlung':
		        tmp = db.query('SELECT * from deckelbesitzer')
			besitzer=[]
			for i in tmp:
				besitzer +=  [i.id,''+i.vorname+' '+ i.nachname],
			f=form.Form(
			form.Dropdown('id',besitzer,description='Deckelbesitzer: '),
			form.Textbox('summe',form.notnull,description='Summe: ')
			)
			return f
	else:
		return None
