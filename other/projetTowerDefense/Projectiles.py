
import helper
import Creeps

class Projectile():
    vitesse = 1
    
    def __init__(self, parent, x,y,couleur, cible, degat): # cible == creep
        self.parent=parent
        self.x=x 
        self.y=y
        self.etat="notAtteint"
        self.aoe = 10
        self.couleur=couleur
        self.ciblex=cible.x
        self.cibley=cible.y
        self.angle=helper.Helper.calcAngle(self.x,self.y,self.ciblex,self.cibley)
        self.degat = degat
       
        #vitesse de projectiles selon la couleur de tour
        
        if self.couleur == "rouge":
            self.vitesse = 15
        
        elif self.couleur == "orange":
            self.vitesse = 8
        
        elif self.couleur == "jaune":
            self.vitesse = 10
            
        elif self.couleur == "blanc":
            self.vitesse = 10
        
        elif self.couleur == "noir":
            self.vitesse = 10
        
        elif self.couleur == "vert":
            self.vitesse = 10
        
        elif self.couleur == "magenta":
            self.vitesse = 10
            
        elif self.couleur == "bleu":
            self.vitesse = 20
        
        
        else : #A deleter quand toutes les couleurs seront faites
            self.vitesse = 0
        
    def deplacer(self):
        self.x=int(self.x)
        self.y=int(self.y)# si la projectile n'atteint pas encore le minion, on calcule l'angle et le prochain point du projectiles
        if self.x-self.vitesse> self.ciblex or self.y-self.vitesse > self.cibley or self.x+self.vitesse < self.ciblex or self.y+self.vitesse < self.cibley:
            self.angle=helper.Helper.calcAngle(self.x,self.y,
                                           self.ciblex,self.cibley)
            self.x,self.y=helper.Helper.getAngledPoint(self.angle,self.vitesse,
                                                        self.x,self.y)
            
        else: # projectile est atteints, on inflige le dégat
           self.parent.etatDeTir="degat"
           self.etat="atteint"
                 