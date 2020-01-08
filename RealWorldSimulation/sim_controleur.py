# -*- coding: utf-8 -*-
import sys
import sim_monde
import sim_vue
import random

class Controleur():
    def __init__(self):
        self.modele = sim_monde.Monde(self)
        self.vue = sim_vue.Vue(self, self.modele)
        self.codeErreur = 0
        self.nbFramesSec = 24
        self.vue.root.mainloop()

    def demarrerSim(self, popAnimal, popVegetal, nivEau, elevTerrain, noyau):
        random.seed(noyau)
        self.modele.demarrerSim(popAnimal, popVegetal, nivEau, elevTerrain, noyau)
        self.vue.positionXCamera = 0
        self.vue.positionYCamera = 0
        self.vue.modifierTemps()
        self.vue.btnPause.configure(bg = "#292929",
                                    fg = "#FFFFFF",
                                    text = "Pauser la simulation")
        self.vue.afficheMonde()
        self.jouerSim()

    def reprendreSim(self):
        self.vue.afficheMonde()

        if self.modele.pauseHorsSim:
            self.pauserOuReprendre()
            self.modele.pauseHorsSim = False

    def retourMenu(self):
        if not self.modele.pause:
            self.pauserOuReprendre()
            self.modele.pauseHorsSim = True

        self.vue.afficherMenuPrincipal()

    def outilsSim(self):
        if not self.modele.pause:
            self.pauserOuReprendre()
            self.modele.pauseHorsSim = True

        self.vue.afficherOutilsSim()

    def pauserOuReprendre(self):
        if self.modele.pause:
            self.modele.pause = False
            self.vue.btnPause.configure(bg = "#292929",
                                        fg = "#FFFFFF",
                                        text = "Pauser la simulation")
            self.jouerSim()
        else:
            self.modele.pause = True
            self.vue.btnPause.configure(bg = "#FC0303",
                                        fg = "#FFFFFF",
                                        text = "Simulation pausée")


    def changerTemps(self, nouveauTemps):
        self.modele.multiplicateurTemps = nouveauTemps

    def ajouterElement(self, typeElement, coordX, coordY):
        self.modele.ajouterElement(typeElement, coordX, coordY)
        self.vue.afficherEnvironnement(echelle = self.vue.echelle)

    def supprimerElement(self, typeElement, coordX, coordY):
        self.modele.supprimerElement(typeElement, coordX, coordY)
        self.vue.afficherEnvironnement(echelle = self.vue.echelle)

    def jouerSim(self):
        self.modele.jouerSim()
        self.vue.modifierTemps()
        self.vue.modifierInspecteur()
        self.vue.modifierPopulations()
        self.vue.afficherEnvironnement(echelle = self.vue.echelle)

        if not self.modele.pause:
            self.vue.root.after(1000 // self.nbFramesSec, self.jouerSim)

    def quitter(self):
        self.vue.root.quit()

def main():
    controleur = Controleur()
    return controleur.codeErreur

if __name__ == '__main__':
    random.seed()
    print("Démarrage du programme de simulateur")
    resultat = main()
    print("Terminé avec le code:", resultat)
    sys.exit(resultat)