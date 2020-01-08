# -*- coding: utf-8 -*-

import numpy as np
import analyseVectorielles
import connexion
import csv

class KNN():
    def __init__(self, taille, kMots, encodage, mots):
        analyse = analyseVectorielles.AnalyseVectorielle()
        connexionBD = connexion.Connexion()
        
        print('Chargement des données...')
        connexionBD.ouvrirConnexion()
        dictBD = connexionBD.telechargementDictionnaire()
        coocBD = connexionBD.telechargementCoocurrences(taille)
        connexionBD.fermerConnexion()
        matrice = np.zeros((len(dictBD), len(dictBD)))
        self.remplirMatrice(matrice, coocBD)
        lexique = self.lectureLexique(encodage)
        
        print('Analyse des données...')    
        resultatsLS = []
        
        for mot in mots:
            mot = mot.lower()
            resultatsLS.append(analyse.calcul(1, dictBD, coocBD, mot))
        
        resultatsFinaux = self.calculKNN(resultatsLS, lexique, kMots)
        self.imprimerResultats(mots, resultatsFinaux)
        
    def remplirMatrice(self, matrice, coocBD):
        for coocurences, frequence in coocBD.items():
            matrice[coocurences[0]][coocurences[1]] = frequence
            
    def lectureLexique(self, encodage):
        fichier = open('..\lexiques\Lexique382.tsv', encoding = encodage)
        mots = csv.reader(fichier, delimiter='\t')
        lexique = []
        
        for mot in mots:
            lexique.append((mot[0], mot[3]))
        
        lexique.pop(0)
        fichier.close()
        
        return lexique
    
    def calculKNN(self, resultatsLS, lexique, kMots):
        resultats = []
        
        for r in resultatsLS:
            motsProche = []
            scoreGenres = {}
            
            for score, mot in r[:kMots]:
                genreMot = []
                
                for motLexique in lexique:
                    if motLexique[0] == mot and motLexique[1] not in genreMot:
                        genreMot.append(motLexique[1])
                
                motsProche.append([score, genreMot])
            
            for motProche in motsProche:
                knnScore = 1 / (motProche[0] + 1)
                
                for genre in motProche[1]:
                    if genre in scoreGenres:
                        scoreGenres[genre] += knnScore
                    else:
                        scoreGenres[genre] = knnScore
                                
            scoreGenresSorted = sorted(scoreGenres, key = scoreGenres.get)
            if len(scoreGenresSorted) == 0:
                resultats.append('Genre Inconnu')
            else:
                resultats.append(scoreGenresSorted[0])
            
        return resultats
    
    def imprimerResultats(self, mots, resultatsFinaux):
        print('\nRésultats:')
        
        for i in range(len(mots)):
            print(mots[i], '--->', resultatsFinaux[i])
                
if __name__ == '__main__':
    print('Dans KNN')