


CREATE TABLE deckelbesitzer (
	id serial PRIMARY KEY,
	nachname varchar(255) NOT NULL,
	vorname varchar(255) NOT NULL,
	email varchar(255) NOT NULL,
	adresse varchar(1024) NOT NULL,
	buchungsfaktor float NOT NULL,
	einkaufspreis boolean NOT NULL,
	kredit        float NOT NULL
);

CREATE TABLE produkte (
	id serial PRIMARY KEY NOT NULL,
	bezeichnung varchar(255) NOT NULL,
	einkaufspreis float NOT NULL,
	verkaufspreis float NOT NULL
);


CREATE TABLE umsaetze(
	deckelbesitzer integer references deckelbesitzer NOT NULL,
	produkt integer references produkte NOT NULL,
	summe float NOT NULL,
	time  timestamp NOT NULL
);

CREATE TABLE groups(
	id serial PRIMARY KEY,
	name varchar(255)
);




CREATE TABLE users (
	deckelbesitzer integer references deckelbesitzer NOT NULL,
	id integer PRIMARY KEY NULL,
	login varchar(255)  NOT NULL,
	pass varchar(255) NOT NULL,
	UNIQUE(deckelbesitzer,login)
);



CREATE TABLE passwd (
	nutzer integer references users NOT NULL,
	gruppe integer references groups NOT NULL,
	UNIQUE(nutzer,gruppe)
);


