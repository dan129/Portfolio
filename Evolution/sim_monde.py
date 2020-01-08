# -*- coding: utf-8 -*-
import numpy as np
import random
import datetime as dt
import terrain
import animaux
import vegetaux
import habitation

class Monde():
    def __init__(self, parent):
        self.parent = parent
        self.simEnCours = False
        self.pause = True
        self.pauseHorsSim = False
        self.seed = None
        self.environnement = None
        self.dimensionsTerrain = 32
        self.nivEau = None
        self.listeTerrain = [
            ["Eau", 0],
            ["Sable", 0],
            ["Gazon", 0],
            ["Montagne", 0],
            ["Sommet Montagne", 1]
            ]
        self.temps = None
        self.multiplicateurTemps = 60                # Représente 1 minute par unité
        self.animauxListe = None
        self.terrierListe= None
        self.vegetauxListe = None
        self.habitationList = None
        self.pourcentageAnimaux = None
        self.pourcentageVegetaux = None
        self.pourcentageHabitation = None
        self.dictionnaireAnimaux = {                # Classe / Terrain sur le quel il peut commencer
            "Lapin" : [animaux.Lapin, [False, False, True, False, False]],
            "Lièvre" : [animaux.Lievre, [False, False, True, False, False]],
            "Loup" : [animaux.Loup, [False, False, True, False, False]],
            "Ours" : [animaux.Ours, [False, False, True, False, False]],
            "Bison": [animaux.Bison, [False, False, True, False, False]]
            }
        self.dictionnaireVegetaux = {               # Classe / Terrain sur le quel il peut commencer
            "Blé" : [vegetaux.Ble, [False, False, True, False, False]],
            "Cerisier" : [vegetaux.Cerisier, [False, False, True, False, False]],
            "Érable" : [vegetaux.Erable, [False, False, True, False, False]],
            "Laitue" : [vegetaux.Laitue, [False, False, True, False, False]],
            "Peuplier" : [vegetaux.Peuplier, [False, False, True, False, False]],
            "Sapin" : [vegetaux.Sapin, [False, False, True, False, False]]
            }
        self.dictionnaireHabitation = {
            "Terrier" : [habitation.Terrier, [False, False, True, False, False]],
            "Caverne" : [habitation.Caverne, [False, False, True, False, False]]
            }
        self.semenceBle=0
        self.dictBiomePlaine = {
            'temperature':20,
            'humiditeSol':60,
            'humiditeAir':20,
            'nutrimentSol':60,
            'ensoleille':True,
            'pluie':False,
            'nuageux':False
            }
        self.listePolygamie=[animaux.Lapin, animaux.Lievre]
        self.saison = None
        self.changementSaison = None

    def demarrerSim(self, popAnimal, popVegetal, nivEau, elevTerrain, noyau):
        np.random.seed(noyau)                       # Sert pour la génération du terrain
        self.temps = dt.datetime(1, 1, 1)
        self.saison = self.getSaison()
        self.changementSaison = True
        self.animauxListe = []
        self.habitationList = []
        self.vegetauxListe = []
        self.determinationPopAnimal(popAnimal)
        self.determinationPopVegetal(popVegetal)
        self.determinationNivEau(nivEau)
        self.determinationElevTerrain(elevTerrain)
        self.genTerrain()
        self.genEtresVivants()
        self.simEnCours = True
        self.pause = False

    def determinationPopAnimal(self, popAnimal):
        if popAnimal == "Rare":
            pourcentage = 2.5
        elif popAnimal == "Basse":
            pourcentage = 5
        elif popAnimal == "Normale":
            pourcentage = 10
        elif popAnimal == "Élevée":
            pourcentage = 20
        elif popAnimal == "Abondante":
            pourcentage = 40

        self.pourcentageAnimaux = pourcentage

    def determinationPopVegetal(self, popVegetal):
        if popVegetal == "Rare":
            pourcentage = 5
        elif popVegetal == "Basse":
            pourcentage = 10
        elif popVegetal == "Normale":
            pourcentage = 20
        elif popVegetal == "Élevée":
            pourcentage = 40
        elif popVegetal == "Abondante":
            pourcentage = 80

        self.pourcentageVegetaux = pourcentage

    def determinationNivEau(self, nivEau):
        if nivEau == "Très Bas":
            self.nivEau = -0.6
        elif nivEau == "Bas":
            self.nivEau = -0.4
        elif nivEau == "Normal":
            self.nivEau = -0.2
        elif nivEau == "Élevé":
            self.nivEau = 0
        elif nivEau == "Très Élevé":
            self.nivEau = 0.2

    def determinationElevTerrain(self, elevTerrain):
        if elevTerrain == "Très Bas":
            modificateur = 0.5
        elif elevTerrain == "Bas":
            modificateur = 0.25
        elif elevTerrain == "Normal":
            modificateur = 0
        elif elevTerrain == "Élevé":
            modificateur = -0.25
        elif elevTerrain == "Très Élevé":
            modificateur = -0.5

        differenceTerrain = 1 - self.nivEau
        self.listeTerrain[0][1] = self.nivEau
        self.listeTerrain[1][1] = differenceTerrain / 100 * 10 + self.nivEau + modificateur
        self.listeTerrain[2][1] = differenceTerrain / 100 * 70 + self.nivEau + modificateur
        self.listeTerrain[3][1] = differenceTerrain / 100 * 90 + self.nivEau + modificateur

    def genTerrain(self):
        self.environnement = []

        genTerrain = terrain.generate_fractal_noise_2d((self.dimensionsTerrain, self.dimensionsTerrain), (2, 2), 5)

        for rangee in genTerrain:
            rangeeHorizontale=[]

            for case in rangee:
                rangeeHorizontale.append([case, None, None])

            self.environnement.append(rangeeHorizontale)

        if self.parent.vue.debugEnvironnement:
            for ligne in self.environnement:
                print(ligne)

    def genPlante(self, plante, nb):
        #print("gen plante -->",plante)
        for i in range(nb):
            while True:
                x = random.randrange(self.dimensionsTerrain)
                y = random.randrange(self.dimensionsTerrain)
                limite = self.listeTerrain[1][1]

                if limite < self.nivEau:
                    limite = self.nivEau

                if self.environnement[y][x][2] == None and self.environnement[y][x][0] > limite and self.environnement[y][x][0] < self.listeTerrain[2][1]:
                    self.vegetauxListe.append(plante(self, x, y, self.dictBiomePlaine, self.temps))
                    break

    def genHabitation(self,habitation,nb):
        for i in range(nb):
            while True:
                x = random.randrange(self.dimensionsTerrain)
                y = random.randrange(self.dimensionsTerrain)
                limite = self.listeTerrain[1][1]

                if limite < self.nivEau:
                    limite = self.nivEau

                if self.environnement[y][x][1] == None and self.environnement[y][x][0] > limite and self.environnement[y][x][0] < self.listeTerrain[2][1]:
                    self.habitationList.append(habitation(self,x,y))
                    break

    def genEtresVivants(self):
        for y in range(self.dimensionsTerrain):
            for x in range(self.dimensionsTerrain):
                for i in range(len(self.listeTerrain)):
                    if self.environnement[y][x][0] <= self.listeTerrain[i][1]:
                        if random.randrange(100) <= self.pourcentageAnimaux:
                            listeAnimauxPotentiels = []

                            for cleAnimal, valeurAnimal in self.dictionnaireAnimaux.items():
                                if valeurAnimal[1][i]:
                                    listeAnimauxPotentiels.append(valeurAnimal[0])

                            nbAnimauxPotentiels = len(listeAnimauxPotentiels)

                            if nbAnimauxPotentiels != 0:
                                animalSelectionne = random.randrange(nbAnimauxPotentiels)
                                sexe = random.randrange(2)
                                self.animauxListe.append(listeAnimauxPotentiels[animalSelectionne](self, x, y, sexe))

                        if random.randrange(100) <= self.pourcentageVegetaux:
                            listeVegetauxPotentiels = []

                            for clePlante, valeurPlante in self.dictionnaireVegetaux.items():
                                if valeurPlante[1][i]:
                                    listeVegetauxPotentiels.append(valeurPlante[0])

                            nbPlantesPotentiels = len(listeVegetauxPotentiels)

                            if nbPlantesPotentiels != 0:
                                planteSelectionnee = random.randrange(nbPlantesPotentiels)
                                self.vegetauxListe.append(listeVegetauxPotentiels[planteSelectionnee](self, x, y, self.dictBiomePlaine, self.temps))

                        self.pourcentageHabitation = 2
                        if random.randrange(100) <= self.pourcentageHabitation:
                            listeHabitationPotentiels = []

                            for cleHab, valeurHab in self.dictionnaireHabitation.items():
                                if valeurHab[1][i]:
                                    listeHabitationPotentiels.append(valeurHab[0])

                            nbHabPotentiels = len(listeHabitationPotentiels)

                            if nbHabPotentiels != 0:
                                habSelectionnee = random.randrange(nbHabPotentiels)
                                self.habitationList.append(listeHabitationPotentiels[habSelectionnee](self, x, y))
                        break

    def changementsClimatiques(self):
        if self.temps.hour == 0 or self.temps.hour == 5 or self.temps.hour == 10 or self.temps.hour == 15 or self.temps.hour == 20:
            #print(self.dictBiomePlaine)
            #JANVIER
            if self.temps.month == 1:
                self.tMinMoyen = -4
                self.tMoyen = 1
                self.tMaxMoyen = 3
                self.humiditeMin = 0
                self.humiditeMoyen = 0
                self.humiditeMax = 0
                self.precipitationMoyen = 14
                self.precipitationsMin = 5
                self.percipitationsMax = 20
                self.chancePluie = 1/7
            #FEVRIER
            elif self.temps.month == 2:
                self.tMinMoyen = -2
                self.tMoyen = 2
                self.tMaxMoyen = 5
                self.humiditeMin = 0
                self.humiditeMoyen = 0
                self.humiditeMax = 0
                self.precipitationMoyen = 16
                self.precipitationsMin = 7
                self.percipitationsMax = 22
                self.chancePluie = 1/6
            #MARS
            elif self.temps.month == 3:
                self.tMinMoyen = 1
                self.tMoyen = 2
                self.tMaxMoyen = 9
                self.humiditeMin = 0
                self.humiditeMoyen = 0
                self.humiditeMax = 0
                self.precipitationMoyen = 22
                self.precipitationsMin = 10
                self.percipitationsMax = 29
                self.chancePluie = 1/5
            #AVRIL
            elif self.temps.month == 4:
                self.tMinMoyen = 5
                self.tMoyen = 10
                self.tMaxMoyen = 17
                self.humiditeMin = 0
                self.humiditeMoyen = 0
                self.humiditeMax = 1
                self.precipitationMoyen = 32
                self.precipitationsMin = 19
                self.percipitationsMax = 38
                self.chancePluie = 1/4
            #MAI
            elif self.temps.month == 5:
                self.tMinMoyen = 9
                self.tMoyen = 16
                self.tMaxMoyen = 20
                self.humiditeMin = 0
                self.humiditeMoyen = 5
                self.humiditeMax = 18
                self.precipitationMoyen = 32
                self.precipitationsMin = 19
                self.percipitationsMax = 38
                self.chancePluie = 1/4
            #JUIN
            elif self.temps.month == 6:
                self.tMinMoyen = 14
                self.tMoyen = 22
                self.tMaxMoyen = 24
                self.humiditeMin = 0
                self.humiditeMoyen = 20
                self.humiditeMax = 50
                self.precipitationMoyen = 59
                self.precipitationsMin = 40
                self.percipitationsMax = 70
                self.chancePluie = 1/3
            #JUILLET
            elif self.temps.month == 7:
                self.tMinMoyen = 15
                self.tMoyen = 24
                self.tMaxMoyen = 30
                self.humiditeMin = 5
                self.humiditeMoyen = 40
                self.humiditeMax = 65
                self.precipitationMoyen = 60
                self.precipitationsMin = 40
                self.percipitationsMax = 100
                self.chancePluie = 1/3
            #AOUT
            elif self.temps.month == 8:
                self.tMinMoyen = 15
                self.tMoyen = 21
                self.tMaxMoyen = 28
                self.humiditeMin = 5
                self.humiditeMoyen = 35
                self.humiditeMax = 60
                self.precipitationMoyen = 57
                self.precipitationsMin = 40
                self.percipitationsMax = 85
                self.chancePluie = 1/4
            #SEPTEMBRE
            elif self.temps.month == 9:
                self.tMinMoyen = 12
                self.tMoyen = 18
                self.tMaxMoyen = 22
                self.humiditeMin = 0
                self.humiditeMoyen = 20
                self.humiditeMax = 35
                self.precipitationMoyen = 52
                self.precipitationsMin = 30
                self.percipitationsMax = 90
                self.chancePluie = 1/4
            #OCTOBRE
            elif self.temps.month == 10:
                self.tMinMoyen = 6
                self.tMoyen = 10
                self.tMaxMoyen = 15
                self.humiditeMin = 0
                self.humiditeMoyen = 2
                self.humiditeMax = 10
                self.precipitationMoyen = 18
                self.precipitationsMin = 30
                self.percipitationsMax = 60
                self.chancePluie = 1/5
            #NOVEMBRE
            elif self.temps.month == 11:
                self.tMinMoyen = 2
                self.tMoyen = 5
                self.tMaxMoyen = 8
                self.humiditeMin = 0
                self.humiditeMoyen = 0
                self.humiditeMax = 0
                self.precipitationMoyen = 24
                self.precipitationsMin = 18
                self.percipitationsMax = 40
                self.chancePluie = 1/6
            #DECEMBRE
            elif self.temps.month == 12:
                self.tMinMoyen = -5
                self.tMoyen = 0
                self.tMaxMoyen = 4
                self.humiditeMin = 0
                self.humiditeMoyen = 0
                self.humiditeMax = 0
                self.precipitationMoyen = 18
                self.precipitationsMin = 8
                self.percipitationsMax = 30
                self.chancePluie = 1/6

            #--TEMPERATURE--
            if self.dictBiomePlaine['temperature'] > self.tMaxMoyen:
                self.dictBiomePlaine['temperature'] -= 1
            elif self.dictBiomePlaine['temperature'] < self.tMinMoyen:
                self.dictBiomePlaine['temperature'] += 1
            else:
                if random.randrange(1,2) == 2:
                    self.dictBiomePlaine['temperature'] += random.randrange(1,5)
                else:
                    self.dictBiomePlaine['temperature'] -= random.randrange(1,5)

            #---PLUIE---
            #il pleut lorsque le niveau des precipitations est en dessou de la moyenne
            if self.dictBiomePlaine['humiditeSol'] < self.precipitationMoyen:
                # 1 chance sur x de pluie
                if random.randrange(1,self.chancePluie) == 2:
                    self.dictBiomePlaine['pluie'] = True
                    self.dictBiomePlaine['ensoleille'] = False
                    self.dictBiomePlaine['humiditeSol'] = random.randrange(self.precipitationsMin,self.percipitationsMax)
                else:
                    self.dictBiomePlaine['pluie'] = False
                    self.dictBiomePlaine['ensoleille'] = True
            #---HUMIDITE AIR---
            if self.humiditeMax == 0:
                self.dictBiomePlaine['humiditeAir'] = self.humiditeMax
            elif self.dictBiomePlaine['humiditeAir'] < self.humiditeMoyen:
                self.dictBiomePlaine['humiditeAir'] += random.randrange(0,1)
            #tant qu'on ne depasse pas le taux d'humidité maximal
            elif self.dictBiomePlaine['humiditeAir'] < self.humiditeMax:
                if random.randrange(1,2) == 2:
                    self.dictBiomePlaine['humiditeAir'] += random.randrange(1,3)
                else:
                    self.dictBiomePlaine['humiditeAir'] -= random.randrange(1,3)
            #le niveau d'humidite est depasse
            else:
                self.dictBiomePlaine['humiditeAir'] -= random.randrange(1,2)

            if self.dictBiomePlaine['humiditeAir'] < 0:
                self.dictBiomePlaine['humiditeAir'] = 0
        #print(self.dictBiomePlaine['humiditeAir'],self.dictBiomePlaine['pluie'],self.dictBiomePlaine['temperature'])

    def getSaison(self):
        if self.temps.month == 1 or self.temps.month == 2 or self.temps.month == 3:
            return "hiver"
        elif self.temps.month == 4 or self.temps.month == 5 or self.temps.month == 6 :
            return "printemps"
        elif self.temps.month == 7 or self.temps.month == 8 or self.temps.month == 9:
            return "ete"
        elif self.temps.month == 10 or self.temps.month == 11 or self.temps.month == 12:
            return "automne"

    def jouerSim(self):
        tempsAjoute = dt.timedelta(minutes = self.multiplicateurTemps / self.parent.nbFramesSec)
        tempsActuel = self.temps - dt.datetime(1, 1, 1)
        finCalendrier = (dt.datetime(9999, 12, 31) - dt.datetime(1, 1, 1)) + dt.timedelta(seconds = 86399)

        while (tempsActuel + tempsAjoute).total_seconds() > finCalendrier.total_seconds():
            tempsAjoute -= finCalendrier

        self.temps += tempsAjoute

        if self.getSaison() != self.saison:
            self.saison = self.getSaison()
            self.changementSaison = True
        else:
            self.changementSaison = False

        self.changementsClimatiques()

        for animal in self.animauxListe:
            animal.behavior()

        for animal in self.animauxListe:
            self.environnement[animal.attributes["posY"]][animal.attributes["posX"]][1] = animal

        for habi in self.habitationList:
            self.environnement[habi.attributes["posY"]][habi.attributes["posX"]][1] = habi

        for plante in self.vegetauxListe:
            if plante.attributes["periodeDeLAnnee"] == True:                  # a ajouter lorsque les saisons vont etre disponibles
                self.environnement[plante.attributes["posY"]][plante.attributes["posX"]][2] = plante
            plante.vivre()
            if plante.attributes["mort"] == True:
                self.environnement[plante.attributes["posY"]][plante.attributes["posX"]][2] = None  #supprime la plante une fois qu'elle meurt
                self.vegetauxListe.remove(plante)

        if self.parent.vue.debugEnvironnement:
            for ligne in self.environnement:
                print(ligne)

    def ajouterElement(self, typeElement, coordX, coordY):
        if typeElement in self.dictionnaireAnimaux and self.environnement[coordY][coordX][1] == None:
            sexe = random.randrange(2)
            animal = self.dictionnaireAnimaux[typeElement][0](self, coordX, coordY, sexe)
            self.animauxListe.append(animal)
            self.environnement[coordY][coordX][1] = animal
        elif typeElement in self.dictionnaireVegetaux and self.environnement[coordY][coordX][2] == None:
            plante = self.dictionnaireVegetaux[typeElement][0](self, coordX, coordY, self.dictBiomePlaine, self.temps)
            self.vegetauxListe.append(plante)
            self.environnement[coordY][coordX][2] = plante

    def supprimerElement(self, typeElement, coordX, coordY):
        if typeElement in self.dictionnaireAnimaux:
            animal = self.environnement[coordY][coordX][1]

            if animal != None:
                if isinstance(animal, animaux.Animal):
                    self.animauxListe.remove(animal)
                    self.environnement[coordY][coordX][1] = None
        elif typeElement in self.dictionnaireVegetaux:
            plante = self.environnement[coordY][coordX][2]

            if plante != None:
                if isinstance(plante, vegetaux.Plante):
                    self.vegetauxListe.remove(plante)
                    plante.tuer()
                    self.environnement[coordY][coordX][2] = None

if __name__ == '__main__':
    print("Dans Modele (Monde)")