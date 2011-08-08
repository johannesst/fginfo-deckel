# !/usr/bin/env python
# -*- coding: UTF-8 -*-
import web
from web import form
import forms
import time

urls = (
'/', 'main',
'/deckel','deckel',
'/einzahlung', 'einzahlung',
'/admin', 'admin')
title = "Getränkedeckel FG Informatik"
app = web.application(urls, globals(), autoreload=True)
render = web.template.render('templates/', base='base')
db = web.database(dbn='postgres', host='localhost',db='fginfo-deckel', user='fginfo',pw='fginfo')


class einzahlung:
   
    def GET(self):
	    i=web.input()
	    backlink=web.input(back='/').back
	    '''if i:
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
			    altsumme=db.query("SELECT guthaben FROM guthaben where deckelbesitzer='"+deckelbesitzer+"'")
			    summe=altsumme[0].guthaben+summe
			    db.query('update guthaben set guthaben='+str(summe)+' WHERE  deckelbesitzer='+deckelbesitzer)
	    	    return render.einzahlungen(title,"Einzahlungen",f,einzahlungen,backlink)

class main:
    def GET(self):
        return render.index(title,"Der elektronische Getränkedeckel")

class deckel:
    def GET(self):
	i = web.input(mode= 'deckel')
	if i.mode=='kasse':
		produkte = db.query('SELECT * from produkte')
		f=forms.editform('editprodukt',produkte)
		return render.kasse(title,"Getränke eintragen",i.id,produkte,f)

	else:
		besitzer = db.query('SELECT * from deckelbesitzer AS   d JOIN guthaben AS g ON g.deckelbesitzer=d.id')
		return render.deckel(title,"Deckelbesitzer",besitzer)


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
