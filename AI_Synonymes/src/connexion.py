# -*- coding: utf-8 -*-
import sys
import sqlite3

sys.path.append('..')

class Connexion():
    def __init__(self):
        self.curseur = None
        self.connexion = None

    def ouvrirConnexion(self):
        self.connexion = sqlite3.connect('cooc.db')
        self.curseur = self.connexion.cursor()
        self.initialisationBD()

    def initialisationBD(self):
        self.curseur.execute('''CREATE TABLE IF NOT EXISTS DICTIONNAIRE
                                (ID int ,
                                MOT char(40) UNIQUE NOT NULL,
                                PRIMARY KEY (ID))''')
        self.curseur.execute('''CREATE TABLE IF NOT EXISTS COOCURRENCES
                                (IDMOT int NOT NULL,
                                IDCOOC int NOT NULL,
                                TFENETRE int NOT NULL,
                                FREQUENCE int NOT NULL,
                                PRIMARY KEY (IDMOT, IDCOOC, TFENETRE),
                                FOREIGN KEY (IDMOT) REFERENCES DICTIONNAIRE(ID),
                                FOREIGN KEY (IDCOOC) REFERENCES DICTIONNAIRE(ID) )''')
        self.connexion.commit()

    def fermerConnexion(self):
        self.connexion.close()

    def telechargementDictionnaire(self):
        dictionnaireMotsBD = {}
        self.curseur.execute('SELECT * FROM DICTIONNAIRE')
        mots = self.curseur.fetchall()

        for (idMot, mot) in mots:
            dictionnaireMotsBD[mot] = idMot

        return dictionnaireMotsBD

    def telechargementCoocurrences(self, taille):
        dictionnaireCoocurrences = {}
        self.curseur.execute('SELECT * FROM COOCURRENCES WHERE TFENETRE = ?', (taille,))
        coocurrences = self.curseur.fetchall()

        for (idMot, idCoocurrence, tailleFenetre, frequence) in coocurrences:
            dictionnaireCoocurrences[(idMot, idCoocurrence, tailleFenetre)] = frequence

        return dictionnaireCoocurrences

    def remplirDictionnaire(self, listeNouveauxMots):
        self.curseur.executemany('INSERT INTO DICTIONNAIRE VALUES(?, ?)', listeNouveauxMots)
        self.connexion.commit()

    # Update coocurances
    def updateBD(self, dictionnaireCoocurrencesBD, dictionnaireNouvellesCoocurrences, tailleFenetre):
        listeInsert = []
        listeUpdate = []
        compte = 0

        for ((idMot, idCoocurrence), frequence) in dictionnaireNouvellesCoocurrences.items():
            compte += 1

            if((idMot,idCoocurrence,tailleFenetre)  in dictionnaireCoocurrencesBD):
                listeUpdate.append((frequence + dictionnaireCoocurrencesBD[(idMot,idCoocurrence,tailleFenetre)], idMot, idCoocurrence, tailleFenetre))
            else:
                listeInsert.append((idMot,idCoocurrence,tailleFenetre,frequence))

        requeteInsert = 'INSERT INTO COOCURRENCES (IDMOT, IDCOOC, TFENETRE, FREQUENCE) VALUES (?, ?, ?, ?)'
        requeteUpdate = 'UPDATE COOCURRENCES SET FREQUENCE = ? WHERE IDMOT = ? AND IDCOOC= ? AND TFENETRE= ?'
        self.curseur.executemany(requeteUpdate,listeUpdate)
        self.curseur.executemany(requeteInsert,listeInsert)
        self.connexion.commit()

if __name__ == '__main__':
    print('Dans Connexion')