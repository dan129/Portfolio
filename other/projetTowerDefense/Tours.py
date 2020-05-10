# -*- coding: UTF-8 -*-

import helper
import Creeps

class Tour():
    portee=10
    niveauTour=1
    compteurTir=1
    vitesseTir=4
    vitesseTirDefault = 30
    def __init__(self, parent, x, y, couleur):
        self.parent=parent
        self.x=x 
        self.y=y
        self.couleur=couleur
        self.etatDeTir="nothing"
        
        
    def tirer(self, creep):  #Méthode générale qui permet à chaque tour de tirer
        distance = helper.Helper.calcDistance(self.x, self.y, creep.x, creep.y)
        if self.etatDeTir is "degat":
            self.etatDeTir="nothing"
        if distance < self.portee:
            self.compteurTir+=1
           
            if self.compteurTir >= self.vitesseTir:
                self.compteurTir=1
                return 0;
            else:
                return 1
    
    def verifDistance(self, creep):
         distance = helper.Helper.calcDistance(self.x, self.y, creep.x, creep.y)
         if distance < self.portee:
             return True
         else:
             return False 
        
class TourRouge(Tour):
    portee=100
    valeurAchat=100
    valeurUpgrade=0
    valeurTotale=0
    degatBase=5
    vitesseTir=30  #Chaque fois que le compteur arrive à vitesseTir, la tour va tirer. 
    vitesseTirDefault = 30
    def __init__(self, parent, x, y, couleur):
        Tour.__init__(self, parent, x, y, "rouge")
        
        #Valeur de base de chaque tours
        self.niveauTour = Tour.niveauTour
        self.compteurTir = Tour.compteurTir
        
        #Valeurs spécifique à la tour
        self.portee=TourRouge.portee
        self.valeurDepensee=TourRouge.valeurAchat
        self.degatBase=TourRouge.degatBase+(self.niveauTour)
        self.vitesseTir=TourRouge.vitesseTir
        self.vitesseTirDefault=TourRouge.vitesseTirDefault
        self.valeurTotale=TourRouge.valeurAchat
        self.valeurUpgrade=TourRouge.valeurAchat*self.niveauTour 
        
    def upgradeTour(self): #Ce qui est upgraded specifiquement a chaque tour
        self.degatBase +=1
        self.valeurTotale += self.valeurUpgrade
        self.valeurUpgrade = self.valeurAchat*self.niveauTour 
        
class TourOrange(Tour):
    portee=70
    valeurAchat=100
    valeurTotale=0
    valeurUpgrade=0
    degatBase=1
    vitesseTir=15  #Chaque fois que le compteur arrive à vitesseTir, la tour va tirer. 
    vitesseTirDefault = 15
    
    def __init__(self, parent, x, y, couleur):
        Tour.__init__(self, parent, x, y, "orange")
        
        #Valeur de base de chaque tours
        self.niveauTour = Tour.niveauTour
        self.compteurTir = Tour.compteurTir
        
        #Valeurs spécifique à la tour
        self.portee=TourOrange.portee
        self.valeurDepensee=TourOrange.valeurAchat
        self.degatBase=TourOrange.degatBase
        self.vitesseTir=TourOrange.vitesseTir-self.niveauTour
        self.vitesseTirDefault=TourOrange.vitesseTirDefault
        self.valeurTotale=TourOrange.valeurAchat
        self.valeurUpgrade=TourOrange.valeurAchat*self.niveauTour 
    
    def upgradeTour(self): #Ce qui est upgraded specifiquement a chaque tour
        self.vitesseTir -= 1
        self.valeurTotale += self.valeurUpgrade
        self.valeurUpgrade = self.valeurAchat*self.niveauTour 
        

