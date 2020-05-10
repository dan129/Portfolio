import Vue
import Modele
import Creeps

class Controleur():
    def __init__(self):
        self.vue=Vue.Vue(self)
        self.modele=Modele.Modele(self)
        self.partie=Modele.Partie(self)
        self.vue.mod=self.modele
        self.vue.menuPrincipal()
        
        self.vue.root.mainloop() 
        
    def jouerCoup(self):
        self.vue.raffraichirSurfaceJeu()
        rep=self.modele.jouerCoup() 
        if rep==0:
            self.vue.menuFinDeNiveau()
        self.vue.afficherEtatJeu()
        if self.vue.pause==False and self.vue.quitte==False and rep!=0:
            self.vue.root.after(50,self.jouerCoup)
        
    def menuMilieuPartie(self):
        self.vue.menuFinDeNiveau()
        
    def lancerPartie(self):
        rep=self.modele.lancerPartie()
        self.vue.root.after(1000,self.jouerCoup)
        return rep
    
    def chargerPartie(self):
        rep = self.modele.chargerPartie()
        self.vue.root.after(1000,self.jouerCoup)
        return rep
        
    def prochainNiveau(self):
        rep = self.modele.initProchainNiveau()
        return self.modele.partieCourante
    
    def acheterTour(self,x,y,couleur):
        rep=self.modele.creerTour(x,y,couleur)
        return rep
    
    def vendreTour(self,tourx,toury):
        rep=self.modele.vendreTour(tourx,toury)
        return rep
    
    def upgraderTour(self,tourx,toury):
        rep=self.modele.upgraderTour(tourx,toury)
        return rep
    
    def utiliserBombe(self,x,y):
        rep=self.modele.creerBombe(x,y)
        return rep
    
    def enleverBombe(self,x,y):
        rep=self.modele.supprimerBombe(x,y)
        return rep
    
if __name__ == '__main__':
    c=Controleur()
     
    
    