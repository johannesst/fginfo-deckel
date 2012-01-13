# !/usr/bin/env python
# -*- coding: UTF-8 -*-
import web
from web import form
import forms
import time
import auth
#import hashlib

urls = (
'/', 'main',
'/login','login',
'/deckel','deckel',
'/einzahlung', 'einzahlung',
'/admin', 'admin')
title = "Getränkedeckel FG Informatik"
app = web.application(urls, globals(), autoreload=True)
render = web.template.render('templates/', base='base')
db = web.database(dbn='postgres', host='localhost',db='fginfo-deckel', user='fginfo',pw='fginfo')


def check_guthaben(besitzer,kredit,summe):
	guthaben = db.query('SELECT * FROM guthaben WHERE deckelbesitzer=$deckelbesitzer',vars=dict(deckelbesitzer=str(besitzer)))[0]
	backlink = "/deckel?mode=kasse&id="+str(besitzer)
	#if guthaben['guthaben']-summe< float(kredit):#['guthaben']
	#	return guthaben['guthaben']-summe
	#return render.status(title,"Kasse",str(guthaben['guthaben']-summe),backlink)
	if guthaben['guthaben']-summe <= kredit:
		return render.status(title,"Kasse","Nicht genug Guthaben vorhanden. Der Deckel muss erst aufgeladen werden! ",backlink)
	else:
		return True
class login:
    def GET(self):
    	    a=auth.auth()
	    f=a.authform
	    return render.login(title,"Login",f)
    def POST(self):
	    a=auth.auth()
	    data=web.input()
	    # ausgabe+= "login " + data['login'] + "\n"
	    #ausgabe+="pw " + data['password'] + " " + 	    hashedpw.hexdigest() + "\n"
	    if a.authenticate(data['login'],data['password']):
		    return "Login erfolgreich!"
	    return "Login failt!"

class einzahlung:
   
    def GET(self):
	    i=web.input()
	    backlink=web.input(back='/').back
	    ''' Nur nach Umstricken nach vars benutzen, sonst SQL
	    Injektion!
	    Wird eigentlich eh nicht mehr gebraucht, daher
	    auskommentiert
	    if i:
		    #return web.input()
		    with db.transaction():
	    	            summe=db.query('select summe FROM einzahlungen WHERE deckelbesitzer='+i.delete+" AND time='"+i.time+"'")
			    guthaben=db.query('select guthaben FROM guthaben WHERE deckelbesitzer='+i.delete)
			    guthaben=guthaben[0].guthaben-summe[0].summe
			    db.query('update guthaben set guthaben='+str(guthaben)+ 'WHERE  deckelbesitzer='+i.delete)
	    	            db.query('delete FROM einzahlungen WHERE deckelbesitzer='+i.delete+" AND time='"+i.time+"'")
	    '''
	    f=forms.newform('einzahlung')
	    einzahlungen=db.query('SELECT * FROM deckelbesitzer AS d JOIN einzahlungen AS e ON d.id=e.deckelbesitzer')
	    if einzahlungen ==None:
		    einzahlungen=""
	    return render.einzahlungen(title,"Einzahlungen",f,einzahlungen,backlink)

    def POST(self):
	    backlink='/'
	    f=forms.newform('einzahlung')
	    einzahlungen=db.query('SELECT * FROM deckelbesitzer AS d JOIN einzahlungen AS e ON d.id=e.deckelbesitzer')
	    #	    return einzahlungen[0]
	    if einzahlungen ==None:
		    einzahlungen=""
	    if not f.validates():
	    	return render.einzahlungen(title,"Einzahlungen",f,einzahlungen,backlink)
	    else:
		    deckelbesitzer=f['id'].value
		    summe=float(f['summe'].value)
		    with db.transaction():
			    sequence_id = db.insert('einzahlungen', deckelbesitzer=deckelbesitzer,summe=summe,time="NOW()")
			    altsumme=db.query("SELECT guthaben FROM guthaben where deckelbesitzer=$deckelbesitzer'",vars=dict(deckelbesitzer=str(deckelbesitzer)))
			    summe=altsumme[0].guthaben+summe
			    db.query('update guthaben set  guthaben=$summe WHERE   deckelbesitzer=$deckelbesitzer',vars=dict(summe=str(summe),deckelbesitzer=str(deckelbesitzer)))
	    	    return render.einzahlungen(title,"Einzahlungen",f,einzahlungen,backlink)

class main:

    def GET(self):
        return render.index(title,"Der elektronische Getränkedeckel")