class TourJaune(Tour):
    portee=80
    valeurAchat=175
    valeurTotale=0
    valeurUpgrade=0
    degatBase=1
    vitesseTir=20  #Chaque fois que le compteur arrive à vitesseTir, la tour va tirer. 
    vitesseTirDefault = 20
    facteurArgent=1
    
    def __init__(self, parent, x, y, couleur):
        Tour.__init__(self, parent, x, y, "jaune")
        
        #Valeur de base de chaque tours
        self.niveauTour = Tour.niveauTour
        self.compteurTir = Tour.compteurTir
        
        #Valeurs spécifique à la tour
        self.portee=TourJaune.portee
        self.valeurDepensee=TourJaune.valeurAchat
        self.degatBase=TourJaune.degatBase
        self.vitesseTir=TourJaune.vitesseTir
        self.vitesseTirDefault=TourJaune.vitesseTirDefault
        self.facteurArgent= TourJaune.facteurArgent+(self.niveauTour*0.35)
        self.valeurTotale=TourJaune.valeurAchat
        self.valeurUpgrade=TourJaune.valeurAchat*self.niveauTour 
        
    def upgradeTour(self): #Ce qui est upgraded specifiquement a chaque tour
        self.facteurArgent += 0.35
        self.valeurTotale += self.valeurUpgrade
        self.valeurUpgrade = self.valeurAchat*self.niveauTour 
        
class TourCyan(Tour):
    portee=50
    valeurAchat=150
    valeurTotale=0
    valeurUpgrade=0
    degatBase=0
    vitesseTir=0  #Chaque fois que le compteur arrive à vitesseTir, la tour va tirer. 
    vitesseTirDefault = 0
    
    def __init__(self, parent, x, y, couleur):
        Tour.__init__(self, parent, x, y, "cyan")
        
        #Valeur de base de chaque tours
        self.niveauTour = Tour.niveauTour
        self.compteurTir = Tour.compteurTir
        
        #Valeurs spécifique à la tour
        self.portee=TourCyan.portee
        self.valeurDepensee=TourCyan.valeurAchat
        self.degatBase=TourCyan.degatBase
        self.vitesseTir=TourCyan.vitesseTir
        self.valeurTotale=TourCyan.valeurAchat
        self.valeurUpgrade=TourCyan.valeurAchat*self.niveauTour 
    
    def upgradeTour(self): #Ce qui est upgraded specifiquement a chaque tour
        self.portee += 25
        self.valeurTotale += self.valeurUpgrade
        self.valeurUpgrade = self.valeurAchat*self.niveauTour 
        
class TourMauve(Tour):
    portee=50
    valeurAchat=100
    valeurTotale=0
    valeurUpgrade=0
    degatBase=0
    vitesseTir=0  #Chaque fois que le compteur arrive à vitesseTir, la tour va tirer. 
    vitesseTirDefault = 0
    facteurTir=1
    def __init__(self, parent, x, y, couleur):
        Tour.__init__(self, parent, x, y, "mauve")
        
        #Valeur de base de chaque tours
        self.niveauTour = Tour.niveauTour
        self.compteurTir = Tour.compteurTir
        
        #Valeurs spécifique à la tour
        self.portee=TourMauve.portee
        self.valeurDepensee=TourMauve.valeurAchat
        self.degatBase=TourMauve.degatBase
        self.vitesseTir=TourMauve.vitesseTir
        self.facteurTir=TourMauve.facteurTir+(self.niveauTour*0.25)
        self.valeurTotale=TourMauve.valeurAchat
        self.valeurUpgrade=TourMauve.valeurAchat*self.niveauTour 
    
    def upgradeTour(self): #Ce qui est upgraded specifiquement a chaque tour
        self.facteurTir += 0.25
        self.valeurTotale += self.valeurUpgrade
        self.valeurUpgrade = self.valeurAchat*self.niveauTour 
        
class TourBlanc(Tour):
    portee=80
    valeurAchat=200
    valeurTotale=0
    valeurUpgrade=0
    degatBase=3
    degatCrit=9
    vitesseTir=25  #Chaque fois que le compteur arrive à vitesseTir, la tour va tirer. 
    vitesseTirDefault = 25
    pourcentageCrit = 10
    def __init__(self, parent, x, y, couleur):
        Tour.__init__(self, parent, x, y, "blanc")
        
        #Valeur de base de chaque tours
        self.niveauTour = Tour.niveauTour
        self.compteurTir = Tour.compteurTir
        
        #Valeurs spécifique à la tour
        self.portee=TourBlanc.portee
        self.valeurDepensee=TourBlanc.valeurAchat
        self.degatBase=TourBlanc.degatBase
        self.vitesseTir=TourBlanc.vitesseTir
        self.valeurTotale=TourBlanc.valeurAchat
        self.valeurUpgrade=TourBlanc.valeurAchat*self.niveauTour 
    
    def upgradeTour(self): #Ce qui est upgraded specifiquement a chaque tour
        self.pourcentageCrit += 5
        self.valeurTotale += self.valeurUpgrade
        self.valeurUpgrade = self.valeurAchat*self.niveauTour 
        
