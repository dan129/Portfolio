import helper
import random

class Creep():
    vitesse=2 #2 pour le creep normal, va heriter de cette classe et changer les stats
    vitesseBase = 2
    pointDeVie = 10 # 5 pour le creep normal,  on va heriter dans autre class avec different stats
    retourArgent = 25
    poison = 0

    def __init__(self,parent,x,y,listDeCibles):
        self.parent=parent
        self.x=x
        self.y=y
        self.indexDeCibles=0
        self.listDeCibles = listDeCibles
        self.ciblex=self.listDeCibles[self.indexDeCibles][0]
        self.cibley=self.listDeCibles[self.indexDeCibles][1]
        self.poison=0
        self.type = "normal"
       
    
        
        
    def deplacer(self):
             

        self.x=int(self.x) 
        self.y=int(self.y)     # si on arrive pas encore à le point de cible, calcul de angle et calcul de prochain point       
        if self.x-self.vitesse> self.ciblex or self.y-self.vitesse > self.cibley or self.x+self.vitesse < self.ciblex or self.y+self.vitesse < self.cibley:
           self.angle=helper.Helper.calcAngle(self.x,self.y,
                                          self.ciblex,self.cibley)
           self.x,self.y=helper.Helper.getAngledPoint(self.angle,self.vitesse,
                                                       self.x,self.y)
            
            
        else: #si on arrive a le tronc de chemin, on change de cible chemin        
           if self.indexDeCibles < (len(self.listDeCibles)-1):
               self.indexDeCibles+=1
               self.ciblex=self.listDeCibles[self.indexDeCibles][0]
               self.cibley=self.listDeCibles[self.indexDeCibles][1] 
                  
                                 
        self.verificationCreep() # on verifie le creep s'il arrive au point de fin de niveau
        
    def verificationCreep(self):
            if self.y<=5:
                self.parent.creeps.remove(self)
                self.parent.nombreDeVie-=1
            
class CreepRapide(Creep):
    def __init__(self,parent,x,y,listDeCibles):
        Creep.__init__(self,parent,x,y,listDeCibles)
        self.vitesse = 4
        self.vitesseBase = 4
        self.pointDeVie = 7
        self.retourArgent = 20
        self.poison = 0
        self.type = "rapide"
        
class CreepGros(Creep):
    def __init__(self,parent,x,y,listDeCibles):
        Creep.__init__(self,parent,x,y,listDeCibles)
        self.vitesse = 1
        self.vitesseBase = 1
        self.pointDeVie=20
        self.retourArgent=40
        self.poison = 0
        self.type = "gros"
        

        