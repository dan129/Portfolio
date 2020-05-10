# -*- coding: UTF-8 -*-
import random
import Tours
import Creeps
import Projectiles
from _ctypes import sizeof
import time
import Bombes
import helper
import csv
#import pyautogui
    
class Partie():
    def __init__(self,parent):
        self.parent=parent
        self.largeur=1000
        self.longueur=800
        self.timerCreeps=0
        self.compteurCreepsPartie=0
        self.listeCreeps=["gros","normal","rapide"]
        self.joueurMort=False
        self.niveauFini=False
        
        self.creeps=[]
        self.vagueCreeps=[]
        self.tours=[]
        self.sentier=[]
        self.projectiles=[]
      
        self.dimensionCarre=50
        self.niveau=4
        self.score=0
        self.argent=1200 # une tour de base vaut 100 et on veut qu'il puisse au moins avoir 2 tours
        self.bombe=1
        self.bombePosition=[]
        self.nombreDeVie=5 #initialiser le nbre de vie + si c'est par niveau puis se remet a 0 ou pour toute la partie 
        self.nombreVagueParNiveau=3 # initialisation du nombre de vague avec n creeps par niveau
        self.nombreCreepsParVague=10  
        self.randomPourcentage=0
        self.tirerJouerCoup = False

     
    def sauvegarde(self):
        monFichier = open("sauvegarde.txt",'w')
        monFichier.write(str(self.score)+','+str(self.niveau)+','+str(self.nombreDeVie))
        monFichier.close()

        
    def loadSauvegarde(self):
        monFichier = open("sauvegarde.txt",'r')
        resultatDeListe=""
        listeDeSauvegarde = monFichier.readlines()
        for i in listeDeSauvegarde:
            resultatDeListe = i.split(",")
        self.score = int(resultatDeListe[0])
        self.niveau = int(resultatDeListe[1])-1
        self.nombreDeVie = int(resultatDeListe[2])
           
    def creerNiveau(self):
        self.sentier = []
        self.tours=[]
        self.niveau+=1
        if self.niveau%5 == 1:
            self.sentier = [(600,800),(600,700),(500,700),(400,700),(400,600),(625,600),(625,400),(300,400),(300,700),(200,700)
                            ,(200,350),(300,350),(300,300),(600,300),(600,200),(200,200),(200,0)]
        elif self.niveau%5 == 2:
            self.sentier =[(600,800),(600,750),(300,750),(300,550),(600,550),(600,450),(600,250),(600,100)
                           ,(250,100),(250,700),(200,700),(200,0)]
        elif self.niveau%5 == 3:
            self.sentier=[(600,800),(600,750),(750,750),(750,600),(300,600),(300,750),(200,750),(200,550),(200,400),(200,300),
                            (700,300),(700,150),(550,150),(550,225),(450,225),(450,150),(300,150),(300,225),(200,225),(200,0)]
        elif self.niveau%5 == 4:
            self.sentier=[(600,800),(600,600),(500,600),(500,675),(400,675),(400,750),(325,750),(325,675), (226,675), (225,400),
                          (600,400),(600,175),(400,175),(400,350),(200,350),(200,0)]

        else : #Modulo 5 == 0 (donc niveau multiple de 5)
            self.sentier= [(600,800),(600,700),(225,700),(225,600),(500,600),(500,500),(620,500),(620,400),(300,400),
                           (300,350),(225,350),(225,425), (150,425),(150,250),(600,250),(600,125),(200,125),(200,0)]
        
        for x in range(self.nombreCreepsParVague*self.nombreVagueParNiveau):
            self.vagueCreeps.append(self.creerCreep(self,600,800,self.sentier,random.choice(self.listeCreeps)))
            
        
        self.creeps.append(Creeps.Creep(self,600,800,self.sentier))                    
        return 1
    
    
    def bombeExplose(self):
        creepMort=[]
        for creep in self.creeps:
            for bombe in self.bombePosition:
                positionX= abs(bombe.x-creep.x)
                positionY= abs(bombe.y-creep.y)
                if positionX<=75 and positionY<=75 :
                    creepMort.append(creep)    

        # on va verifier si le creep a deja été tué avant de le tuer de nouveau 
        posmort=[]
        for creepMort in creepMort:
            if [creepMort.x,creepMort.y] not in posmort :
                posmort.append([creepMort.x,creepMort.y])
            self.creeps.remove(creepMort)  
    
        
    def creerTour(self, x, y, couleur):
        if self.verifierArgent(couleur) == True:
            if couleur == "rouge":
                self.tours.append(Tours.TourRouge(self, x , y, "rouge"))
            elif couleur == "orange":
                self.tours.append(Tours.TourOrange(self, x , y, "orange"))
            elif couleur == "jaune":
                self.tours.append(Tours.TourJaune(self, x , y, "jaune"))
            elif couleur == "mauve":
                self.tours.append(Tours.TourMauve(self, x , y, "mauve"))
            elif couleur == "cyan":
                self.tours.append(Tours.TourCyan(self, x , y, "cyan"))
            elif couleur == "blanc":
                self.tours.append(Tours.TourBlanc(self, x , y, "blanc"))
            elif couleur == "vert":
                self.tours.append(Tours.TourVert(self, x , y, "vert"))
            elif couleur == "magenta":
                self.tours.append(Tours.TourMagenta(self, x , y, "magenta"))
            elif couleur == "bleu":
                self.tours.append(Tours.TourBleu(self, x , y, "bleu"))
            return True
        else:
            return False
    
    def vendreTour(self, tourx, toury):
        for i in self.tours:
            if tourx == i.x and toury == i.y:
                self.argent += i.valeurTotale
                self.tours.remove(i)
    
    def upgraderTour(self,tourx,toury):
        for i in self.tours:
            if tourx == i.x and toury == i.y:
                if self.argent >= i.valeurUpgrade:
                    self.argent -= i.valeurUpgrade
                    i.niveauTour+=1 
                    i.upgradeTour()
                    
                    
         
    def verifierArgent(self, couleur):
        valeurAchat=0
        if couleur == "rouge":
            valeurAchat = Tours.TourRouge.valeurAchat
        elif couleur == "orange":
            valeurAchat = Tours.TourOrange.valeurAchat   
        elif couleur == "jaune":
            valeurAchat = Tours.TourJaune.valeurAchat   
        elif couleur == "mauve":
            valeurAchat = Tours.TourMauve.valeurAchat  
        elif couleur == "cyan":
            valeurAchat = Tours.TourCyan.valeurAchat
        elif couleur == "blanc":
            valeurAchat = Tours.TourBlanc.valeurAchat
        elif couleur == "vert":
            valeurAchat = Tours.TourVert.valeurAchat
        elif couleur == "magenta":
            valeurAchat = Tours.TourMagenta.valeurAchat
        elif couleur == "bleu":
            valeurAchat = Tours.TourBleu.valeurAchat
        
        if valeurAchat > self.argent:
            return False
        else:
            self.argent-=valeurAchat  
            return True
    
        
    def creerCreep(self,parent,x,y,listeDeCibles,type): #ciblex et cible y = coordonne de arrivee|| type = le type de creep
        if type == "normal": return Creeps.Creep(self,x,y,listeDeCibles)
        elif type == "gros": return Creeps.CreepGros(self,x,y,listeDeCibles)
        elif type == "rapide": return Creeps.CreepRapide(self,x,y,listeDeCibles)
        
    def creerBombe(self,x,y):
        self.bombePosition.append(Bombes.BombeDommage(self,x,y))# j'essaie avec bombe dommage 

    def supprimerBombe(self,x,y):
        self.bombePosition.clear()
    
    
    def testMouvementCreeps(self): # pour tester le mouvement des creeps
        c=Creeps.Creep(self,self.sentier[self.niveau-1][0],self.sentier[self.niveau-1][1],self.sentier)
        print(c.x,c.y)
        for i in range(200):
            c.deplacer()
    
    def randomTourBlanc(self, crit):
        self.randomPourcentage = random.randint(1,100)
        if self.randomPourcentage <= crit:
            return True
        else:
            return False
             
            
    def tourTir(self):
        self.tirerJouerCoup = False
        for t in self.tours: # dans la liste de creeps
            self.tirerJouerCoup = False 
            for c in self.creeps: # dans la liste de tours
                if t.couleur != "mauve" and t.couleur != "cyan" and self.tirerJouerCoup == False: #tours mauve et cyan ne tire pas
                    
                    if t.tirer(c) == 0: #methode tours tirer retourne 0 s'il doit lancer un projectile
                        if t.couleur == "blanc" and self.randomTourBlanc(t.pourcentageCrit):
                            self.projectiles.append(Projectiles.Projectile(self,t.x,t.y,"noir",c, t.degatBase))
                            c.pointDeVie=c.pointDeVie-t.degatCrit
                        elif t.couleur == "vert":
                            self.projectiles.append(Projectiles.Projectile(self,t.x,t.y,t.couleur,c,t.degatBase))
                            c.poison = t.dureePoison
                            c.pointDeVie=c.pointDeVie-t.degatBase   
                                   
                        else :
                            self.projectiles.append(Projectiles.Projectile(self,t.x,t.y,t.couleur,c, t.degatBase)) # creation de projectile dans la liste
                            c.pointDeVie=c.pointDeVie-t.degatBase
                               
                        if c.pointDeVie <= 0:  #Si le creeps meurt
                            if t.couleur == "jaune": #Calcul d'argent si creeps tue par tour jaune ou non
                                self.argent += c.retourArgent * t.facteurArgent
                                for v in self.creeps:
                                    if v is c:
                                        self.creeps.remove(c) #retirer le creeps de la liste s'il est more, a la fin
                            else:
                                self.argent+= c.retourArgent
                                for v in self.creeps:
                                    if v is c:
                                        self.creeps.remove(c) #retirer le creeps de la liste s'il est more, a la fin
                    
                    if t.verifDistance(c) == True:
                        self.tirerJouerCoup = True                    
                    
    def verificationCreep(self):
        for i in self.creeps :
            if i.y<=5:
                self.creeps.remove(i)
                self.nombreDeVie-=1
    
    def applyTourMauve(self):
        for t in self.tours:
            if t.couleur == "mauve":
                for t2 in self.tours:
                    distance = helper.Helper.calcDistance(t.x, t.y, t2.x, t2.y)
                    if distance < t.portee:
                         t2.vitesseTir = t2.vitesseTirDefault/t.facteurTir
                    else:
                        t2.vitesseTir = t2.vitesseTirDefault
    
    def applyTourCyan(self):
        for t in self.tours:
            if t.couleur == "cyan":
                for c in self.creeps:
                    distance = helper.Helper.calcDistance(t.x, t.y, c.x, c.y)
                    if distance < t.portee:
                        if c.vitesseBase != 1:
                            c.vitesse = c.vitesseBase/2
                    else:
                        c.vitesse = c.vitesseBase
    
    def applyPoison(self):                 
        for c in self.creeps:
            if c.poison != 0:
                c.poison -=1
                if c.poison % 20 == 0 :
                    c.pointDeVie -= 1
    
    def applyTourMagenta(self, h):
        for c in self.creeps:
            if helper.Helper.calcDistance(h.x, h.y, c.x, c.y) < 50:
                c.pointDeVie -= h.degat
            
            
                
    def jouerCoup(self):

        for i in self.creeps:
            i.deplacer()    #deplacement des creeps + verification du creep s'il arrive au point de fin de niveau
        #verification vie
        if self.nombreDeVie<=0:
            self.joueurMort=True
            return self.joueurMort
        self.applyTourCyan()
        self.applyTourMauve()
        self.applyPoison()
        self.tourTir()
        if self.timerCreeps==50:
            if self.compteurCreepsPartie < len(self.vagueCreeps):
                #vague de creeps par intervale de 5
                if self.compteurCreepsPartie==self.nombreCreepsParVague or self.compteurCreepsPartie==self.nombreCreepsParVague*2:
                    if len(self.creeps)==0:
                        while self.timerCreeps<=500:    #intervale de temps avant l'arrivee de chaque creep
                            self.timerCreeps+=1
                        self.compteurCreepsPartie+=1
                else:
                    self.creeps.append(self.vagueCreeps[self.compteurCreepsPartie]) #ajout des creeps de la vague dans la liste de creeps de partie
                    self.compteurCreepsPartie+=1
            else:
                if len(self.creeps)==0:
                    self.niveauFini=True
                    print("niveau fini")
                    #lancer splash screen prochain niv
                    return self.niveauFini #fin niveau
        
                     
            self.timerCreeps=0
        #incremente le timer
        self.timerCreeps+=1
        if len(self.projectiles) > 0:
            for h in self.projectiles:
                h.deplacer()
                if h.etat == "atteint":
                    if h.couleur == "magenta":
                        if h.aoe == 50:
                            self.applyTourMagenta(h)
                            self.projectiles.remove(h)
                        else :
                            h.aoe +=10 
                    else : 
                        self.projectiles.remove(h)
        self.bombeExplose()             
        #TODO : reste du jouercoup (... ce qui se refresh)
    
    def initProchainNiveau(self):
        self.timerCreeps=0
        self.compteurCreepsPartie=0
        self.creeps=[]
        self.vagueCreeps=[]
        self.tours=[]   
        self.sentier=[]
        self.projectiles=[]
        self.argent=600 # une tour de base vaut 100 et on veut qu'il puisse au moins avoir 2 tours
        self.bombe=1
        self.bombePosition=[]
        self.nombreCreepsParVague+=1  
        self.joueurMort=False
        self.niveauFini=False
    