class TourVert(Tour):
    portee=80
    valeurAchat=150
    valeurTotale=0
    valeurUpgrade=0
    degatBase=1
    degatPoison=0
    vitesseTir=40  #Chaque fois que le compteur arrive à vitesseTir, la tour va tirer. 
    vitesseTirDefault = 40
    dureePoison=120
    
    def __init__(self, parent, x, y, couleur):
        Tour.__init__(self, parent, x, y, "vert")
        
        #Valeur de base de chaque tours
        self.niveauTour = Tour.niveauTour
        self.compteurTir = Tour.compteurTir
        
        #Valeurs spécifique à la tour
        self.portee=TourVert.portee
        self.valeurDepensee=TourVert.valeurAchat
        self.degatBase=TourVert.degatBase
        self.vitesseTir=TourVert.vitesseTir
        self.valeurTotale=TourVert.valeurAchat
        self.valeurUpgrade=TourVert.valeurAchat*self.niveauTour 
    
    def upgradeTour(self): #Ce qui est upgraded specifiquement a chaque tour
        self.dureePoison+=20
        self.valeurTotale += self.valeurUpgrade
        self.valeurUpgrade = self.valeurAchat*self.niveauTour 
        
class TourMagenta(Tour):
    portee=100
    valeurAchat=200
    valeurTotale=0
    valeurUpgrade=0
    degatBase=2
    vitesseTir=30  #Chaque fois que le compteur arrive à vitesseTir, la tour va tirer. 
    vitesseTirDefault = 30
    
    
    def __init__(self, parent, x, y, couleur):
        Tour.__init__(self, parent, x, y, "magenta")
        
        #Valeur de base de chaque tours
        self.niveauTour = Tour.niveauTour
        self.compteurTir = Tour.compteurTir
        
        #Valeurs spécifique à la tour
        self.portee=TourMagenta.portee
        self.valeurDepensee=TourMagenta.valeurAchat
        self.degatBase=TourMagenta.degatBase
        self.vitesseTir=TourMagenta.vitesseTir
        self.valeurTotale=TourMagenta.valeurAchat
        self.valeurUpgrade=TourMagenta.valeurAchat*self.niveauTour 
    
    def upgradeTour(self): #Ce qui est upgraded specifiquement a chaque tour
        self.degatBase += 1
        self.valeurTotale += self.valeurUpgrade
        self.valeurUpgrade = self.valeurAchat*self.niveauTour

class TourBleu(Tour):
    portee=200
    valeurAchat=200
    valeurUpgrade=0
    valeurTotale=0
    degatBase=7
    vitesseTir=60  #Chaque fois que le compteur arrive à vitesseTir, la tour va tirer. 
    vitesseTirDefault = 60
    def __init__(self, parent, x, y, couleur):
        Tour.__init__(self, parent, x, y, "bleu")
        
        #Valeur de base de chaque tours
        self.niveauTour = Tour.niveauTour
        self.compteurTir = Tour.compteurTir
        
        #Valeurs spécifique à la tour
        self.portee=TourBleu.portee
        self.valeurDepensee=TourBleu.valeurAchat
        self.degatBase=TourBleu.degatBase+(self.niveauTour)
        self.vitesseTir=TourBleu.vitesseTir
        self.vitesseTirDefault=TourBleu.vitesseTirDefault
        self.valeurTotale=TourBleu.valeurAchat
        self.valeurUpgrade=TourBleu.valeurAchat*self.niveauTour 
        
    def upgradeTour(self): #Ce qui est upgraded specifiquement a chaque tour
        self.degatBase +=1
        self.vitesseTir -=2
        self.vitesseTirDefault -=2
        self.valeurTotale += self.valeurUpgrade
        self.valeurUpgrade = self.valeurAchat*self.niveauTour 
            
#Tests � deleter
if __name__ == '__main__':
    
    tr=TourRouge(1,1,1,1)
    tj=TourJaune(1,1,1,1)
    print(tr.portee, tr.niveauTour, tr.degatBase, tr.vitesseTir, tr.valeurDepensee)
    print(tj.facteurArgent)
        
        
        