class deckel:

    def GET(self):
	i = web.input(mode= 'deckel')
	if i.mode=='kasse':
		besitzer = db.query("SELECT * from deckelbesitzer AS  d	JOIN guthaben AS g ON	g.deckelbesitzer=d.id WHERE d.id=$id",vars=dict(id=str(i.id)))
		ownerid = db.query("SELECT * from deckelbesitzer AS  d	JOIN guthaben AS g ON	g.deckelbesitzer=d.id WHERE d.id=$id",vars=dict(id=str(i.id)))
		ownerid = ownerid[0]
		#einkaufliste=form.Form(form.Hidden('',value="test"))
		einkaufliste = []
		for i in range(1,10):
			einkaufliste += [(i,forms.kassenform(ownerid,i))]
		#return einkaufliste[0][0]
		return render.kasse(title,"Kasse",besitzer[0],einkaufliste)

	else:
		besitzer = db.query('SELECT * from deckelbesitzer AS   d JOIN guthaben AS g ON g.deckelbesitzer=d.id')
		return render.deckel(title,"Deckelbesitzer",besitzer)

    def POST(self):
	data = web.input()
	summe = 0
	besitzer = db.query("SELECT * from deckelbesitzer AS  d	JOIN guthaben AS g ON	g.deckelbesitzer=d.id WHERE d.id=$id",vars=dict(id=str(data.besitzer_1)))
	besitzer= besitzer[0]
	preise = db.query('SELECT id,einkaufspreis,verkaufspreis FROM produkte')
	tmp =[]
	for i in preise:
		tmp+=i,
	#preise=tmp
	#return preise[0]['id']#.pop()
	#+ preise[0]
	buchungsfaktor=besitzer.buchungsfaktor
	preise  = {}
	for i in tmp:
		if besitzer.einkaufspreis:
			preise = dict(preise.items() + {'preis_'+str(i.id) : i.einkaufspreis}.items())
		else:
			preise = dict(preise.items() + {'preis_'+str(i.id) : i.verkaufspreis}.items())
	posten=[]
	summe=0.0
	backlink = "/deckel?mode=kasse&id="+str(besitzer['id'])
	for i in range(1,10):
		try:
			if int(data['anzahl_'+str(i)]) != 0:
				if int(data['anzahl_'+str(i)]) >= 0:
				#			t=(preise[data['id_'+str(i)]])
					anzahl = float(data['anzahl_'+str(i)])
					preis = preise['preis_'+str(data['id_'+str(i)])]
					summe = (summe + (  anzahl * preis )) * buchungsfaktor
					posten.append((data['id_'+str(i)] , anzahl, preis , anzahl * preis , summe))
				else:
					raise(ValueError)
				#[float(data['anzahl_'+str(i)]),preise['preis_'+str(data['id_'+str(i)])]],
			else:
				pass
			break
		except ValueError:
			return render.status(title,"Kasse","Ungültige Eingabe! Die Anzahl muss eine positive ganze Zahl sein.",backlink)

	if summe==0.0:
		return render.status(title,"Kasse","Ungültige Eingabe! Die Anzahl muss eine positive ganze Zahl sein.",backlink)
	
	test=check_guthaben(besitzer['id'],besitzer['kredit'],summe)
	if test == True:
		#return test
		#		pass
		with db.transaction():
			for i in posten:
				print i[0]
				#
				sequence_id = db.insert('umsaetze', deckelbesitzer=besitzer['id'],produkt=i[0],anzahl=i[1],summe=i[2],time="NOW()")
			summe=besitzer['guthaben']-summe
			sequence_id = db.query('UPDATE guthaben SET guthaben='+str(summe)+' WHERE deckelbesitzer=' + str(besitzer['id']))
			sequence_id = db.query("UPDATE guthaben SET guthaben=$summe WHERE deckelbesitzer=$besitzer",vars=dict(summe=str(summe),besitzer=str(besitzer['id'])))
		#sequence_id = db.
	else:
		return test

	besitzer = db.query('SELECT * from deckelbesitzer AS   d JOIN guthaben AS g ON g.deckelbesitzer=d.id')
	return render.status(title,"Kasse","Umsatz erfolgreich eingetragen!","/deckel")
	'''
			return db.query("WITH (SELECT * FROM deckelbesitzer) AS bJOIN (SELECT * from produkte) AS s ON b.id=s.id")[0]

	return summe
	#[data]+preise

     

	#if einkaufspreis:
	#	summe
	#	return besitzer[0]
	#	return web.input().
	#.besitzer:
	#	tmp+=i
	#return tmp
	'''