class Modele():
    def __init__(self,parent):
        self.parent=parent
        self.largeur=800
        self.longueur=800
        self.partieCourante = None
        

    def lancerPartie(self):
        self.partieCourante=Partie(self.parent)
        self.partieCourante.creerNiveau()
        return self.partieCourante
    
    def chargerPartie(self):
        self.partieCourante=Partie(self.parent)
        self.partieCourante.loadSauvegarde()
        self.partieCourante.creerNiveau()
        return self.partieCourante
    
    def prochainNiveau(self):
        self.partieCourante.initProchainNiveau()
        self.partieCourante.creerNiveau()
        print("prochain niveau")
        return self.partieCourante
        
    def jouerCoup(self):
        #self.partieCourante.jouerCoup()
        rep=self.partieCourante.jouerCoup()
        if rep==True:
            if self.partieCourante.niveauFini==True:
                return self.prochainNiveau()
            else:
                return 0
        else:
            return self.partieCourante
    
    def creerTour(self,x,y,couleur):
        self.partieCourante.creerTour(x,y,couleur)
        return self.partieCourante
    
    def vendreTour(self,tourx,toury):
        self.partieCourante.vendreTour(tourx,toury)
        return self.partieCourante
    
    def upgraderTour(self,tourx,toury):
        self.partieCourante.upgraderTour(tourx,toury)
        return self.partieCourante
                 
    def creerBombe(self,x,y):
        self.partieCourante.creerBombe(x, y)
        return self.partieCourante
        
    def supprimerBombe(self,x,y):
        self.partieCourante.supprimerBombe(x, y)
        return self.partieCourante
    
