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
db = web.database(dbn='postgres', host='localhost',db='fg_deckel', user='fginfo',pw='fginfo')


class einzahlung:
	   
    def GET(self):
	    i=web.input()
	    backlink=web.input(back='/').back
	    if i:
		    #return web.input()
	    	    db.query('delete FROM einzahlungen WHERE deckelbesitzer='+i.delete+" AND time='"+i.time+"'")
	    f=forms.newform('einzahlung')
	    einzahlungen=db.query('SELECT * FROM deckelbesitzer AS d JOIN einzahlungen AS e ON d.id=e.deckelbesitzer')
	    if einzahlungen ==None:
		    einzahlungen=""
	    return render.einzahlungen(title,"Einzahlungen",f,einzahlungen,backlink)

    def POST(self):
	    f=forms.newform('einzahlung')
	    einzahlungen=db.query('SELECT * FROM deckelbesitzer AS d JOIN einzahlungen AS e ON d.id=e.deckelbesitzer')
	    if einzahlungen ==None:
		    einzahlungen=""
	    if not f.validates():
	    	return render.einzahlungen(title,"Einzahlungen",f,einzahlungen)
	    else:
		    deckelbesitzer=f['id'].value
		    summe=float(f['summe'].value)
		    sequence_id = db.insert('einzahlungen', deckelbesitzer=deckelbesitzer,summe=summe)
	    	    return render.einzahlungen(title,"Einzahlungen",f,einzahlungen)

class main:
    def GET(self):
        return render.index(title,"Der elektronische Getränkedeckel")


class admin:
    def GET(self):
	    i = web.input(mode = 'admin')
	    f=forms.newform(i.mode)
	    if i.mode=='newdeckel':
		    return render.form(title,"Neuer Deckel",f,i.mode)
	    elif i.mode=='deckelbesitzer':
		    besitzer = db.select('deckelbesitzer')
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
		            sequence_id = db.insert('deckelbesitzer',guthaben='0', nachname=nachname,vorname=vorname,email=email,adresse=adresse,buchungsfaktor=buchungsfaktor,einkaufspreis=einkaufsdeckel,kredit=kredit)
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
