

CREATE TABLE deckelbesitzer (
	id integer PRIMARY KEY,
	nachname varchar(255) NOT NULL,
	vorname varchar(255) NOT NULL,
	email varchar(255) NOT NULL,
	adresse varchar(1024) NOT NULL,
	buchungsfaktor float NOT NULL,
	einkaufspreis boolean NOT NULL,
	kredit        float NOT NULL
);

CREATE TABLE produkte (
	id integer PRIMARY KEY NOT NULL,
	bezeichnung varchar(255) NOT NULL,
	einkaufspreis float NOT NULL,
	verkaufspreis float NOT NULL
);

CREATE TABLE users (
	deckelbesitzer integer references deckelbesitzer NOT NULL,
	login varchar(255)  NOT NULL,
	pass varchar(255) NOT NULL,
	PRIMARY KEY(deckelbesitzer,login)
);

CREATE TABLE umsaetze(
	deckelbesitzer integer references deckelbesitzer NOT NULL,
	produkt integer references produkte NOT NULL,
	summe float NOT NULL,
	time  timestamp NOT NULL
);

CREATE TABLE groups(
	id integer PRIMARY KEY,
	name varchar(255)
);

CREATE TABLE passwd (
	nutzer integer references users NOT NULL,
	gruppe integer references groups NOT NULL
);


