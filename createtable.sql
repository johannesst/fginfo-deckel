
/*
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




CREATE TABLE einzahlungen(
	deckelbesitzer integer references deckelbesitzer NOT NULL,
	summe float NOT NULL,
	time timestamp  NOT NULL
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



CREATE TABLE auth (
	id serial  PRIMARY KEY,
	login varchar(255)  NOT NULL,
	pass varchar(255) NOT NULL
);

CREATE TABLE authgroups(
	auth integer references auth NOT NULL,
	groups integer references groups NOT NULL,
	PRIMARY KEY (auth,groups)
);
*/

CREATE TABLE guthaben(
	deckelbesitzer integer references deckelbesitzer NOT NULL PRIMARY KEY,
	guthaben float NOT NULL
)