class admin:
    def GET(self):
	    i = web.input(mode = 'admin')
	    f=forms.newform(i.mode)
	    if i.mode=='newdeckel':
		    return render.form(title,"Neuer Deckel",f,i.mode)
	    elif i.mode=='deckelbesitzer':
		    besitzer = db.query('SELECT * from deckelbesitzer AS   d JOIN guthaben AS g ON g.deckelbesitzer=d.id')
		    return render.deckelbesitzer(title,"Deckelbesitzer",besitzer)
	    elif i.mode=='newprodukt':
		    return render.form(title,"Neues Produkt",f,i.mode)
	    elif i.mode=='editprodukt':
		    produkt=db.select('produkte',where="id="+i.id)	
		    f=forms.editform(i.mode,produkt)
		    return render.form(title,"Produkt bearbeiten",f,i.mode)
	    elif i.mode=='editdeckel':
		    besitzer=db.select('deckelbesitzer',where="id="+i.id)	
		    f=forms.editform(i.mode,besitzer)
		    return render.form(title,"Deckelbesitzer bearbeiten",f,i.mode)
	    elif i.mode=='karte':
		    produkte = db.select('produkte')
		    return render.karte(title,"Karte",produkte)
	    elif i.mode=='admin':
		    return render.admin(title,"Verwaltung")
	    elif i.mode=='einzahlung':
	    	    f=forms.newform('einzahlung')
	            einzahlungen=db.query('SELECT * FROM deckelbesitzer AS d JOIN einzahlungen AS e ON d.id=e.deckelbesitzer')
	            if einzahlungen ==None:
			einzahlungen=""
		    backlink='/admin'
	            return render.einzahlungen(title,"Einzahlungen",f,einzahlungen,backlink)
	    else:
		    return render.admin(title,"Verwaltung")

    def POST(self):
	    i=web.input()
	    mode=i.mode
	    f=forms.newform(mode)
	    #if not f.validates():
	    if mode=='newprodukt':
	       heading="Neues Produkt"
	    elif mode=='newdeckel':
	       heading="Neuer Deckel"
	    elif mode=='editprodukt':
	       produkt=db.select('produkte',where="id="+i.id)	
	       f=forms.editform(mode,produkt)
	       heading="Produkt bearbeiten"
	    elif mode=='editdeckel':
	       deckelbesitzer=db.select('deckelbesitzer',where="id="+i.id)	
	       f=forms.editform(mode,deckelbesitzer)
	       heading="Deckel bearbeiten"
	    else:
	       pass

	    if not f.validates():
	    	return render.form(title,heading,f,mode)
	    else:
		    if mode=='newprodukt':
			    bezeichnung=f['bezeichnung'].value
		            einkaufspreis=float(f['einkaufspreis'].value)
		            verkaufspreis=float(f['verkaufspreis'].value)
		            sequence_id = db.insert('produkte', einkaufspreis=float(einkaufspreis),verkaufspreis=float(verkaufspreis),bezeichnung=bezeichnung)
			    update_string="Neues Produkt erfolgreich		    hinzugefügt!"
			    heading="Produkt hinzugefügt"
			    backlink="/admin"
		    elif mode=='editprodukt':
			    bezeichnung=f['bezeichnung'].value
		            einkaufspreis=float(f['einkaufspreis'].value)
		            verkaufspreis=float(f['verkaufspreis'].value)
		            sequence_id = db.update('produkte',where="id="+i.id ,einkaufspreis=float(einkaufspreis),verkaufspreis=float(verkaufspreis),bezeichnung=bezeichnung),
			    update_string="Produkt erfolgreich	bearbeitet!"
			    heading="Produkt bearbeitet"
			    backlink="/admin?mode=karte"
		    elif mode=='newdeckel':
			    nachname=f['nachname'].value
			    vorname=f['vorname'].value
			    email=f['email'].value
			    adresse=f['adresse'].value
			    buchungsfaktor=float(f['buchungsfaktor'].value)
			    einkaufsdeckel=f['einkaufsdeckel'].checked
			    if einkaufsdeckel==True:
				    einkaufsdeckel=True
			    else:
				    einkaufsdeckel=False
			    kredit=float(f['kredit'].value)
			    with db.transaction():
				    sequence_id = db.insert('deckelbesitzer', nachname=nachname,vorname=vorname,email=email,adresse=adresse,buchungsfaktor=buchungsfaktor,einkaufspreis=einkaufsdeckel,kredit=kredit)
			    	    sequence_id= db.insert('guthaben',deckelbesitzer=sequence_id,guthaben='0')
			    update_string="Neuer Deckel erfolgreich		    hinzugefügt!"
			    heading="Deckel hinzugefügt"
			    backlink="/admin"
		    elif mode=='editdeckel':
			    nachname=f['nachname'].value
			    vorname=f['vorname'].value
			    email=f['email'].value
			    adresse=f['adresse'].value
			    buchungsfaktor=float(f['buchungsfaktor'].value)
			    einkaufsdeckel=f['einkaufsdeckel'].checked
			    if einkaufsdeckel==True:
				    einkaufsdeckel=True
			    else:
				    einkaufsdeckel=False
			    kredit=float(f['kredit'].value)
		            sequence_id =db.update('deckelbesitzer',where="id="+i.id, nachname=nachname,vorname=vorname,email=email,adresse=adresse,buchungsfaktor=buchungsfaktor,einkaufspreis=einkaufsdeckel,kredit=kredit)
			    update_string="Deckel erfolgreich geändert!"
			    heading=""
			    backlink="/admin"
		    else:
			    pass
		    return render.status(title,heading, update_string,backlink)

if __name__ == "__main__":
    app.run()
