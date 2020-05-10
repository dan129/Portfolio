from tkinter import *
import Modele
import Tours
from tkinter.constants import TOP
#import pyautogui
from PIL import ImageTk
from tkinter import messagebox


class Vue():
    def __init__(self, parent):
        self.parent=parent
        self.root=Tk()
        self.root.title("Tower Defense")
        
        self.root["bg"] = "black"
        self.root.geometry("1200x850")
        self.mod = None
        self.couleurTourAcheter = None
        self.tourSelectionee = False
        self.compteurBombe=0
        self.couleurProjectile=None
        self.timerBomb = 0
        self.x=0 # pour la bombe
        self.y=0# pour la bombe
        self.incrementationTimerBomb = 0
        self.tourx = 0
        self.toury = 0
        self.pause=False
        self.quitte=False

        self.effetCyan = 5
        self.effetMagenta = 1
        self.tailleTexteBoutons=13
        self.imageSurfaceDessin = ImageTk.PhotoImage(file = "dessinPhotoshop.jpg")


        self.effetCyan = 5

        self.tailleTexteBoutons=13
        self.imageSurfaceDessin = ImageTk.PhotoImage(file = "dessinPhotoshop.jpg")


    
    def menuPrincipal(self): #Methode qui appelle le menu principal
        self.cadreMenuP=Frame(self.root)
        self.cadreMenuP.pack(fill="none", expand=True)

        self.btnJouer=Button(self.cadreMenuP,padx=170,pady=40,text="  Jouer   ",font=("Helvetica", 30),bg="grey",command=self.lancerPartie)
        self.btnScore=Button(self.cadreMenuP,padx=170,pady=40,text="Score",font=("Helvetica", 30),bg="grey",command=lambda : print("charger score"))
        self.btnChargerPartie=Button(self.cadreMenuP,padx=170,pady=40,text=" Charger partie  ",font=("Helvetica", 30),bg="grey", command=lambda : self.chargerPartie())
        
        self.btnJouer.pack(fill=BOTH, expand=1)
        self.btnScore.pack(fill=BOTH, expand=1)
        self.btnChargerPartie.pack(fill=BOTH, expand=1)
        
        
    def lancerPartie(self): 
        rep = self.parent.lancerPartie()
        self.mod=rep
        self.dessineSurfaceJeu()
    
    def chargerPartie(self):
        rep = self.parent.chargerPartie()
        self.mod=rep
        self.dessineSurfaceJeu()
    
    def prochainNiveau(self):
        rep = self.parent.prochainNiveau()
        self.mod=rep
        self.dessineSurfaceJeu()
    
    def raffraichirSurfaceJeu(self): #Delete le sentier et le reaffiche en fonction des coord du sentier
        self.surface.delete("sentier")
        couleur="black" 
        self.surface.create_line(self.mod.sentier, width=20, fill=couleur, tags = ("sentier"))
        
        
    def acheterTour(self,eventx, eventy, couleur):
        nbToursAvant = len(self.mod.tours)
        rep=self.parent.acheterTour(eventx,eventy, couleur)
        self.mod = rep
        nbToursApres = len(self.mod.tours)
        if (nbToursAvant == nbToursApres):
            self.manqueArgent()
        else:
            self.afficherStatsTourExistante(eventx, eventy)
            
    def vendreTour(self):
        if self.tourSelectionee == False:
            self.labelInfoTours.config(fg = "white", text = "Selectionnez une tour avant de cliquer sur Vendre Tour")
        else:
            rep = self.parent.vendreTour(self.tourx, self.toury)
            self.mod = rep
            self.tourSelectionee = False
    
    def upgraderTour(self):
        argentAvant = self.mod.argent
        if self.tourSelectionee == False:
            self.labelInfoTours.config(fg = "white", text = "Selectionnez une tour avant de cliquer sur Vendre Tour")
        else:
            rep = self.parent.upgraderTour(self.tourx, self.toury)
            self.mod = rep
            self.afficherStatsTourExistante(self.tourx, self.toury)
            argentApres = self.mod.argent
            if (argentAvant == argentApres):
                self.manqueArgent()
                self.tourSelectionee = False
     
    def dessineSurfaceJeu(self): #Methode qui n'est appelee qu'une seule fois au debut du niveau
        
        couleurTours = None
        self.cadreMenuP.pack_forget()
        self.cadreJeu=Frame(self.root)
        self.cadreJeu.pack(side=LEFT, padx=10) 
        
        self.surface=Canvas(self.cadreJeu,width=800,
                            height=self.mod.longueur,
                            bg="green")
        self.surface.create_image(0, 0, image = self.imageSurfaceDessin, anchor = NW)
        self.surface.pack(expand = YES, fill = BOTH)
      
        couleur="black" 
        self.surface.create_line(self.mod.sentier, width=20, fill=couleur, tags = ("sentier"))     
            
        
        self.cadreBoutons = Frame(self.root, width=200, height=400, background = "black", highlightbackground="white", highlightcolor="white", highlightthickness=1)
        self.cadreBoutons.pack(side=TOP, pady=10)
        self.FrameInfoTours = Frame(self.root, width=280, height=400, background = "black", highlightbackground="white", highlightcolor="white", highlightthickness=1)
        self.FrameInfoTours.pack(side=TOP, pady=10)
        self.labelInfoTours = Label(self.FrameInfoTours, width=280, height=400, background = "black", padx = 2, pady = 2, text="")
        self.labelInfoTours.pack(side = TOP)
        self.labelInfoTours.config(fg = "white", text = 
                                   "Vous avez 5 secondes pour placer des tours" + 
                                   "\navant que les creeps soient lances")
        
       #variables 
        self.hauteur=2
        self.long=18
        self.styleEcriture="Helvetica,18,bold"
        
        self.btnAcheterTourRouge=Button(self.cadreBoutons,width = self.long, height = self.hauteur ,text="Tour rouge",font=(self.styleEcriture),bg="red",command=lambda: self.afficherStatsTourAcheter("rouge"))
        self.btnAcheterTourOrange=Button(self.cadreBoutons,width = self.long, height = self.hauteur ,text="Tour orange",font=(self.styleEcriture),bg="orange",command=lambda: self.afficherStatsTourAcheter("orange"))
        self.btnAcheterTourJaune=Button(self.cadreBoutons,width = self.long, height = self.hauteur ,text="Tour jaune",font=(self.styleEcriture),bg="yellow",command=lambda: self.afficherStatsTourAcheter("jaune"))
        self.btnAcheterTourVerte=Button(self.cadreBoutons,width = self.long, height = self.hauteur ,text="Tour verte",font=(self.styleEcriture),bg="yellow green",command=lambda: self.afficherStatsTourAcheter("vert"))
        self.btnAcheterTourCyan=Button(self.cadreBoutons,width = self.long, height = self.hauteur ,text="Tour cyan",font=(self.styleEcriture),bg="cyan2",command=lambda: self.afficherStatsTourAcheter("cyan"))
        self.btnAcheterTourMagenta=Button(self.cadreBoutons,width = self.long, height = self.hauteur ,text="Tour magenta",font=(self.styleEcriture),bg="magenta2",command=lambda: self.afficherStatsTourAcheter("magenta"))
        self.btnAcheterTourBleue=Button(self.cadreBoutons,width = self.long, height = self.hauteur ,text="Tour bleue",font=(self.styleEcriture),bg="royal blue",command=lambda: self.afficherStatsTourAcheter("bleu"))
        self.btnAcheterTourBlanche=Button(self.cadreBoutons,width = self.long, height = self.hauteur ,text="Tour blanche",font=(self.styleEcriture),bg="white",command=lambda: self.afficherStatsTourAcheter("blanc"))
        self.btnAcheterTourMauve=Button(self.cadreBoutons,width = self.long, height = self.hauteur, text="Tour mauve",font=(self.styleEcriture),bg="purple",command=lambda: self.afficherStatsTourAcheter("mauve"))
        
        self.btnVendreTour=Button(self.cadreBoutons, width = 15, height =1 ,text="Vendre tour",bg="grey",command=lambda: self.vendreTour())
        self.btnAmeliorerTour=Button(self.cadreBoutons,width = 15, height =1,text="Upgrader tour",bg="grey",command=lambda: self.upgraderTour())
        self.btnLancerBombe=Button(self.cadreBoutons,width = 15, height =1,text="Lancer bombe",bg="grey",command=lambda:  self.afficherBombe())
        self.btnPause=Button(self.cadreBoutons,width = 15, height =1,text="Pause/Jeu",bg="grey",command=self.pauseJeu)
        self.btnJouer=Button(self.cadreBoutons,width = 15, height =1,text="Sauvegarder",bg="grey",command=lambda: print("save"))
        self.btnQuitter=Button(self.cadreBoutons,width = 15, height =1,text="Quitter",bg="grey",command=self.quitterJeu)
        
        self.paddingy=2
        
        self.btnAcheterTourRouge.grid(column=0, row=0,  pady=self.paddingy, padx=4)
        self.btnAcheterTourOrange.grid(column=0, row=1, pady=self.paddingy, padx=4)
        self.btnAcheterTourJaune.grid(column=0, row=2, pady=self.paddingy, padx=4)
        self.btnAcheterTourVerte.grid(column=0, row=3, pady=self.paddingy, padx=4)
        self.btnAcheterTourCyan.grid(column=0, row=4, pady=self.paddingy, padx=4)
        self.btnAcheterTourMagenta.grid(column=0, row=5, pady=self.paddingy, padx=4)
        self.btnAcheterTourBleue.grid(column=0, row=6, pady=self.paddingy, padx=4)
        self.btnAcheterTourBlanche.grid(column=0, row=7, pady=self.paddingy, padx=4)
        self.btnAcheterTourMauve.grid(column=0, row=8, pady=self.paddingy, padx=4)


        
        self.btnVendreTour.grid(column=0, row=9)
        self.btnAmeliorerTour.grid(column=1, row=9)
        self.btnLancerBombe.grid(column=0, row=10)
        self.btnPause.grid(column=1, row=10)
        self.btnJouer.grid(column=0, row=11)
        self.btnQuitter.grid(column=1, row=11)
        
        self.cadreInfoPartie = Frame(self.cadreJeu)
        self.cadreInfoPartie.pack()
        
        self.labelVie=Label(self.cadreInfoPartie,padx=5,pady=2,text="Vie : "+ str(self.mod.nombreDeVie),font=("Helvetica", self.tailleTexteBoutons),bg="grey")
        self.labelNiveau=Label(self.cadreInfoPartie,padx=5,pady=2,text="Niveau : "+ str(self.mod.niveau),font=("Helvetica", self.tailleTexteBoutons),bg="grey")
        self.labelArgent=Label(self.cadreInfoPartie,padx=5,pady=2,text="Argent : "+ str(self.mod.argent),font=("Helvetica", self.tailleTexteBoutons),bg="grey")
        self.labelVagueActive=Label(self.cadreInfoPartie,padx=5,pady=2,text="VagueActive : " + str(self.mod.niveau),font=("Helvetica", self.tailleTexteBoutons),bg="grey")
        self.labelBombe=Label(self.cadreInfoPartie,padx=5,pady=2,text="Bombe Disponible: "+ str(self.mod.bombe),font=("Helvetica", self.tailleTexteBoutons),bg="grey")
        self.labelVie.grid(column=0, row=0)
        self.labelNiveau.grid(column=1, row=0)
        self.labelArgent.grid(column=2, row=0)
        self.labelVagueActive.grid(column=3, row=0)
        self.labelBombe.grid(column=4, row=0) 
        
        self.surface.bind("<Button-1>", self.canvasClicked)
        self.surface.bind("<Button-3>",self.bombeCanvasClick)
        
    def afficherLabelBas(self):  #Methode appelee a chaque AfficherEtat, pour refresh le label du bas
       self.labelVie.config(fg = "black", text="Vie : "+ str(self.mod.nombreDeVie))
       self.labelNiveau.config(fg = "black", text="Niveau : "+ str(self.mod.niveau))
       self.labelArgent.config(fg = "black", text="Argent : "+ str(self.mod.argent))
       self.labelVagueActive.config(fg = "black", text="Vague Active : "+ str(self.mod.niveau))
       self.labelBombe.config(fg = "black", text="Bombe Disponible : "+ str(self.mod.bombe))
       
        
        
    def traductionCouleur(self,couleur): #Servant a traduire l'attribut couleur de chaque tour et l'utiliser pour dessiner les tours ou projectile
        if couleur == "rouge":
            return "red"
        elif couleur == "orange":
            return "orange"
        elif couleur == "jaune":
            return "yellow"
        elif couleur == "vert":
            return "lightgreen"
        elif couleur == "cyan":
            return "lightblue"
        elif couleur == "magenta":
            return "magenta"
        elif couleur == "bleu":
            return "blue"
        elif couleur == "blanc":
            return "white"
        elif couleur == "mauve":
            return "purple"
        elif couleur == "noir":
            return "black"
        
    def afficherEtatJeu(self): #Appelee a chaque jouer coup
        timerRefresh=0     
        self.surface.delete("creep")
        self.surface.delete("projectile")
        self.surface.delete("tours")
        self.surface.delete("effetvague")
        
        if self.mod.niveau%5==1 :
            timerRefresh=50  
        elif self.mod.niveau%5==2 :
            timerRefresh=100
        elif self.mod.niveau%5==3 :
           timerRefresh=150
        elif self.mod.niveau%5==4 :
           timerRefresh=200
        else :
            timerRefresh=200
        if self.timerBomb == timerRefresh:
                self.surface.delete("bombe")
                self.incrementationTimerBomb = 0
        if self.compteurBombe < 1 and self.incrementationTimerBomb == 1:
            self.surface.create_oval(self.x-20,self.y-20,self.x+20,self.y+20,fill= "black",tags="bombe")
            self.timerBomb+=1
        t=10
      
        tProjectile=3
        for tour in self.mod.tours:
            couleurADessiner = self.traductionCouleur(tour.couleur) 
            self.surface.create_rectangle(tour.x-t,tour.y-t,tour.x+t,tour.y+t,fill=couleurADessiner, tags=("tours"))
            if tour.couleur == "cyan":
                 self.surface.create_oval(tour.x - self.effetCyan, tour.y - self.effetCyan, tour.x + self.effetCyan, tour.y + self.effetCyan, outline ="lightblue", fill=None, tags=("effetvague"))
                 self.effetCyan+=2
                 if self.effetCyan >= tour.portee:
                     self.effetCyan = 5
            elif tour.couleur == "mauve":
                 self.surface.create_oval(tour.x - tour.portee, tour.y - tour.portee, tour.x + tour.portee, tour.y + tour.portee, outline="purple", fill = None, tags=("tours"))
                
                
        for creep in self.mod.creeps:
            if creep.type == "gros":
                self.surface.create_oval(creep.x-t,creep.y-t,creep.x+t,creep.y+t,fill="lightblue", tags=("creep"))
            elif creep.type == "normal":
                self.surface.create_oval(creep.x-7,creep.y-7,creep.x+7,creep.y+7,fill="red", tags=("creep"))
            elif creep.type == "rapide":
                self.surface.create_oval(creep.x-4,creep.y-4,creep.x+4,creep.y+4,fill="yellow", tags=("creep"))
                
            if creep.poison != 0:
                self.surface.create_oval(creep.x-2,creep.y-2,creep.x+2,creep.y+2,fill="green", tags=("creep"))
                

            
            for lesProjectiles in self.mod.projectiles:
                self.couleurProjectile=(self.traductionCouleur(lesProjectiles.couleur))
                self.surface.create_rectangle(lesProjectiles.x-tProjectile,lesProjectiles.y-tProjectile,lesProjectiles.x+tProjectile,lesProjectiles.y+tProjectile,fill=self.couleurProjectile,tags=("projectile"))   
                if lesProjectiles.couleur == "magenta" and lesProjectiles.etat == "atteint":
                    self.surface.create_oval(lesProjectiles.x - lesProjectiles.aoe, lesProjectiles.y - lesProjectiles.aoe, lesProjectiles.x + lesProjectiles.aoe, lesProjectiles.y + lesProjectiles.aoe, outline ="magenta", fill=None, tags=("effetvague"))
                    
            
            self.afficherLabelBas()
        else:
           return 0
        return 1

        if self.mod.niveauFini == True:
            self.prochainNiveau()
        
    def afficherBombe(self):
        self.compteurBombe=self.mod.bombe
        
    def bombeCanvasClick(self,event):
        if self.compteurBombe<1 :
            pyautogui.alert('La Bombe a ete utilisee dans le passe')
        elif self.compteurBombe==1:
            self.x= event.x
            self.y=event.y
            print(" X ", self.x)
            print("Y " , self.y)
            if self.verifOverlapSentier(self.x, self.y)== True:#s'il ne se retrouve pas sur le sentier 
                self.compteurBombe+=1
                pyautogui.alert("en dehors du sentier")
            else :
                self.surface.create_oval(self.x-20,self.y-20,self.x+20,self.y+20,fill= "black",tags="bombe")
                self.compteurBombe-=1     
                self.incrementationTimerBomb+=1
                self.mod.bombe=0  
            rep = self.parent.utiliserBombe(self.x,self.y)
            self.mod= rep
            #la bombe explose et elle se supprime 
            self.mod.bombeExplose()
            self.mod.supprimerBombe(self.x,self.y)
           
    def afficherStatsTourAcheter (self,couleurTour): #Est appelee avant qu'une tour soit achetee
        if couleurTour == "rouge":
            self.labelInfoTours.config(fg = "white", text = 
                                        "Tour " + couleurTour + ": Niveau 1" + 
                                    "\n Prix: "+ str(Tours.TourRouge.valeurAchat) +
                                    "\n Dommage: "+ str(Tours.TourRouge.degatBase) +
                                    "\n Portee: "+ str(Tours.TourRouge.portee) +
                                    "\n Delai de tir: "+ str(Tours.TourRouge.vitesseTir) +
                                    "\n\n Une tour lente qui tire loin et plus forte" +
                                    "\n\n\n Cliquez sur le terrain ou vous voulez placer cette tour")
            
        elif couleurTour == "orange":
           self.labelInfoTours.config(fg = "white", text = 
                                        "Tour " + couleurTour + ": Niveau 1" + 
                                    "\n Prix: "+ str(Tours.TourOrange.valeurAchat) +
                                    "\n Dommage: "+ str(Tours.TourOrange.degatBase) +
                                    "\n Portee: "+ str(Tours.TourOrange.portee) +
                                    "\n Delai de tir: "+ str(Tours.TourOrange.vitesseTir) +
                                    "\n\n Une tour rapide, qui tire moins loin et moins forte"+
                                    "\n\n\n Cliquez sur le terrain ou vous voulez placer cette tour")
           
        elif couleurTour == "jaune":
           self.labelInfoTours.config(fg = "white", text = 
                                        "Tour " + couleurTour + ": Niveau 1" + 
                                    "\n Prix: "+ str(Tours.TourJaune.valeurAchat) +
                                    "\n Dommage: "+ str(Tours.TourJaune.degatBase) +
                                    "\n Portee: "+ str(Tours.TourJaune.portee) +
                                    "\n Delai de tir: "+ str(Tours.TourJaune.vitesseTir) +
                                    "\n\n Une tour faible qui rapporte plus d'argent si elle tue le creep"+
                                    "\n\n\n Cliquez sur le terrain ou vous voulez placer cette tour")  
           
        elif couleurTour == "mauve":
           self.labelInfoTours.config(fg = "white", text = 
                                        "Tour " + couleurTour + ": Niveau 1" + 
                                    "\n Prix: "+ str(Tours.TourMauve.valeurAchat) +
                                    "\n Portee: "+ str(Tours.TourMauve.portee) +
                                    "\n Facteur Rapidite: "+ str(Tours.TourMauve.facteurTir) +
                                    "\n\n Une tour qui ne tire pas, mais qui augmente la rapidite"+
                                    "\n des autre tour dans sa portee."+
                                    "\n\n\n Cliquez sur le terrain ou vous voulez placer cette tour")  
        elif couleurTour == "cyan":
           self.labelInfoTours.config(fg = "white", text = 
                                        "Tour " + couleurTour + ": Niveau 1" + 
                                    "\n Prix: "+ str(Tours.TourCyan.valeurAchat) +
                                    "\n Portee: "+ str(Tours.TourCyan.portee) +
                                    "\n\n Une tour qui ne tire pas, mais qui reduit la vitesse " +
                                    "\n des creeps dans sa portee" +
                                    "\n\n\n Cliquez sur le terrain ou vous voulez placer cette tour")
        elif couleurTour == "blanc":
           self.labelInfoTours.config(fg = "white", text = 
                                        "Tour " + couleurTour + ": Niveau 1" + 
                                    "\n Dommage: "+ str(Tours.TourBlanc.degatBase) +
                                    "\n Portee: "+ str(Tours.TourBlanc.portee) +
                                    "\n Delai de tir: "+ str(Tours.TourBlanc.vitesseTir) +
                                    "\n Pourcentage Triple Dommage : "+ str(Tours.TourBlanc.pourcentageCrit) + " %" +
                                    "\n\n Une tour relativement faible mais ayant une chance " +
                                    "\n de tirer un projectile pour triple dommage" +
                                    "\n\n\n Cliquez sur le terrain ou vous voulez placer cette tour")
        elif couleurTour == "vert":
            self.labelInfoTours.config(fg = "white", text =
                                    "Tour " + couleurTour + ": Niveau 1" + 
                                    "\n Dommage: "+ str(Tours.TourVert.degatBase) +
                                    "\n Portee: "+ str(Tours.TourVert.portee) +
                                    "\n Delai de tir: "+ str(Tours.TourVert.vitesseTir) +
                                    "\n Dommage Poison : "+ str(Tours.TourVert.degatPoison) +
                                    "\n Duree Poison :" + str(Tours.TourVert.dureePoison) +
                                    "\n\n Une tour qui inflige in poison lorsqu'elle touche le creep" +
                                    "\n\n\n Cliquez sur le terrain ou vous voulez placer cette tour")
            
        elif couleurTour == "magenta":
            self.labelInfoTours.config(fg = "white", text =
                                    "Tour " + couleurTour + ": Niveau 1" + 
                                    "\n Dommage: "+ str(Tours.TourMagenta.degatBase) +
                                    "\n Portee: "+ str(Tours.TourMagenta.portee) +
                                    "\n Delai de tir: "+ str(Tours.TourMagenta.vitesseTir) +
                                    "\n\n Une tour qui inflige du degat en zone" +
                                    "\n\n\n Cliquez sur le terrain ou vous voulez placer cette tour")
        elif couleurTour == "bleu":
            self.labelInfoTours.config(fg = "white", text = 
                                        "Tour " + couleurTour + ": Niveau 1" + 
                                    "\n Prix: "+ str(Tours.TourBleu.valeurAchat) +
                                    "\n Dommage: "+ str(Tours.TourBleu.degatBase) +
                                    "\n Portee: "+ str(Tours.TourBleu.portee) +
                                    "\n Delai de tir: "+ str(Tours.TourBleu.vitesseTir) +
                                    "\n\n Une tour tres lente mais tres puissante" +
                                    "\n\n\n Cliquez sur le terrain ou vous voulez placer cette tour")
             
           
        self.couleurTourAcheter = couleurTour       
        
    def verifOverlapTour(self,clickx,clicky): #Pour verifier si une tour est deja a l'endroit ou le joueur veut acheter une tour
        if len(self.mod.tours) == 0:
            return True
        else:
            for i in self.mod.tours:    
                if ((clickx >= i.x-10 and clickx <= i.x+10) and (clicky >= i.y-10 and clicky <= i.y+10)):
                    return False
                else:
                    return True
    
    def verifOverlapSentier(self,clickx,clicky): #Pour verifier si le joueur veut acheter une tour sur le sentier
        longueurSentier = len(self.mod.sentier)
        compteurSentier = 0
        boolOverlap = False
        while(compteurSentier < longueurSentier - 1):
            sentierX1=self.mod.sentier[compteurSentier][0]
            sentierY1=self.mod.sentier[compteurSentier][1]
            sentierX2=self.mod.sentier[compteurSentier+1][0]
            sentierY2=self.mod.sentier[compteurSentier+1][1]
            if sentierX2 < sentierX1 or sentierY2 < sentierY1:
                if ((clickx >= sentierX2-10 and clickx <= sentierX1+10) and (clicky >= sentierY2-10 and clicky <= sentierY1+10)):
                    boolOverlap = False
                    return False
                else:
                    boolOverlap = True
            else:
                if ((clickx >= sentierX1-10 and clickx <= sentierX2+10) and (clicky >= sentierY1-10 and clicky <= sentierY2+10)):
                    boolOverlap = False
                    return False
                else:
                    boolOverlap = True
            compteurSentier+=1
        return boolOverlap
     
    def verifPosTour(self,clickx,clicky): #Utilise les methodes OverlapSentier et OverlapTour et affiche un message si faux
        if self.verifOverlapTour(clickx,clicky) == True and self.verifOverlapSentier(clickx, clicky) == True: 
            print (self.couleurTourAcheter + " aux positions (" + str(clickx) + "," + str(clicky)+ ")")
            self.acheterTour(clickx, clicky, self.couleurTourAcheter)
        elif self.verifOverlapTour(clickx,clicky) == False:
            self.labelInfoTours.config(fg="white", text = "Veuillez choisir une position valide, la position est deja occupee")
        elif self.verifOverlapSentier(clickx, clicky) == False:  
            self.labelInfoTours.config(fg="white", text = "Veuillez choisir une position valide, la tour ne peut pas etre \n sur le sentier")
    
    def manqueArgent(self):
         self.labelInfoTours.config(fg="white", text = "Il manque d'argent pour acheter cette action")

    def afficherStatsTourExistante(self,clickx,clicky): # Afficher les statistiques de la tour existante
        self.surface.delete("portee")
        for i in self.mod.tours: 
            if ((clickx >= i.x-10 and clickx <= i.x+10) and (clicky >= i.y-10 and clicky <= i.y+10)):
                self.surface.create_oval(i.x - i.portee, i.y - i.portee, i.x + i.portee, i.y + i.portee, fill=None, tags=("portee"))
                if i.couleur == "rouge" :
                    self.tourSelectionee = True 
                    self.tourx = i.x
                    self.toury = i.y
                    self.labelInfoTours.config(fg = "white", text = 
                                    "Tour " + i.couleur + ": Niveau " + str(i.niveauTour) + 
                                    "\n Valeur de la tour: "+ str(i.valeurTotale) +
                                    "\n Cout upgrade: " + str(i.valeurUpgrade) +
                                    "\n Dommage: "+ str(i.degatBase) +
                                    "\n Portee: "+ str(i.portee) +
                                    "\n Delai de tir: "+ str(i.vitesseTir) +
                                    "\n\n Une tour lente qui tire loin et plus forte" +
                                    "\n\n\n Cliquez sur Vendre Tour si vous voulez vendre la tour" +
                                    "\n pour la moitie de sa valeur totale" +
                                    "\n\n Cliquez sur Upgrader Tour pour ameliorer la tour" +
                                    "\n en payant le cout decrit")
                elif i.couleur == "orange" : 
                    self.tourSelectionee = True 
                    self.tourx = i.x
                    self.toury = i.y
                    self.labelInfoTours.config(fg = "white", text = 
                                    "Tour " + i.couleur + ": Niveau " + str(i.niveauTour) + 
                                    "\n Valeur de la tour: "+ str(i.valeurTotale) +
                                    "\n Cout upgrade: " + str(i.valeurUpgrade) +
                                    "\n Dommage: "+ str(i.degatBase) +
                                    "\n Portee: "+ str(i.portee) +
                                    "\n Delai de tir: "+ str(i.vitesseTir) +
                                    "\n\n Une tour rapide, qui tire moins loin et moins forte" +
                                    "\n\n\n Cliquez sur Vendre Tour si vous voulez vendre la tour" +
                                    "\n pour la moitie de sa valeur totale" +
                                    "\n\n Cliquez sur Upgrader Tour pour ameliorer la tour" +
                                    "\n en payant le cout decrit")
                elif i.couleur == "jaune" : 
                    self.tourSelectionee = True 
                    self.tourx = i.x
                    self.toury = i.y
                    self.labelInfoTours.config(fg = "white", text = 
                                    "Tour " + i.couleur + ": Niveau " + str(i.niveauTour) + 
                                    "\n Valeur de la tour: "+ str(i.valeurTotale) +
                                    "\n Cout upgrade: " + str(i.valeurUpgrade) +
                                    "\n Dommage: "+ str(i.degatBase) +
                                    "\n Portee: "+ str(i.portee) +
                                    "\n Delai de tir: "+ str(i.vitesseTir) +
                                    "\n\n Une tour faible qui rapporte plus d'argent si elle tue le creep"+
                                    "\n\n\n Cliquez sur Vendre Tour si vous voulez vendre la tour" +
                                    "\n pour la moitie de sa valeur totale" +
                                    "\n\n Cliquez sur Upgrader Tour pour ameliorer la tour" +
                                    "\n en payant le cout decrit")
                elif i.couleur == "mauve" : 
                    self.tourSelectionee = True 
                    self.tourx = i.x
                    self.toury = i.y
                    self.labelInfoTours.config(fg = "white", text = 
                                    "Tour " + i.couleur + ": Niveau " + str(i.niveauTour) + 
                                    "\n Valeur de la tour: "+ str(i.valeurTotale) +
                                    "\n Cout upgrade: " + str(i.valeurUpgrade) +
                                    "\n Portee: "+ str(i.portee) +
                                    "\n Facteur Rapidite: "+ str(i.facteurTir) +
                                    "\n\n Une tour qui ne tire pas, mais qui augmente la rapidite"+
                                    "\n des autre tour dans sa portee."+
                                    "\n\n\n Cliquez sur Vendre Tour si vous voulez vendre la tour" +
                                    "\n pour la moitie de sa valeur totale" + 
                                    "\n\n Cliquez sur Upgrader Tour pour ameliorer la tour" +
                                    "\n en payant le cout decrit")
                elif i.couleur == "cyan":
                    self.tourSelectionee = True 
                    self.tourx = i.x
                    self.toury = i.y
                    self.labelInfoTours.config(fg = "white", text = 
                                    "Tour " + i.couleur + ": Niveau " + str(i.niveauTour) + 
                                    "\n Valeur de la tour: "+ str(i.valeurTotale) +
                                    "\n Cout upgrade: " + str(i.valeurUpgrade) +
                                    "\n Portee: "+ str(i.portee) +
                                    "\n\n Une tour qui ne tire pas, mais qui reduit la vitesse des creeps" +
                                    "\n des creeps dans sa portee" +
                                    "\n\n\n Cliquez sur le terrain ou vous voulez placer cette tour" +
                                    "\n\n Cliquez sur Upgrader Tour pour ameliorer la tour" +
                                    "\n en payant le cout decrit") 
                elif i.couleur == "blanc":
                    self.tourSelectionee = True 
                    self.tourx = i.x
                    self.toury = i.y
                    self.labelInfoTours.config(fg = "white", text =
                                    "Tour " + i.couleur + ": Niveau " + str(i.niveauTour) + 
                                    "\n Valeur de la tour: "+ str(i.valeurTotale) +
                                    "\n Cout upgrade: " + str(i.valeurUpgrade) +
                                    "\n Dommage: "+ str(i.degatBase) +
                                    "\n Portee: "+ str(i.portee) +
                                    "\n Delai de tir: "+ str(i.vitesseTir) +
                                    "\n Pourcentage Triple Dommage : "+ str(i.pourcentageCrit) + " %" +
                                    "\n\n Une tour relativement faible mais ayant une chance " +
                                    "\n de tirer un projectile pour triple dommage" +
                                    "\n\n\n Cliquez sur le terrain ou vous voulez placer cette tour" +
                                    "\n\n Cliquez sur Upgrader Tour pour ameliorer la tour" +
                                    "\n en payant le cout decrit") 
                elif i.couleur == "vert":
                    self.tourSelectionee = True 
                    self.tourx = i.x
                    self.toury = i.y
                    self.labelInfoTours.config(fg = "white", text =
                                    "Tour " + i.couleur + ": Niveau " + str(i.niveauTour) + 
                                    "\n Valeur de la tour: "+ str(i.valeurTotale) +
                                    "\n Cout upgrade: " + str(i.valeurUpgrade) +
                                    "\n Dommage: "+ str(i.degatBase) +
                                    "\n Portee: "+ str(i.portee) +
                                    "\n Delai de tir: "+ str(i.vitesseTir) +
                                    "\n Dommage Poison : "+ str(i.degatPoison) +
                                    "\n Duree Poison :" + str(i.dureePoison) +
                                    "\n\n Une tour qui inflige in poison lorsqu'elle touche le creep" +
                                    "\n\n\n Cliquez sur le terrain ou vous voulez placer cette tour" +
                                    "\n\n Cliquez sur Upgrader Tour pour ameliorer la tour" +
                                    "\n en payant le cout decrit") 
                elif i.couleur == "magenta":
                    self.tourSelectionee = True 
                    self.tourx = i.x
                    self.toury = i.y
                    self.labelInfoTours.config(fg = "white", text =
                                    "Tour " + i.couleur + ": Niveau " + str(i.niveauTour) + 
                                    "\n Valeur de la tour: "+ str(i.valeurTotale) +
                                    "\n Cout upgrade: " + str(i.valeurUpgrade) +
                                    "\n Dommage: "+ str(i.degatBase) +
                                    "\n Portee: "+ str(i.portee) +
                                    "\n Delai de tir: "+ str(i.vitesseTir) +
                                    "\n\n Une tour qui inflige du degat en zone" +
                                    "\n\n\n Cliquez sur le terrain ou vous voulez placer cette tour" +
                                    "\n\n Cliquez sur Upgrader Tour pour ameliorer la tour" +
                                    "\n en payant le cout decrit") 
                elif i.couleur == "bleu" :
                    self.tourSelectionee = True 
                    self.tourx = i.x
                    self.toury = i.y
                    self.labelInfoTours.config(fg = "white", text = 
                                    "Tour " + i.couleur + ": Niveau " + str(i.niveauTour) + 
                                    "\n Valeur de la tour: "+ str(i.valeurTotale) +
                                    "\n Cout upgrade: " + str(i.valeurUpgrade) +
                                    "\n Dommage: "+ str(i.degatBase) +
                                    "\n Portee: "+ str(i.portee) +
                                    "\n Delai de tir: "+ str(i.vitesseTir) +
                                    "\n\n Une tour tres lente mais puissante" +
                                    "\n\n\n Cliquez sur Vendre Tour si vous voulez vendre la tour" +
                                    "\n pour la moitie de sa valeur totale" +
                                    "\n\n Cliquez sur Upgrader Tour pour ameliorer la tour" +
                                    "\n en payant le cout decrit")
                
                
    def canvasClicked(self, event):
        if self.couleurTourAcheter == None:
            self.afficherStatsTourExistante(event.x,event.y)
            if self.tourSelectionee == False:
                self.labelInfoTours.config(fg="white", text = "Veuillez choisir quelle tour acheter")
        else:
           self.verifPosTour(event.x,event.y)
    
        self.couleurTourAcheter = None
        
    def menuFinDeNiveau(self):
        print("fin niveau")
        self.cadreJeu.pack_forget()
        self.surface.pack_forget()
        self.cadreBoutons.pack_forget()
        self.FrameInfoTours.pack_forget()
        self.labelInfoTours.pack_forget()
        self.cadreInfoPartie.pack_forget()
        
        self.cadreMenuFin=Frame(self.root,width=500, height=300)
        self.cadreMenuFin.pack(fill="none", expand=True) #parametres pour pack le frame au milieu
        
        self.btnRejouer=Button(self.cadreMenuFin,padx=140,pady=10,text="Rejouer",font=("Helvetica", 30),bg="grey",command=self.rejouer)
        self.btnMenuPrincipal=Button(self.cadreMenuFin,padx=160,pady=10,text="Menu",font=("Helvetica", 30),bg="grey",command=self.retourMenu)
        self.textPerdu= Label(self.cadreMenuFin,pady=45,text="Vous avez perdu :(",font=("Helvetica", 40),fg="white",bg="black")
        self.textPerdu.pack(fill=BOTH, expand=1)
        self.btnRejouer.pack(fill=BOTH, expand=1)
        self.btnMenuPrincipal.pack(fill=BOTH, expand=1)
        
    def pauseJeu(self):
        print("pause")
        if self.pause==True:
            self.pause=False
        else:
            self.pause=True
        self.parent.jouerCoup()
    
    def retourMenu(self):
        
        self.cadreMenuFin.pack_forget()
        self.menuPrincipal()
        
    def rejouer(self):
        
        self.cadreMenuFin.pack_forget()
        self.lancerPartie()
   
    def initVue(self):
        self.mod = None
        self.couleurTourAcheter = None
        self.tourSelectionee = False
        self.compteurBombe=0
        self.couleurProjectile=None
        self.timerBomb = 0
        self.x=0 # pour la bombe
        self.y=0# pour la bombe
        self.incrementationTimerBomb = 0
        self.tourx = 0
        self.toury = 0
        self.pause=False
        self.quitte=False

        self.effetCyan = 5
        self.effetMagenta = 1
        self.menuPrincipal()
    
    def quitterJeu(self):
        self.cadreJeu.pack_forget()
        self.surface.pack_forget()
        self.cadreBoutons.pack_forget()
        self.FrameInfoTours.pack_forget()
        self.labelInfoTours.pack_forget()
        self.cadreInfoPartie.pack_forget()
        self.quitte=True
        self.initVue()
        #self.menuPrincipal()
        
        
        
    