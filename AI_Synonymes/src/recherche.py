# -*- coding: utf-8 -*-
import connexion
import numpy as np
import analyseVectorielles

class Recherche:
    def __init__(self, taille):
        self.options = ['produit scalaire','least-squares', 'city-block']
        analyse = analyseVectorielles.AnalyseVectorielle()
        connexionBD = connexion.Connexion()

        print('Chargement des données de la base de donnée...')
        connexionBD.ouvrirConnexion()
        dictBD = connexionBD.telechargementDictionnaire()
        coocBD = connexionBD.telechargementCoocurrences(taille)
        connexionBD.fermerConnexion()

        print('Chargement terminé.')
        if(len(dictBD) == 0 or len(coocBD) == 0):
            print('Veuillez d\'abord entrainez vos resultats')
        else:
            self.commencerRecherche(analyse, dictBD, coocBD)

    def afficherOptions(self):
        print('\nEntrez un mot, le nombre de synonymes que vous voulez et la méthode de calcul,')

        textOptions = 'i.e '
        compteur = 0

        for option in self.options:
            textOptions += ' ' + str(compteur) + ': ' + option
            compteur += 1

        print(textOptions)
        print('\nTapez q pour quitter.\n')

    def commencerRecherche(self, analyse, dictBD, coocBD):
        saisie = None

        while saisie != 'q':
            self.afficherOptions()
            saisie = str(np.core.defchararray.lower(input()))
            saisieSeparee = saisie.split(' ')

            # Si l'utilisatuer entre les bonnes données
            if saisie == 'q':
                print('\nFin de la recherche.')
            elif len(saisieSeparee) != 3:
                print('\nLe nombre d\'arguments entrés n\'est pas valide, veuillez recommencer.')
            elif saisieSeparee[0] not in dictBD:
                print('\nLe mot recherché n\'est pas dans le dictionnaire.')
            elif int(saisieSeparee[2]) >= len(self.options) or int(saisieSeparee[2]) < 0:
                print('\nL\'option de traitement choisie n\'existe pas.')
            else:
                synonyme = saisieSeparee[0]
                nbSynonyme = int(saisieSeparee[1])
                resultats = analyse.calcul(int(saisieSeparee[2]), dictBD, coocBD, synonyme)
                self.imprimerResultats(resultats, nbSynonyme)
    
    def imprimerResultats(self, resultats, nbSynonyme):
        print('\nRésultats:')
        
        for score, mot in resultats[:nbSynonyme]:
            print(mot, '--->', score)

if __name__ == '__main__':
    print('Dans Recherche')