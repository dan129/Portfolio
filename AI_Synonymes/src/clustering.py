# -*- coding: utf-8 -*-
import numpy as np
import sys
import random
import time
import connexion
import analyseVectorielles

class Clustering:
    def __init__(self, taille, nbResultats, nbCentroides, mots, chemin):
        if mots != None:
            mots = mots.lower().split(' ')
            nbCentroides = len(mots)

        connexionBD = connexion.Connexion()
        analyse = analyseVectorielles.AnalyseVectorielle()
        random.seed(int(time.time()))

        print('Chargement des données...')
        connexionBD.ouvrirConnexion()
        dictBD = connexionBD.telechargementDictionnaire()
        coocBD = connexionBD.telechargementCoocurrences(taille)
        connexionBD.fermerConnexion()
        matrice = np.zeros((len(dictBD), len(dictBD)))
        self.remplirMatrice(matrice, coocBD)

        if len(dictBD) == 0:
            print('Aucun mots associé avec la taille de la fenêtre n\'à été répertorié.\nVeuillez entrainer le programme avec la taille désignée ou recommencer avec une autre taille.')
        else:
            motsNonRepertorie = []

            if mots != None:
                for mot in mots:
                    if mot not in dictBD:
                        motsNonRepertorie.append(mot)

            if len(motsNonRepertorie) != 0:
                print('\nles mots suivants ne font pas parti du dictionnaire associé avec la taille de la fenêtre:')

                for mot in motsNonRepertorie:
                    print(mot)

                print('\nVeuillez entrainer le programme avec la taille désignée, recommencer avec une autre taille ou choisir des mots valides.')
            else:
                print('Initialisation des centrodïes de départ...')
                centroidesDepart = self.initCentroides(mots, matrice, dictBD, nbCentroides)

                print('Calcule des clusters...')
                fichier = None
                
                if chemin != None:
                    fichier = open(chemin, 'w+')
                    fichier.write('Arguments: ')
        
                    for arg in sys.argv:
                        fichier.write(arg + ' ')
                    
                clustersFinaux, tempsFinal, nbIterations = self.clustering(centroidesDepart, analyse, dictBD, matrice, fichier)
                self.afficherResultatsCluster(nbIterations, tempsFinal, clustersFinaux, nbResultats)
                
                if chemin != None:
                    self.enregistrerResultats(nbIterations, tempsFinal, clustersFinaux, nbResultats, fichier)
                    fichier.close()

    def remplirMatrice(self, matrice, coocBD):
        for coocurences, frequence in coocBD.items():
            matrice[coocurences[0]][coocurences[1]] = frequence

    def initCentroides(self, mots, matrice, dictBD, nbCentroides):
        centroidesDepart = []

        # Centroides avec mots
        if mots != None:
            for mot in mots:
                centroidesDepart.append(matrice[dictBD[mot]])

        # Centroides au hasard
        else:
            clustersMots = []

            for i in range(nbCentroides):
                clustersMots.append([])

            for mot in dictBD:
                clustersMots[random.randint(0, nbCentroides - 1)].append(matrice[dictBD[mot]])

            for i in range(nbCentroides):
                centroidesDepart.append(np.mean(clustersMots[i], axis = 0))
        
        return centroidesDepart

    def trouverCentroide(self, clusters):
        centroide = []
        
        for cluster in clusters:
            valeurs = []
            
            for cle, valeur in cluster.items():
                valeurs.append(valeur)
                
            centroide.append(np.mean(valeurs, axis=0))

        return centroide

    def clustering(self, centroidesDepart, analyse, dictBD, matrice, fichier):
        clustersVide = [{} for centroide in centroidesDepart]
        nbIterations = 0
        tempsDepart = time.time()
        nouveauCluster, changements = analyse.calculCluster(dictBD, matrice, centroidesDepart, clustersVide)
        nbIterations += 1
        self.afficherIterationCluster(nouveauCluster, changements, nbIterations)
        
        if fichier != None:
            self.enregistrerIteration(nouveauCluster, changements, nbIterations, fichier)
        
        while changements > 0:
            centroides = self.trouverCentroide(nouveauCluster)
            nouveauCluster, changements = analyse.calculCluster(dictBD, matrice, centroides, nouveauCluster)
            nbIterations += 1
            self.afficherIterationCluster(nouveauCluster, changements, nbIterations)
            
            if fichier != None:
                self.enregistrerIteration(nouveauCluster, changements, nbIterations, fichier)
                
        tempsFinal = time.time() - tempsDepart
        
        return nouveauCluster, tempsFinal, nbIterations
    
    def afficherIterationCluster(self, nouveauCluster, changements, nbIterations):
        print('\n=========================================================================\n')
        print('Itération #' + str(nbIterations))
        print('Nombre de changements:', changements)
    
        for i in range(len(nouveauCluster)):
            print('Nombre de mots dans le cluster #' + str(i + 1) + ': ' + str(len(nouveauCluster[i])))
            
    def afficherResultatsCluster(self, nbIterations, tempsFinal, clustersFinaux, nbResultats):
        print('\n=========================================================================\n')
        print('Nombre d\'itérations total:', nbIterations)
        print('Temps total pour effectuer les opérations:', tempsFinal)
        
        for i in range(len(clustersFinaux)):
            print('\n=========================================================================\n')
            print('Cluster #' + str(i + 1) + ":")
            compteur = 0
            
            for cle, score in clustersFinaux[i].items():
                print('   - ', cle)
                compteur += 1
                
                if compteur > nbResultats:
                    break;
    
    def enregistrerIteration(self, nouveauCluster, changements, nbIterations, fichier):
        fichier.write('\n\n=========================================================================\n\n')
        fichier.write('Itération #' + str(nbIterations) + '\n')
        fichier.write('Nombre de changements: ' + str(changements) + '\n')
    
        for i in range(len(nouveauCluster)):
            fichier.write('Nombre de mots dans le cluster #' + str(i + 1) + ': ' + str(len(nouveauCluster[i])) + '\n')
            
    def enregistrerResultats(self, nbIterations, tempsFinal, clustersFinaux, nbResultats, fichier):
        fichier.write('\n\n=========================================================================\n\n')
        fichier.write('Nombre d\'itérations total: ' + str(nbIterations) + '\n')
        fichier.write('Temps total pour effectuer les opérations: ' + str(tempsFinal) + '\n')
        
        for i in range(len(clustersFinaux)):
            fichier.write('\n\n=========================================================================\n\n')
            fichier.write('Cluster #' + str(i + 1) + ":\n")
            compteur = 0
            
            for cle, score in clustersFinaux[i].items():
                fichier.write('   - ' + cle + '\n')
                compteur += 1
                
                if compteur > nbResultats:
                    break;

if __name__ == '__main__':
    print('Dans Clustering')