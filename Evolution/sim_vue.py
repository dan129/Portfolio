    # -*- coding: utf-8 -*-
from tkinter import *
import winsound
import animaux
import vegetaux
import habitation

class Vue():
    def __init__(self, parent, modele):
        self.parent = parent
        self.modele = modele
        self.root = Tk()

        # Text
        self.copyrightsText = "Développé par: Hiba Aneq, Dan Munteau, Mohamed Ilias, Ka-son Chau, Pierre-Marc Daméus et Maxime Denis\nDans le cadre du cour de B52 Développement en environnement de base de données au CVM"
        self.instructionsText = [
            "1. Pour inspected un animal ou une plante, vous pouvez cliquer dessus. La fenêtre de l'inspecteur s'ouvrira alors.",
            "2. Lorsque vous utilisez les outils pour ajouter ou supprimer des éléments, cliquez à gauche sur la case pour effectuer l'opération. Si vous désirez quitter le mode édition, faites ESCAPE.",
            "3. Si vous désirez passer de pleine résolution au mode normal ou vice versa, faites ALT + END."
            ]
        self.optionsText = [
            "Résolution",
            "Plein Écran\n(Alt + End)",
            "Musique"
            ]
        self.optionsGenText = [
            "Population Végétale",
            "Population Animale",
            "Niveau de l'eau",
            "Élévation du terrain",
            "Noyau"
            ]

        # Titre
        self.titreSim = "Simulation"
        self.root.title(self.titreSim)

        # Polices et couleurs
        self.policeMenu = "Agency FB"
        self.policeCopyrights = "Arial"
        self.couleurBG = "#F0F0F0"
        self.policeInfo= "Halvetica"

        # Variables d'affichage du monde
        self.echelle = 0.75                                                     # L'échelle à la quel la simulation est jouée
        self.echelleCarte = 0.035                                               # L'échelle de la carte
        self.mondeDirection = 'n'                                               # 'n' = nord (défaut), 'e' = est, 's' = sud et 'o' = ouest
        self.elevation = 300                                                    # L'élévation du terrain
        self.positionXCamera = 0
        self.positionYCamera = 0
        self.positionXCameraTmp = None
        self.positionYCameraTmp = None
        self.mondeAffiche = False
        self.ajoutElement = False
        self.supprimerElement = False
        self.afficherEco=False
        self.element = None
        self.entiteSelectionnee = None

        # Résolution
        self.largeurFenetre = 1280
        self.hauteurFenetre = 720
        self.largeurMin = 1280
        self.hauteurMin = 720
        self.pleinEcran = False
        self.ecranRedimensionnable = False

        # Musique
        self.musique = False
        self.appliquerMusique()

        # Chargements
        self.chargementImages()
        self.chargementGUI()

        # Application de la résolution
        self.appliquerResolution()

        # Créer les écouteurs
        self.ecouteurs()

        # Mode debuggage
        self.debuggage = True
        if self.debuggage:
            self.modeDebuggage()

        # Début de l'affichage
        self.afficherMenuPrincipal()

    def modeDebuggage(self):                                                    # Affiche le débuggage dans la console
        self.debugCoordonnees = False
        self.debugEnvironnement = False
        self.debugAnimal = False

        # Coordonnées du curseur sur le canvas
        def coordonnees(event):
            print('Coordonnées: {}, {}'.format(event.x, event.y))

        if self.debugCoordonnees:
            self.canvasMonde.bind('<Motion>', coordonnees)

    def trouverResolution(self):
            if self.pleinEcran:
                largeur = self.root.winfo_width()
                hauteur = self.root.winfo_height()
                self.varPleinEcran.set(self.choixPleinEcran[1])
            else:
                largeur = self.largeurFenetre
                hauteur = self.hauteurFenetre
                self.varPleinEcran.set(self.choixPleinEcran[0])
            self.root.geometry("{}x{}+0+0".format(largeur, hauteur))
            self.root.attributes("-fullscreen", self.pleinEcran)
            self.root.update_idletasks()
            self.canvasMonde.configure(width = self.root.winfo_width(),
                                       height = self.root.winfo_height())

            if self.modele.pause == False:
                self.nettoyerEcran()
                self.afficheMonde()

    def appliquerResolution(self):                                              # Détermine la résolution de la fenêtre
        if (not self.ecranRedimensionnable):
            self.root.resizable(False, False)                                   # Non-redimensionnable sur les x et les y

        self.root.minsize(self.largeurMin, self.hauteurMin)                     # Dimensions minimales de la fenêtre

        def trouverResolution():
            if self.pleinEcran:
                largeur = self.root.winfo_width()
                hauteur = self.root.winfo_height()
                self.varPleinEcran.set(self.choixPleinEcran[1])
            else:
                largeur = self.largeurFenetre
                hauteur = self.hauteurFenetre
                self.varPleinEcran.set(self.choixPleinEcran[0])
            self.root.geometry("{}x{}+0+0".format(largeur, hauteur))
            self.root.attributes("-fullscreen", self.pleinEcran)
            self.root.update_idletasks()

            self.canvasMonde.pack_forget()
            self.canvasMonde.configure(width = self.root.winfo_width(),
                                       height = self.root.winfo_height())

            if self.modele.pause == False:
                self.nettoyerEcran()
                self.afficheMonde()

        self.trouverResolution()

    def ecouteurs(self):
        # Alt + End pour changer à pleine écran ou no
        def togglePleinEcran(event):
            self.pleinEcran = not self.pleinEcran
            self.trouverResolution()

        self.root.bind("<Alt-End>", togglePleinEcran)

        # Bouger L'écran
        def coordInit(event):
            self.coordXInit = event.x
            self.coordYInit = event.y
            self.positionXCameraTmp = self.positionXCamera
            self.positionYCameraTmp = self.positionYCamera

        def bougerTerrain(event):
            self.positionXCamera = self.positionXCameraTmp - self.coordXInit + event.x
            self.positionYCamera = self.positionYCameraTmp - self.coordYInit + event.y

            if self.modele.pause:
                self.afficherEnvironnement(echelle = self.echelle)

        self.canvasMonde.bind("<ButtonPress-3>", coordInit)
        self.canvasMonde.bind("<B3-Motion>", bougerTerrain)
        self.canvasMonde.bind("<ButtonRelease-3>", bougerTerrain)

        # Modifie le temps
        def changerTemps(event):
            self.parent.changerTemps(int(self.varMultiplicateurTemps.get()))

        self.entTemps.bind("<Return>", changerTemps)

        # Cliquer sur un objet dans le canvas du monde
        def cliqueCanvasMonde(event):
            if not self.ajoutElement and not self.supprimerElement:
                self.afficherEco=True

            if self.mondeAffiche and (self.ajoutElement or self.supprimerElement or self.afficherEco) :
                tag = self.canvasMonde.gettags(CURRENT)

                if self.ajoutElement:
                    self.afficherEco = False
                    self.parent.ajouterElement(self.element, int(tag[0]), int(tag[1]))

                elif self.supprimerElement:
                    self.afficherEco = False
                    self.parent.supprimerElement(tag[2], int(tag[0]), int(tag[1]))

                self.frameInspecteur.place_forget()

                if self.afficherEco:
                    if len(tag) >= 3:
                        if "current" not in tag[2]:
                            animal = self.modele.environnement[int(tag[1])][int(tag[0])][1]
                            plante = self.modele.environnement[int(tag[1])][int(tag[0])][2]
    
                            if tag[2] in self.modele.dictionnaireVegetaux:
                                self.entiteSelectionnee = plante
                                self.modifierInspecteur()
                                self.afficherInspecteur(0)
                            elif tag[2] in self.modele.dictionnaireAnimaux:
                                self.entiteSelectionnee = animal
                                self.modifierInspecteur()
                                self.afficherInspecteur(1)

        self.canvasMonde.bind("<Button-1>", cliqueCanvasMonde)
        
        # Bouger sur la carte
        def bougerCarte(event):
            ratio = self.echelle / self.echelleCarte
            self.positionXCamera = 100 * ratio - event.x * ratio - 100 * self.echelle
            self.positionYCamera = 100 * ratio - event.y * ratio + self.elevation * self.echelle

            if self.modele.pause:
                self.afficherEnvironnement(echelle = self.echelle)

        self.canvasCarte.bind("<ButtonPress-1>", bougerCarte)
        self.canvasCarte.bind("<B1-Motion>", bougerCarte)
        self.canvasCarte.bind("<ButtonRelease-1>", bougerCarte)

        # Escape pour annuler les actions avec l'outil
        def annulerAction(event):
            if self.mondeAffiche:
                self.outilSimActif = False
                self.ajoutElement = False
                self.supprimerElement = False
                self.afficherEco=False

        self.root.bind("<Escape>", annulerAction)

    def chargementImages(self):

        self.imagesBG = [
            PhotoImage(file = "images//bgMenuPrincipal.png"),                   # 0. Background du menu principal
            PhotoImage(file = "images//bgInstructions.png"),                    # 1. Background des instructions
            PhotoImage(file = "images//bgMenuOptions.png"),                     # 2. Background du menu d'options pour la génération du monde
            PhotoImage(file = "images//bgOptions.png"),                         # 3. Background du menu d'options
            PhotoImage(file = "images//bgOutilsSim.png")                        # 4. Background pour les outils de la simulatioin
            ]

        self.imagesAnimaux = [
            PhotoImage(file = "images//Animaux//loup.png"),                     # 0. Loup
            PhotoImage(file = "images//Animaux//lapin.png"),                     # 1. Lapin
            PhotoImage(file = "images//Animaux//ours.png"),                     # 2. Ours
            PhotoImage(file = "images//Animaux//lievre1.png"),                     # 3. Lievre
            PhotoImage(file = "images//Animaux//bison.png")                     # 4. bison
            ]
        self.imageHabitation = [
            PhotoImage(file ="images//Animaux//terrier.png")
            ]
        self.imagesPlantes = [
            PhotoImage(file ="images//Plantes//ble.png"),                       # 0. ble
            PhotoImage(file ="images//Plantes//arbre.png"),                     # 1. Érable
            PhotoImage(file ="images//Plantes//laitue.png"),                    # 2 laitue
            PhotoImage(file ="images//Plantes//cerisierFleuri.png"),            #3 cerisier
            PhotoImage(file ="images//Plantes//peuplier.png"),                  #4 peuplier
            PhotoImage(file ="images//Plantes//cerisier-pre-fleuri.png"),       #5 cerisier
            PhotoImage(file ="images//Plantes//sapin.png")                      #6 sapin
            ]
        self.imagesPlantesHiver = [
            PhotoImage(file ="images//Plantes//peuplier_nu.png"),                # 0. peuplier
            PhotoImage(file ="images//Plantes//erable_nu.png"),                  # 1. Érable
            PhotoImage(file ="images//Plantes//sapin_neige.png")                 # 2 sapin
        ]

    def chargementGUI(self):                                                    # Construit et charge tout le GUI
        self.chargementMenuPrincipal()
        self.chargementInstructions()
        self.chargementOptions()
        self.chargementMenuOptionsGen()
        self.chargementMonde()
        self.chargementInspecteur()
        self.chargementOutilsSim()

    def nettoyerEcran(self):                                                    # Nettoye l'écran de toute interface
        for enfant in self.frameMenuPrincipalCentre.winfo_children():
            enfant.pack_forget()

        self.frameMenuPrincipal.pack_forget()
        self.frameInstructions.pack_forget()
        self.frameMenuOptions.pack_forget()
        self.frameMenuOptionsGen.pack_forget()

        for enfant in self.frameControles.winfo_children():
            enfant.pack_forget()

        self.frameInspecteur.place_forget()
        self.frameMonde.pack_forget()
        self.frameOutilsSim.pack_forget()

    def hexToRGB(self, couleurHex):                                             # Converti une couleur en hexadécimal à RGB
        rouge = int(couleurHex[1:3], 16)
        vert = int(couleurHex[3:5], 16)
        bleu = int(couleurHex[5:7], 16)

        return rouge, vert, bleu

    def rgbToHex(self, couleurRgb):                                             # Converti une couleur en RGB à hexadécimal
        hexRouge = "{:02x}".format(couleurRgb[0])
        hexVert = "{:02x}".format(couleurRgb[1])
        hexBleu = "{:02x}".format(couleurRgb[2])

        return "#" + hexRouge + hexVert + hexBleu

    def clamp(self, valeur, valeurMin, valeurMax):                              # Donne une valeur minimale et maximale à ne pas dépasser
        return max(min(valeur, valeurMax), valeurMin)

    def luminositeCouleurRGB(self, couleurRGB, modificateur):                     # Modifie la couleur en incrémentant ou en décrémentant les valeurs
        rougeModifie = self.clamp(couleurRGB[0] + modificateur, 0, 255)
        vertModifie = self.clamp(couleurRGB[1] + modificateur, 0, 255)
        bleuModifie = self.clamp(couleurRGB[2] + modificateur, 0, 255)

        return rougeModifie, vertModifie, bleuModifie

    def luminositeCouleurHex(self, couleurHex, modificateur):                     # Modofie la couleur hexadécimale selon l'incrémentation ou la décrémentation des valeurs
        couleurRBG = self.hexToRGB(couleurHex)
        couleurModifiee = self.luminositeCouleurRGB(couleurRBG, modificateur)

        return self.rgbToHex(couleurModifiee)

    def chargementMenuPrincipal(self):                                          # Construit et charge le menu principal
        # Frame qui contient la page
        self.frameMenuPrincipal = Frame(self.root,
                                        bg = self.couleurBG,
                                        highlightthickness = 0)
        # Affiche le background
        self.labBGMenuPrincipal = Label(self.frameMenuPrincipal,
                                        bg = self.couleurBG,
                                        image = self.imagesBG[0])
        # Frame qui contient le menu
        self.frameMenuPrincipalCentre = Frame(self.frameMenuPrincipal,
                                              bg = self.couleurBG,
                                              highlightthickness = 0)
        # Affiche le titre de la simulationi
        self.labTitreSim = Label(self.frameMenuPrincipalCentre,
                                 font = (self.policeMenu, 40),
                                 bg = self.couleurBG,
                                 fg = "#222222",
                                 text = self.titreSim)

        # Afficher les boutons du menu
        self.btnMenuPrincipal = []

        btnMenuPrincipalTxtOuCmd = [
            ("Reprendre la simulation", self.parent.reprendreSim),
            ("Nouvelle simulation", self.afficherMenuOptionsGen),
            ("Instructions", self.afficherInstructions),
            ("Options", self.afficherOptions),
            ("Quitter", self.parent.quitter)
            ]

        for txtOuCmd in btnMenuPrincipalTxtOuCmd:
            btn = Button(self.frameMenuPrincipalCentre,
                         font = (self.policeMenu, 20),
                         bg = "#292929",
                         fg = "#FFFFFF",
                         activebackground = "#FFFFFF",
                         activeforeground = "#292929",
                         text = txtOuCmd[0],
                         command = txtOuCmd[1])

            self.btnMenuPrincipal.append(btn)
        # Copyrights
        self.labCopyrightsMenuPrincipal = Label(self.frameMenuPrincipal,
                                                font = (self.policeCopyrights, 7),
                                                bg = self.couleurBG,
                                                fg = "#222222",
                                                text = self.copyrightsText)


    def chargementInstructions(self):                                          # Construit et charge les instructions
        # Frame qui contient la page
        self.frameInstructions = Frame(self.root,
                                       bg = self.couleurBG,
                                       highlightthickness = 0)
        # Affiche le background
        self.labBGInstructions = Label(self.frameInstructions,
                                       bg = self.couleurBG,
                                       image = self.imagesBG[1])
        # Frame qui contient les instructions
        self.frameInstructionsCentre = Frame(self.frameInstructions,
                                             bg = self.couleurBG,
                                             highlightthickness = 0)
        # Affiche le titre
        self.labTitreInstructions = Label(self.frameInstructionsCentre,
                                          font = (self.policeMenu, 40),
                                          bg = self.couleurBG,
                                          fg = "#222222",
                                          text = "Instructions")
        # Labal pour les instructions
        self.mesInstructions = Message(self.frameInstructionsCentre,
                                       font = (self.policeMenu, 20),
                                       bg = self.couleurBG,
                                       fg = "#222222",
                                       anchor='w',
                                       width = 700)

        instText = ""

        for inst in self.instructionsText[:-1]:
            instText = instText + inst + "\n\n"

        instText = instText + self.instructionsText[-1]
        self.mesInstructions["text"] = instText
        # Bouton pour retourner au menu principal
        self.btnInstructionsRetourMenuPrincipal = Button(self.frameInstructionsCentre,
                                                         font = (self.policeMenu, 20),
                                                         bg = "#292929",
                                                         fg = "#FFFFFF",
                                                         activebackground = "#FFFFFF",
                                                         activeforeground = "#292929",
                                                         text = "Retour au menu",
                                                         command = self.afficherMenuPrincipal)
        # Copyrights
        self.labCopyrightsInstructions = Label(self.frameInstructions,
                                               font = (self.policeCopyrights, 7),
                                               bg = self.couleurBG,
                                               fg = "#222222",
                                               text = self.copyrightsText)

    def chargementOptions(self):
        # Frame qui contient la page
        self.frameMenuOptions = Frame(self.root,
                                         bg = self.couleurBG,
                                         highlightthickness = 0)
        # Affiche le background
        self.labBGMenuOptions = Label(self.frameMenuOptions,
                                         bg = self.couleurBG,
                                         image = self.imagesBG[3])
        # Frame qui contient les options de génération
        self.frameMenuOptionsCentre = Frame(self.frameMenuOptions,
                                               bg = self.couleurBG,
                                               highlightthickness = 0)
        # Affiche le titre
        self.labTitreMenuOptions = Label(self.frameMenuOptionsCentre,
                                            font = (self.policeMenu, 40),
                                            bg = self.couleurBG,
                                            fg = "#222222",
                                            text = "Options")
        # Frame pour les options
        self.frameOptions = Frame(self.frameMenuOptionsCentre,
                                  bg = self.couleurBG,
                                  highlightthickness = 0)
        # Labal pour les options
        self.labOptions = []

        for option in self.optionsText:
            self.labOptions.append(Label(self.frameOptions,
                                         font = (self.policeMenu, 20),
                                         bg = self.couleurBG,
                                         fg = "#222222",
                                         text = option))
        # Largeur des option menus
        largeur = 15
        # Option menu de la résolution
        self.varResolution = StringVar(self.frameOptions)
        choix = []
        ecranX = self.root.winfo_screenwidth()
        ecranY = self.root.winfo_screenheight()
        # Résolution minimale de base
        choix.append("1280 x 720 (16:9)")
        self.varResolution.set("1280 x 720 (16:9)")

        choixPossibles = [
            "1280 x 768 (5:3)",
            "1280 x 800 (16:10)",
            "1280 x 854 (3:2)",
            "1280 x 960 (4:3)",
            "1280 x 1024 (5:4)",
            "1366 x 768 (16:9)",
            "1400 x 1050 (4:3)",
            "1440 x 900 (16:10)",
            "1440 x 960 (3:2)",
            "1440 x 1080 (4:3)",
            "1600 x 900 (16:9)",
            "1600 x 1200 (4:3)",
            "1680 x 1050 (16:10)",
            "1920 x 1080 (16:9)",
            "1920 x 1200 (16:10)",
            "2048 x 1080 (17:9)",
            "2048 x 1536 (4:3)",
            "2560 x 1080 (21:9)",
            "2560 x 1440 (16:9)",
            "2560 x 1600 (16:10)",
            "2560 x 2048 (5:4)",
            "3440 x 1440 (21:0)",
            "3840 x 2160 (16:9)",
            "4096 x 2160 (17:9)"
            ]

        for resolution in choixPossibles:
            valeurs = resolution.split(" ")
            if int(valeurs[0]) <= ecranX and int(valeurs[2]) <= ecranY:
                choix.append(resolution)

            if int(valeurs[0]) == self.largeurFenetre and int(valeurs[2]) == self.hauteurFenetre:
                self.varResolution.set(resolution)

        self.optMenuResolution = OptionMenu(self.frameOptions,
                                            self.varResolution,
                                            *choix)
        self.optMenuResolution.configure(font = (self.policeMenu, 20),
                                         bg = "#292929",
                                         fg = "#FFFFFF",
                                         activebackground = "#FFFFFF",
                                         activeforeground = "#292929",
                                         width = largeur)
        # Option menu pour activer ou désactiver le mode plein écran
        self.varPleinEcran = StringVar(self.frameOptions)
        self.choixPleinEcran = [
            "Désactivé",
            "Activé"
            ]

        if self.pleinEcran:
            self.varPleinEcran.set(self.choixPleinEcran[1])
        else:
            self.varPleinEcran.set(self.choixPleinEcran[0])

        self.optMenuPleinEcran = OptionMenu(self.frameOptions,
                                             self.varPleinEcran,
                                             *self.choixPleinEcran)
        self.optMenuPleinEcran.configure(font = (self.policeMenu, 20),
                                          bg = "#292929",
                                          fg = "#FFFFFF",
                                          activebackground = "#FFFFFF",
                                          activeforeground = "#292929",
                                          width = largeur)
        # Option menu pour activer ou désactiver la musique
        self.varMusique = StringVar(self.frameOptions)
        choix = [
            "Désactivé",
            "Activé"
            ]

        if self.musique:
            self.varMusique.set(choix[1])
        else:
            self.varMusique.set(choix[0])

        self.optMenuMusique = OptionMenu(self.frameOptions,
                                             self.varMusique,
                                             *choix)
        self.optMenuMusique.configure(font = (self.policeMenu, 20),
                                          bg = "#292929",
                                          fg = "#FFFFFF",
                                          activebackground = "#FFFFFF",
                                          activeforeground = "#292929",
                                          width = largeur)
        # Bouton pour retourner au menu principal
        def appliquerOptions():
            resolution = self.varResolution.get().split(" ")
            self.largeurFenetre = int(resolution[0])
            self.hauteurFenetre = int(resolution[2])

            if self.varPleinEcran.get() == "Activé":
                self.pleinEcran = True
            else:
                self.pleinEcran = False

            self.appliquerResolution()

            if self.varMusique.get() == "Activé":
                self.musique = True
            else:
                self.musique = False

            self.appliquerMusique()
            self.afficherMenuPrincipal()

        self.btnOptionsRetourMenuPrincipal = Button(self.frameMenuOptionsCentre,
                                                       font = (self.policeMenu, 20),
                                                       bg = "#292929",
                                                       fg = "#FFFFFF",
                                                       activebackground = "#FFFFFF",
                                                       activeforeground = "#292929",
                                                       text = "Retour au menu",
                                                       command = appliquerOptions)
        # Copyrights
        self.labCopyrightsMenuOptions = Label(self.frameMenuOptions,
                                                 font = (self.policeCopyrights, 7),
                                                 bg = self.couleurBG,
                                                 fg = "#222222",
                                                 text = self.copyrightsText)

    def chargementMenuOptionsGen(self):                                          # Construit et charge le menu d'options de la génération du monde
        # Frame qui contient la page
        self.frameMenuOptionsGen = Frame(self.root,
                                         bg = self.couleurBG,
                                         highlightthickness = 0)
        # Affiche le background
        self.labBGMenuOptionsGen = Label(self.frameMenuOptionsGen,
                                         bg = self.couleurBG,
                                         image = self.imagesBG[2])
        # Frame qui contient les options de génération
        self.frameMenuOptionsGenCentre = Frame(self.frameMenuOptionsGen,
                                               bg = self.couleurBG,
                                               highlightthickness = 0)
        # Affiche le titre
        self.labTitreMenuOptionsGen = Label(self.frameMenuOptionsGenCentre,
                                            font = (self.policeMenu, 40),
                                            bg = self.couleurBG,
                                            fg = "#222222",
                                            text = "Nouvelle Simulation")
        # Frame pour les options
        self.frameOptionsGen = Frame(self.frameMenuOptionsGenCentre,
                                  bg = self.couleurBG,
                                  highlightthickness = 0)
        # Labal pour les options
        self.labOptionsGen = []

        for option in self.optionsGenText:
            self.labOptionsGen.append(Label(self.frameOptionsGen,
                                      font = (self.policeMenu, 20),
                                      bg = self.couleurBG,
                                      fg = "#222222",
                                      text = option))
        # Largeur des option menus
        largeur = 9
        # Option menu de la population végétale
        self.varPopVegetale = StringVar(self.frameOptionsGen)
        self.choixVarPopVegetale = ["Rare", "Basse", "Normale", "Élevée", "Abondante"]
        self.varPopVegetale.set(self.choixVarPopVegetale[2])
        self.optMenuPopVegetale = OptionMenu(self.frameOptionsGen,
                                             self.varPopVegetale,
                                             *self.choixVarPopVegetale)
        self.optMenuPopVegetale.configure(font = (self.policeMenu, 20),
                                          bg = "#292929",
                                          fg = "#FFFFFF",
                                          activebackground = "#FFFFFF",
                                          activeforeground = "#292929",
                                          width = largeur)
        # Option menu de la population animale
        self.varPopAnimale = StringVar(self.frameOptionsGen)
        self.choixVarPopAnimale = ["Rare", "Basse", "Normale", "Élevée", "Abondante"]
        self.varPopAnimale.set(self.choixVarPopAnimale[2])
        self.optMenuPopAnimale = OptionMenu(self.frameOptionsGen,
                                            self.varPopAnimale,
                                            *self.choixVarPopAnimale)
        self.optMenuPopAnimale.configure(font = (self.policeMenu, 20),
                                         bg = "#292929",
                                         fg = "#FFFFFF",
                                         activebackground = "#FFFFFF",
                                         activeforeground = "#292929",
                                         width = largeur)
        # Option menu du niveau de l'eau
        self.varNivEau = StringVar(self.frameOptionsGen)
        self.choixVarNivEau = ["Très Bas", "Bas", "Normal", "Élevé", "Très Élevé"]
        self.varNivEau.set(self.choixVarNivEau[2])
        self.optMenuNivEau = OptionMenu(self.frameOptionsGen,
                                        self.varNivEau,
                                        *self.choixVarNivEau)
        self.optMenuNivEau.configure(font = (self.policeMenu, 20),
                                     bg = "#292929",
                                     fg = "#FFFFFF",
                                     activebackground = "#FFFFFF",
                                     activeforeground = "#292929",
                                     width = largeur)
        # Option menu de l'élévation du terrain
        self.varElevationTerrain = StringVar(self.frameOptionsGen)
        self.choixVarElevationTerrain = ["Très Bas", "Bas", "Normal", "Élevé", "Très Élevé"]
        self.varElevationTerrain.set(self.choixVarElevationTerrain[2])
        self.optMenuElevationTerrain = OptionMenu(self.frameOptionsGen,
                                                  self.varElevationTerrain,
                                                  *self.choixVarElevationTerrain)
        self.optMenuElevationTerrain.configure(font = (self.policeMenu, 20),
                                               bg = "#292929",
                                               fg = "#FFFFFF",
                                               activebackground = "#FFFFFF",
                                               activeforeground = "#292929",
                                               width = largeur)
        # Entry pour le noyau
        def correct(entree):
            if (entree.isdigit() and int(entree) < (2 ** 32 - 1)) or entree is "":
                return True
            else:
                return False

        self.varNoyau = StringVar(self.frameOptionsGen,
                                  value = 0)

        reg = self.root.register(correct)

        self.entNoyau = Entry(self.frameOptionsGen,
                              font = (self.policeMenu, 20),
                              bg = "#292929",
                              fg = "#FFFFFF",
                              textvariable = self.varNoyau,
                              validate = "key",
                              validatecommand = (reg, "%P"),
                              width = 13)
        # Frame pour les boutons pour procéder ou retourner au menu
        self.frameProcederOuRetourner = Frame(self.frameMenuOptionsGenCentre,
                                              bg = self.couleurBG,
                                              highlightthickness = 0)
        # Bouton pour retourner au menu principal
        self.btnOptionsGenRetourMenuPrincipal = Button(self.frameProcederOuRetourner,
                                                       font = (self.policeMenu, 20),
                                                       bg = "#292929",
                                                       fg = "#FFFFFF",
                                                       activebackground = "#FFFFFF",
                                                       activeforeground = "#292929",
                                                       text = "Retour au menu",
                                                       command = self.afficherMenuPrincipal,
                                                       width = 25)
        # Bouton pour commencer la simulation
        def commencerSim():
            if self.varNoyau.get() == "":
                noyau = 0
            else:
                noyau = int(self.varNoyau.get())

            self.parent.demarrerSim(self.varPopAnimale.get(), self.varPopVegetale.get(), self.varNivEau.get(), self.varElevationTerrain.get(), noyau)

        self.btnDemarrerSim = Button(self.frameProcederOuRetourner,
                                     font = (self.policeMenu, 20),
                                     bg = "#292929",
                                     fg = "#FFFFFF",
                                     activebackground = "#FFFFFF",
                                     activeforeground = "#292929",
                                     text = "Démarrer la simulation",
                                     command = commencerSim,
                                     width = 25)
        # Copyrights
        self.labCopyrightsMenuOptionsGen = Label(self.frameMenuOptionsGen,
                                                 font = (self.policeCopyrights, 7),
                                                 bg = self.couleurBG,
                                                 fg = "#222222",
                                                 text = self.copyrightsText)

    def chargementMonde(self):                                                  # Construit et charge le monde de la simulation
        # Frame qui contient la page
        self.frameMonde = Frame(self.root,
                              bg = self.couleurBG,
                              highlightthickness = 0)
        # Frame qui contient les contrôles pour l'utilisateur
        self.frameControles = Frame(self.frameMonde,
                              bg = self.couleurBG,
                              highlightthickness = 0)

        # Bouton pour retourner au menu principal
        self.btnRetourMenu = Button(self.frameControles,
                                    font = (self.policeMenu, 17),
                                    bg = "#292929",
                                    fg = "#FFFFFF",
                                    activebackground = "#FFFFFF",
                                    activeforeground = "#292929",
                                    text = "Retour au menu",
                                    command = self.parent.retourMenu)
        # Bouton pour retourner au menu principal
        self.btnOutilsSim = Button(self.frameControles,
                                    font = (self.policeMenu, 17),
                                    bg = "#292929",
                                    fg = "#FFFFFF",
                                    activebackground = "#FFFFFF",
                                    activeforeground = "#292929",
                                    text = "Outils De Simulation",
                                    command = self.parent.outilsSim)
        # Canvas sur le quel la simulation va se dérouler
        self.canvasCarte = Canvas(self.frameControles,
                                  highlightthickness = 0,
                                  width = 200,
                                  height = 200,
                                  bg = self.couleurBG)
        # Labal pour l'affichage du temps
        self.labTemps = Label(self.frameControles,
                              font = (self.policeMenu, 16),
                              bg = self.couleurBG,
                              fg = "#222222")
        # Label gestionnaire de temps
        self.labMultiplicateurTemps = Label(self.frameControles,
                                            font = (self.policeMenu, 16),
                                            bg = self.couleurBG,
                                            fg = "#222222",
                                            text = "Gestionnaire de temps\n(Minute / Seconde)")
        # Entry temps
        def correct(entree):
            if (entree.isdigit() and int(entree) < (2 ** 32 - 1)) or entree is "":
                return True
            else:
                return False

        self.varMultiplicateurTemps = StringVar(self.frameMonde,
                                                value = self.modele.multiplicateurTemps)

        reg = self.root.register(correct)

        self.entTemps = Entry(self.frameControles,
                              font = (self.policeMenu, 15),
                              bg = "#292929",
                              fg = "#FFFFFF",
                              textvariable = self.varMultiplicateurTemps,
                              validate = "key",
                              validatecommand = (reg, "%P"))
        # Bouton pause
        self.btnPause = Button(self.frameControles,
                               font = (self.policeMenu, 15),
                               bg = "#292929",
                               fg = "#FFFFFF",
                               activebackground = "#FFFFFF",
                               activeforeground = "#292929",
                               text = "Pauser la simulation",
                               command = self.parent.pauserOuReprendre)
        # Label populations
        self.labPopulations = Label(self.frameControles,
                                    font = (self.policeMenu, 16),
                                    bg = self.couleurBG,
                                    fg = "#222222",
                                    text = "Populations")
        # Frame qui affiche les populations
        self.framePopulations = Frame(self.frameControles,
                                      bg = self.couleurBG,
                                      highlightthickness = 0)
        # Labels de la population d'animaux
        self.labPopAnimaux = []

        for animal in self.modele.dictionnaireAnimaux:
            self.labPopAnimaux.append([Label(self.framePopulations,
                                               font = (self.policeInfo, 10),
                                               bg = self.couleurBG,
                                               fg = "#222222",
                                               text = animal + ": ",
                                               anchor = "w",
                                               width = 12),
                                       animal])
        # Labels de la population de végétaux
        self.labPopVegetaux = []

        for plante in self.modele.dictionnaireVegetaux:
            self.labPopVegetaux.append([Label(self.framePopulations,
                                             font = (self.policeInfo, 10),
                                             bg = self.couleurBG,
                                             fg = "#222222",
                                             text = plante + ": ",
                                             anchor = "w",
                                             width = 12),
                                        plante])
        # Canvas du monde
        self.canvasMonde = Canvas(self.frameMonde,
                                  highlightthickness = 0,
                                  width = self.root.winfo_width(),
                                  height = self.root.winfo_height(),
                                  bg = self.couleurBG)

    def chargementInspecteur(self):
        self.frameInspecteur = Frame(self.frameMonde,
                                    bg = "#292929")

        self.labTitreInspecteur = Label(self.frameInspecteur,
                                        font = (self.policeInfo,10 ),
                                        bg = "#000000",
                                        fg = "#FFFFFF",
                                        text = "Inspecteur",
                                        width = 50)

        self.labInfoInspecteur = []

        for i in range(9):
            self.labInfoInspecteur.append(Label(self.frameInspecteur,
                                                font = (self.policeInfo, 10),
                                                text = ""))

    def chargementOutilsSim(self):
        # Frame qui contient la page
        self.frameOutilsSim = Frame(self.root,
                                    bg = self.couleurBG,
                                    highlightthickness = 0)
        # Affiche le background
        self.labBGOutilsSim = Label(self.frameOutilsSim,
                                    bg = self.couleurBG,
                                    image = self.imagesBG[4])
        # Frame qui contient le menu
        self.frameOutilsSimCentre = Frame(self.frameOutilsSim,
                                          bg = self.couleurBG,
                                          highlightthickness = 0)
        # Affiche le titre de la simulationi
        self.labTitreOutilsSim = Label(self.frameOutilsSimCentre,
                                       font = (self.policeMenu, 40),
                                       bg = self.couleurBG,
                                       fg = "#222222",
                                       text = "Outils de simulation")
        # Label pour ajouter des éléments à la simulation
        self.labOutilSimAjouter = Label(self.frameOutilsSimCentre,
                                        font = (self.policeMenu, 20),
                                        bg = self.couleurBG,
                                        fg = "#222222",
                                        text = "Ajouter des animaux ou des plantes")
        # Frame pour les options
        self.frameOutilSimSelection = Frame(self.frameOutilsSimCentre,
                                            bg = self.couleurBG,
                                            highlightthickness = 0)
        # Largeur des option menus
        largeurOptionMenu = 20
        largeurButton = 15
        # Outil pour ajouter des animaux
        self.varAjouterAnimal = StringVar(self.frameOutilSimSelection)
        self.choixVarAjouterAnimal = ["---Animal---", "Lapin", "Loup", "Ours","Lièvre"]
        self.varAjouterAnimal.set(self.choixVarAjouterAnimal[0])
        self.outilSimAjouterAnimal = OptionMenu(self.frameOutilSimSelection,
                                                self.varAjouterAnimal,
                                                *self.choixVarAjouterAnimal)
        self.outilSimAjouterAnimal.configure(font = (self.policeMenu, 20),
                                             bg = "#292929",
                                             fg = "#FFFFFF",
                                             activebackground = "#FFFFFF",
                                             activeforeground = "#292929",
                                             width = largeurOptionMenu)
        # Outil pour ajouter des végétaux
        self.varAjouterPlante = StringVar(self.frameOutilSimSelection)
        self.choixVarAjouterPlante = ["---Plante---", "Blé", "Cerisier", "Érable", "Laitue", "Peuplier", "Sapin"]
        self.varAjouterPlante.set(self.choixVarAjouterPlante[0])
        self.outilSimAjouterPlante = OptionMenu(self.frameOutilSimSelection,
                                                self.varAjouterPlante,
                                                *self.choixVarAjouterPlante)
        self.outilSimAjouterPlante.configure(font = (self.policeMenu, 20),
                                             bg = "#292929",
                                             fg = "#FFFFFF",
                                             activebackground = "#FFFFFF",
                                             activeforeground = "#292929",
                                             width = largeurOptionMenu)
        # Bouton pour ajouter un animal
        def ajouterAnimal():
            if self.varAjouterAnimal.get() != self.choixVarAjouterAnimal[0]:
                self.element = self.varAjouterAnimal.get()
                self.ajoutElement = True
                self.supprimerElement = False
                self.parent.reprendreSim()

        self.btnOutilsSimAjouterAnimal = Button(self.frameOutilSimSelection,
                                                font = (self.policeMenu, 17),
                                                bg = "#292929",
                                                fg = "#FFFFFF",
                                                activebackground = "#FFFFFF",
                                                activeforeground = "#292929",
                                                text = "Ajouter",
                                                command = ajouterAnimal,
                                                width = largeurButton)
        # Bouton pour ajouter une plante
        def ajouterPlante():
            if self.varAjouterPlante.get() != self.choixVarAjouterPlante[0]:
                self.element = self.varAjouterPlante.get()
                self.ajoutElement = True
                self.supprimerElement = False
                self.parent.reprendreSim()

        self.btnOutilsSimAjouterPlante = Button(self.frameOutilSimSelection,
                                                font = (self.policeMenu, 17),
                                                bg = "#292929",
                                                fg = "#FFFFFF",
                                                activebackground = "#FFFFFF",
                                                activeforeground = "#292929",
                                                text = "Ajouter",
                                                command = ajouterPlante,
                                                width = largeurButton)
        # Label pour ajouter des éléments à la simulation
        self.labOutilSimSupprimer = Label(self.frameOutilsSimCentre,
                                        font = (self.policeMenu, 20),
                                        bg = self.couleurBG,
                                        fg = "#222222",
                                        text = "Supprimer des animaux ou des plantes")
        # Bouton pour supprimer une plante
        def supprimer():
            self.ajoutElement = False
            self.supprimerElement = True
            self.parent.reprendreSim()

        self.btnOutilsSimSupprimer = Button(self.frameOutilsSimCentre,
                                            font = (self.policeMenu, 17),
                                            bg = "#292929",
                                            fg = "#FFFFFF",
                                            activebackground = "#FFFFFF",
                                            activeforeground = "#292929",
                                            text = "Supprimer",
                                            command = supprimer,
                                            width = largeurButton)
        # Bouton pour retourner à la simulation
        self.btnRetourSim = Button(self.frameOutilsSimCentre,
                                   font = (self.policeMenu, 20),
                                   bg = "#292929",
                                   fg = "#FFFFFF",
                                   activebackground = "#FFFFFF",
                                   activeforeground = "#292929",
                                   text = "Retour à la simulation",
                                   command = self.parent.reprendreSim)

    def afficherMenuPrincipal(self):                                            # Affiche le menu principal
        self.nettoyerEcran()

        self.mondeAffiche = False

        self.frameMenuPrincipal.pack(side = TOP,
                                     expand = True,
                                     fill = BOTH)

        self.labBGMenuPrincipal.place(x = 0,
                                      y = 0,
                                      relwidth = 1,
                                      relheight = 1)

        self.frameMenuPrincipalCentre.pack(side = TOP,
                                           expand = True)

        self.labTitreSim.pack(fill = X,
                              padx = 40,
                              pady = 20)

        for btn in self.btnMenuPrincipal:
            if btn["text"] == "Reprendre la simulation" and not self.modele.simEnCours:
                continue

            btn.pack(fill = X,
                     padx = 7,
                     pady = 7)

        self.labCopyrightsMenuPrincipal.pack(side = BOTTOM,
                                             padx = 15,
                                             pady = 15)
    def afficherInstructions(self):                                            # Affiche les instructions
        self.nettoyerEcran()

        self.frameInstructions.pack(side = TOP,
                                    expand = True,
                                    fill = BOTH)

        self.labBGInstructions.place(x = 0,
                                     y = 0,
                                     relwidth = 1,
                                     relheight = 1)

        self.frameInstructionsCentre.pack(side = TOP,
                                          expand = True)

        self.labTitreInstructions.pack(fill = X,
                                       padx = 40,
                                       pady = 20)

        self.mesInstructions.pack(fill = X,
                                  padx = 7,
                                  pady = 7)

        self.btnInstructionsRetourMenuPrincipal.pack(fill = X,
                                                     padx = 7,
                                                     pady = 7)

        self.labCopyrightsInstructions.pack(side = BOTTOM,
                                            padx = 15,
                                            pady = 15)

    def afficherOptions(self):
        self.nettoyerEcran()

        self.frameMenuOptions.pack(side = TOP,
                                      expand = True,
                                      fill = BOTH)

        self.labBGMenuOptions.place(x = 0,
                                       y = 0,
                                       relwidth = 1,
                                       relheight = 1)

        self.frameMenuOptionsCentre.pack(side = TOP,
                                            expand = True)

        self.labTitreMenuOptions.pack(fill = X,
                                         padx = 40,
                                         pady = 20)

        self.frameOptions.pack(fill = X)

        compteur = 0

        for lab in self.labOptions:
            lab.grid(row = compteur,
                     column = 0,
                     padx = 7,
                     pady = 7,
                     sticky = "W")
            compteur += 1

        self.optMenuResolution.grid(row = 0,
                                    column = 1,
                                    padx = 7,
                                    pady = 7,
                                    sticky = "W")

        self.optMenuPleinEcran.grid(row = 1,
                                    column = 1,
                                    padx = 7,
                                    pady = 7,
                                    sticky = "W")

        self.optMenuMusique.grid(row = 2,
                                 column = 1,
                                 padx = 7,
                                 pady = 7,
                                 sticky = "W")

        self.btnOptionsRetourMenuPrincipal.pack(fill = X,
                                                padx = 7,
                                                pady = 7)

        self.labCopyrightsMenuOptions.pack(side = BOTTOM,
                                              padx = 15,
                                              pady = 15)

    def afficherMenuOptionsGen(self):                                            # Affiche le menu d'options de la génération du monde
        self.nettoyerEcran()

        # Réinitialize les choix
        self.varPopVegetale.set(self.choixVarPopVegetale[2])
        self.varPopAnimale.set(self.choixVarPopAnimale[2])
        self.varNivEau.set(self.choixVarNivEau[2])
        self.varElevationTerrain.set(self.choixVarElevationTerrain[2])

        self.frameMenuOptionsGen.pack(side = TOP,
                                      expand = True,
                                      fill = BOTH)

        self.labBGMenuOptionsGen.place(x = 0,
                                       y = 0,
                                       relwidth = 1,
                                       relheight = 1)

        self.frameMenuOptionsGenCentre.pack(side = TOP,
                                            expand = True)

        self.labTitreMenuOptionsGen.pack(fill = X,
                                         padx = 40,
                                         pady = 20)

        self.frameOptionsGen.pack()
        compteur = 0

        for lab in self.labOptionsGen:
            lab.grid(row = compteur,
                     column = 0,
                     padx = 7,
                     pady = 7,
                     sticky = "W")
            compteur += 1

        self.optMenuPopVegetale.grid(row = 0,
                                     column = 1,
                                     padx = 7,
                                     pady = 7,
                                     sticky = "W")

        self.optMenuPopAnimale.grid(row = 1,
                                    column = 1,
                                    padx = 7,
                                    pady = 7,
                                    sticky = "W")

        self.optMenuNivEau.grid(row = 2,
                                column = 1,
                                padx = 7,
                                pady = 7,
                                sticky = "W")

        self.optMenuElevationTerrain.grid(row = 3,
                                          column = 1,
                                          padx = 7,
                                          pady = 7,
                                          sticky = "W")

        self.entNoyau.grid(row = 4,
                           column = 1,
                           padx = 7,
                           pady = 7,
                           sticky = "W")

        self.frameProcederOuRetourner.pack(fill = X)

        self.btnOptionsGenRetourMenuPrincipal.grid(row = 0,
                                                   column = 0,
                                                   padx = 7,
                                                   pady = 7)

        self.btnDemarrerSim.grid(row = 0,
                                 column = 1,
                                 padx = 7,
                                 pady = 7)

        self.labCopyrightsMenuOptionsGen.pack(side = BOTTOM,
                                              padx = 15,
                                              pady = 15)

    def afficheMonde(self):                                                     # Affiche le monde de la simulation
        self.nettoyerEcran()

        self.mondeAffiche = True

        self.frameMonde.pack(side = TOP,
                             expand = True,
                             fill = BOTH)

        self.frameControles.pack(side = RIGHT,
                                 fill = Y)

        self.btnRetourMenu.pack(fill = X,
                                padx = 7,
                                pady = 7)

        self.btnOutilsSim.pack(fill = X,
                                padx = 7,
                                pady = 7)

        self.canvasCarte.pack(padx = 7,
                              pady = 7)

        self.labTemps.pack(fill = X,
                           padx = 7,
                           pady = 7)

        self.labMultiplicateurTemps.pack(fill = X)

        self.entTemps.pack(fill = X,
                           padx = 7,
                           pady = 7)

        self.btnPause.pack(fill = X,
                           padx = 7,
                           pady = 7)

        self.labPopulations.pack(fill = X,
                                 padx = 7)

        self.framePopulations.pack(padx = 7,
                                   pady = 7)

        compteur = 0

        for labPopAnimaux in self.labPopAnimaux:
            labPopAnimaux[0].grid(row = compteur,
                                  column = 0,
                                  sticky = "W")
            compteur += 1

        compteur = 0

        for labPopVegetaux in self.labPopVegetaux:
            labPopVegetaux[0].grid(row = compteur,
                                   column = 1,
                                   sticky = "W")
            compteur += 1

        self.canvasMonde.pack(side = LEFT)

        self.afficherEnvironnement(echelle = self.echelle)

    def afficherEnvironnement(self, echelle = 1):
        # Efface tout le canvas
        self.canvasMonde.delete(ALL)
        self.canvasCarte.delete("Caméra")

        if self.modele.changementSaison:
            self.canvasCarte.delete(ALL)

        # Jour ou nuit
        debutJour = 6
        debutNuit = 18
        transition = 2
        heure = int(self.modele.temps.strftime("%H"))
        minutes = int(self.modele.temps.strftime("%M"))

        if heure >= debutJour and heure < debutNuit - transition:
            eclairage = 0
        elif heure >= debutNuit or heure < debutJour - transition:
            eclairage = 100
        elif heure >= debutJour - transition and heure < debutJour:
            eclairage = 100 - (((heure - debutJour + transition) * 60 + minutes) * 100 / (transition * 60))
        else:
            eclairage = ((heure - debutNuit + transition) * 60 + minutes) * 100 / (transition * 60)

        # Changement de couleur du background pour les cycles de jour et de nuit
        self.canvasMonde.configure(bg = self.luminositeCouleurHex(self.couleurBG, -int(eclairage * 2.1)))
        self.canvasCarte.configure(bg = self.luminositeCouleurHex(self.couleurBG, -int(eclairage * 2.1)))
        # Échelle de la carte
        echelleCarte = self.echelleCarte
        # Calcule la largeur et la hauteur de la matrice de l'environnement
        largeurMatrice = len(self.modele.environnement)
        hauteurMatrice = len(self.modele.environnement[0])
        # Calcule le centre de la matrice par rapport à l'écran
        centreX = self.root.winfo_width() // 2
        centreY = self.root.winfo_height() // 2 - (largeurMatrice + hauteurMatrice - 1) * echelle * 75 // 2 + self.elevation * echelleCarte
        centreXMini = 100
        centreYMini = 100 - (largeurMatrice + hauteurMatrice - 1) * echelleCarte * 75 // 2 + self.elevation * echelleCarte
        # Sert à calculer la position lors de l'affichage de la matrice
        affichageX = 0
        affichageY = 0
        limiteAffichage = 200 * echelle
        largeurEcran = self.root.winfo_width()
        hauteurEcran = self.root.winfo_height()

        # =====[Affiche le monde et la carte]=====
        # Pour tout les y de la matrice
        for y in range(hauteurMatrice):
            # L'on donne la valeur y au compteur et le le décremente à chaque fois qu'on se déplace dans le tableau pour ainsi le parcourir en diagonal
            compteurY = y

            # Parcour tout les x de la matrice
            for x in range(largeurMatrice):
                # Si le compteur est plus bas que 0, c'est que l'on doit changer de rangée
                if compteurY < 0:
                    break

                # Calcule les coordonnées de la case en question
                coordX = affichageX * -75 * echelle + x * 150 * echelle + centreX + self.positionXCamera
                coordY = affichageY * 75 * echelle + centreY + self.positionYCamera
                coordXMini = affichageX * -75 * echelleCarte + x * 150 * echelleCarte + centreXMini
                coordYMini = affichageY * 75 * echelleCarte + centreYMini

                if self.modele.changementSaison:
                    self.afficherCase(self.canvasCarte, coordXMini, coordYMini, self.modele.environnement[compteurY][x][0], echelleCarte, x, compteurY, 0)

                if coordX > -limiteAffichage and coordX < largeurEcran + limiteAffichage and coordY > -limiteAffichage and coordY < hauteurEcran + limiteAffichage + self.elevation * echelle * 2:
                    #Affiche les cases
                    self.afficherCase(self.canvasMonde, coordX, coordY, self.modele.environnement[compteurY][x][0], echelle, x, compteurY, eclairage)

                    # Affiche les végétaux
                    if self.modele.environnement[compteurY][x][2] != None:
                        self.afficherPlantes(self.modele.environnement[compteurY][x][2], coordX, coordY, self.modele.environnement[compteurY][x][0], echelle, x, compteurY)

                    # Affiche les animaux
                    if self.modele.environnement[compteurY][x][1] != None:
                        self.afficherAnimaux(self.modele.environnement[compteurY][x][1], coordX, coordY, self.modele.environnement[compteurY][x][0], echelle, x, compteurY)

                    elif isinstance(self.modele.environnement[compteurY][x][1], habitation.Terrier):
                        self.afficherTerrier(coordX, coordY, self.modele.environnement[compteurY][x][0], echelle, x, compteurY)
                compteurY -= 1

            if y < hauteurMatrice - 1:
                affichageX += 1

            affichageY += 1

        # Parcour tout les x à partir de 1 jusqu'à la fin de la matrice
        for x in range(1, largeurMatrice):
            # L'on donne la valeur x au compteur et le le décremente à chaque fois qu'on se déplace dans le tableau pour ainsi le parcourir en diagonal
            compteurX = x
            affichageX -= 1
            compteurAffichageX = 0

            # L'on parcours tout les y en ordre inverse pour se déplacer dans le tableau en diagonale
            for y in reversed(range(hauteurMatrice)):
                # Si le compteur dépasse la limite de la matrice, c'est que l'on doit changer de rangée
                if compteurX > largeurMatrice - 1:
                    break

                # Calcule les coordonnées de la case en question
                coordX = affichageX * -75 * echelle + compteurAffichageX * 150 * echelle + centreX + self.positionXCamera
                coordY = affichageY * 75 * echelle + centreY + self.positionYCamera
                coordXMini = affichageX * -75 * echelleCarte + compteurAffichageX * 150 * echelleCarte + centreXMini
                coordYMini = affichageY * 75 * echelleCarte + centreYMini

                if self.modele.changementSaison:
                    self.afficherCase(self.canvasCarte, coordXMini, coordYMini, self.modele.environnement[y][compteurX][0], echelleCarte, compteurX, y, 0)

                if coordX > -limiteAffichage and coordX < largeurEcran + limiteAffichage and coordY > -limiteAffichage and coordY < hauteurEcran + limiteAffichage + self.elevation * echelle * 2:
                    #Affiche les cases
                    self.afficherCase(self.canvasMonde, coordX, coordY, self.modele.environnement[y][compteurX][0], echelle, compteurX, y, eclairage)

                    # Affiche les végétaux
                    if self.modele.environnement[y][compteurX][2] != None:
                        self.afficherPlantes(self.modele.environnement[y][compteurX][2], coordX, coordY, self.modele.environnement[y][compteurX][0], echelle, compteurX, y)

                    # Affiche les animaux
                    if self.modele.environnement[y][compteurX][1] != None:
                        self.afficherAnimaux(self.modele.environnement[y][compteurX][1], coordX, coordY, self.modele.environnement[y][compteurX][0], echelle, compteurX, y)

                    if isinstance(self.modele.environnement[y][compteurX][1], habitation.Terrier):
                        self.afficherTerrier(coordX, coordY, self.modele.environnement[y][compteurX][0], echelle, compteurX, y)
                compteurX += 1
                compteurAffichageX += 1

            affichageY += 1
        # ====================================


        ratioEchelle = echelleCarte / echelle
        offsetTuile = 150 * ratioEchelle / 2
        largeurFrameControles = 200 * ratioEchelle
        largeurEcranMini = largeurEcran * ratioEchelle / 2
        hauteurEcranMini = hauteurEcran * ratioEchelle / 2
        positionXCameraMini = self.positionXCamera * ratioEchelle
        positionYCameraMini = self.positionYCamera * ratioEchelle

        # Affiche la position de la caméra dans la carte
        self.canvasCarte.create_rectangle(100 - largeurEcranMini - positionXCameraMini,
                                          100 - hauteurEcranMini + self.elevation * ratioEchelle - positionYCameraMini - offsetTuile,
                                          100 + largeurEcranMini - positionXCameraMini - largeurFrameControles,
                                          100 + hauteurEcranMini + self.elevation * ratioEchelle - positionYCameraMini - offsetTuile,
                                          outline = "#CC0000",
                                          tag = "Caméra")

    def afficherAnimaux(self, animal, coordX, coordY, elevation, echelle, caseX, caseY):
        # Regarde le niveau de l'eau
        if elevation < self.modele.nivEau:
            hauteur = self.modele.nivEau
        else:
            hauteur = elevation

        # Calcule les coordonnées y
        hauteurMultiplicateur = self.elevation * echelle
        coordY = coordY - hauteur * hauteurMultiplicateur - hauteurMultiplicateur

        # Affiche l'animal selon son type
        if isinstance(animal, animaux.Lapin):
            self.canvasMonde.create_image(coordX,
                                          coordY + 30 * echelle,
                                          anchor = "s",
                                          image=self.imagesAnimaux[1],
                                          tags = (str(caseX), str(caseY),"Lapin"))
        elif isinstance(animal, animaux.Loup):
            self.canvasMonde.create_image(coordX,
                                          coordY + 30 * echelle,
                                          anchor = "s",
                                          image= self.imagesAnimaux[0],
                                          tags = (str(caseX), str(caseY),"Loup"))
        elif isinstance(animal, animaux.Ours):
            self.canvasMonde.create_image(coordX,
                                          coordY + 40 * echelle,
                                          anchor = "s",
                                          image= self.imagesAnimaux[2],
                                          tags = (str(caseX), str(caseY),"Ours"))
        elif isinstance(animal, animaux.Lievre):
            self.canvasMonde.create_image(coordX,
                                          coordY + 40 * echelle,
                                          anchor = "s",
                                          image= self.imagesAnimaux[3],
                                          tags = (str(caseX), str(caseY),"Lièvre"))
        elif isinstance(animal, animaux.Bison):
            self.canvasMonde.create_image(coordX,
                                          coordY + 40 * echelle,
                                          anchor = "s",
                                          image= self.imagesAnimaux[4],
                                          tags = (str(caseX), str(caseY),"Bison"))
    
    

    def afficherPlantes(self, plante, coordX, coordY, elevation, echelle, caseX, caseY):
        # Regarde le niveau de l'eau
        if elevation < self.modele.nivEau:
            hauteur = self.modele.nivEau
        else:
            hauteur = elevation

        # Calcule les coordonnées y
        hauteurMultiplicateur = self.elevation * echelle
        coordY = coordY - hauteur * hauteurMultiplicateur - hauteurMultiplicateur

        if plante.attributes["perteFeuilles"] is False:
        #if self.modele.getSaison() == "ete" or self.modele.getSaison() == "printemps" or self.modele.getSaison() == "automne":
            # Affiche la plante selon son type
            if isinstance(plante, vegetaux.Ble):
                self.canvasMonde.create_image(coordX,
                                            coordY + 50 * echelle,
                                            anchor = "s",
                                            image = self.imagesPlantes[0],
                                            tags = (str(caseX), str(caseY), "Blé"))
            elif isinstance(plante, vegetaux.Erable):
                self.canvasMonde.create_image(coordX,
                                            coordY + 10 * echelle,
                                            anchor = "s",
                                            image = self.imagesPlantes[1],
                                            tags = (str(caseX), str(caseY),"Érable"))
            elif isinstance(plante, vegetaux.Laitue):
                self.canvasMonde.create_image(coordX,
                                            coordY + 45 * echelle,
                                            anchor = "s",
                                            image = self.imagesPlantes[2],
                                            tags = (str(caseX), str(caseY),"Laitue"))
            elif isinstance(plante, vegetaux.Peuplier):
                self.canvasMonde.create_image(coordX,
                                            coordY + 10 * echelle,
                                            anchor = "s",
                                            image = self.imagesPlantes[4],
                                            tags = (str(caseX), str(caseY),"Peuplier"))
            elif isinstance(plante, vegetaux.Cerisier):
                self.canvasMonde.create_image(coordX,
                                            coordY + 10 * echelle,
                                            anchor = "s",
                                            image = self.imagesPlantes[5],
                                            tags = (str(caseX), str(caseY),"Cerisier"))
            elif isinstance(plante, vegetaux.Sapin):
                self.canvasMonde.create_image(coordX,
                                            coordY + 15 * echelle,
                                            anchor = "s",
                                            image = self.imagesPlantes[6],
                                            tags = (str(caseX), str(caseY),"Sapin"))
        else:
            if isinstance(plante, vegetaux.Peuplier):
                self.canvasMonde.create_image(coordX,
                                            coordY + 10 * echelle,
                                            anchor = "s",
                                            image = self.imagesPlantesHiver[0],
                                            tags = (str(caseX), str(caseY),"Peuplier"))
            elif isinstance(plante, vegetaux.Cerisier):
                self.canvasMonde.create_image(coordX,
                                            coordY + 10 * echelle,
                                            anchor = "s",
                                            image = self.imagesPlantesHiver[1],
                                            tags = (str(caseX), str(caseY),"Cerisier"))
            elif isinstance(plante, vegetaux.Erable):
                self.canvasMonde.create_image(coordX,
                                            coordY + 10 * echelle,
                                            anchor = "s",
                                            image = self.imagesPlantesHiver[1],
                                            tags = (str(caseX), str(caseY),"Érable"))
            elif isinstance(plante, vegetaux.Sapin):
                self.canvasMonde.create_image(coordX,
                                            coordY + 15 * echelle,
                                            anchor = "s",
                                            image = self.imagesPlantesHiver[2],
                                            tags = (str(caseX), str(caseY),"Sapin"))


    def afficherTerrier(self, coordX, coordY, elevation, echelle, caseX, caseY):
        # Regarde le niveau de l'eau
        if elevation < self.modele.nivEau:
            hauteur = self.modele.nivEau
        else:
            hauteur = elevation

        # Calcule les coordonnées y
        hauteurMultiplicateur = self.elevation * echelle
        coordY = coordY - hauteur * hauteurMultiplicateur - hauteurMultiplicateur

        #afficher les terriers pour les lapins
        self.canvasMonde.create_image(coordX,
                                      coordY + 20 * echelle,
                                          anchor = "center",
                                          image= self.imageHabitation[0],
                                          tags = (str(caseX),str(caseY), "Terrier"))

    def afficherCase(self, canvas, x, y, hauteur, echelle, caseX, caseY, eclairage):
        def eau(x, y, hauteur, hauteurFinale, echelle, surface, eclairage):
            # Couleurs de base de l'eau
            couleurEau = "#000088"
            couleurFond = "#806040"
            couleurmultiplicateur = 50

            # Ajustement de l'éclairage
            eclairage /= 2

            # Application du multiplicateur sur les couleurs selon la façade
            couleurLosangeEau = self.luminositeCouleurHex(couleurEau, int(hauteur * couleurmultiplicateur - eclairage))
            couleurParallelogrammeEau1 = self.luminositeCouleurHex(couleurEau, int(hauteur * couleurmultiplicateur - 50 - eclairage))
            couleurParallelogrammeEau2 = self.luminositeCouleurHex(couleurEau, int(hauteur * couleurmultiplicateur - 25 - eclairage))
            couleurParallelogrammeFond1 = self.luminositeCouleurHex(couleurFond, int(hauteur * couleurmultiplicateur - 50 - eclairage))
            couleurParallelogrammeFond2 = self.luminositeCouleurHex(couleurFond, int(hauteur * couleurmultiplicateur - 25 - eclairage))

            # Vu que les cases sont carrées, réduction des calcules pour les coordonnées
            pointCase = 75 * echelle

            # Losange qui forme le dessus de la case (eau)
            canvas.create_polygon([x, y - pointCase - surface,
                                             x + pointCase, y - surface,
                                             x, y + pointCase - surface,
                                             x - pointCase, y - surface],
                                             fill = couleurLosangeEau,
                                             tag = (str(caseX), str(caseY)))
            # Façade supérieur gauche (eau)
            canvas.create_polygon([x - pointCase, y - hauteurFinale,
                                             x, y + pointCase - hauteurFinale,
                                             x, y + pointCase - surface,
                                             x - pointCase, y - surface],
                                             fill = couleurParallelogrammeEau1,
                                             tag = (str(caseX), str(caseY)))
            # Façade supérieur droite (eau)
            canvas.create_polygon([x, y + pointCase - hauteurFinale,
                                             x + pointCase, y - hauteurFinale,
                                             x + pointCase, y - surface,
                                             x, y + pointCase - surface,],
                                             fill = couleurParallelogrammeEau2,
                                             tag = (str(caseX), str(caseY)))
            # Façade inférieur gauche (fond de l'océan)
            canvas.create_polygon([x - pointCase, y,
                                             x, y + pointCase,
                                             x, y + pointCase - hauteurFinale,
                                             x - pointCase, y - hauteurFinale],
                                             fill = couleurParallelogrammeFond1,
                                             tag = (str(caseX), str(caseY)))
            # Façade inférieur droite (fond de l'océan)
            canvas.create_polygon([x, y + pointCase,
                                             x + pointCase, y,
                                             x + pointCase, y - hauteurFinale,
                                             x, y + pointCase - hauteurFinale,],
                                             fill = couleurParallelogrammeFond2,
                                             tag = (str(caseX), str(caseY)))

        def terrain(x, y, hauteur, hauteurFinale, echelle, typeTerrain, eclairage):
            saison = self.modele.getSaison()

            # Couleur de base selon le type de terrain
            if typeTerrain == "Gazon":
                if saison == "hiver":
                    couleur = "#FFFAFA"
                    gradation = -1
                    couleurmultiplicateur = 65
                else:
                    couleur = "#007700"
                    gradation = -1
                    couleurmultiplicateur = 65
            elif typeTerrain == "Montagne":
                if saison == "hiver":
                    couleur = "#FFFFFF"
                    gradation = -1
                    couleurmultiplicateur = 65
                else:
                    couleur = "#777777"
                    gradation = -1
                    couleurmultiplicateur = 75
            elif typeTerrain == "Sommet Montagne":
                couleur = "#AAAAAA"
                gradation = 1
                couleurmultiplicateur = 50
            elif typeTerrain == "Sable":
                if saison == "hiver":
                    couleur = "#FFFAFA"
                    gradation = -1
                    couleurmultiplicateur = 65
                else:
                    couleur = "#FFE675"
                    gradation = 1
                    couleurmultiplicateur = 100

            # Ajustement de l'éclairage
            eclairage /= 2

            # Application du multiplicateur sur les couleurs selon la façade
            couleurLosange = self.luminositeCouleurHex(couleur, int(hauteur * couleurmultiplicateur * gradation - eclairage))
            couleurParallelogramme1 = self.luminositeCouleurHex(couleur, int(hauteur * couleurmultiplicateur * gradation - 50 - eclairage))
            couleurParallelogramme2 = self.luminositeCouleurHex(couleur, int(hauteur * couleurmultiplicateur * gradation - 25 - eclairage))

            # Vu que les cases sont carrées, réduction des calcules pour les coordonnées
            pointCase = 75 * echelle

            # Losange qui forme le dessus de la case
            canvas.create_polygon([x, y - pointCase - hauteurFinale,
                                             x + pointCase, y - hauteurFinale,
                                             x, y + pointCase - hauteurFinale,
                                             x - pointCase, y - hauteurFinale],
                                             fill = couleurLosange,
                                             tag = (str(caseX), str(caseY)))
            # Façade gauche
            canvas.create_polygon([x - pointCase, y,
                                             x, y + pointCase,
                                             x, y + pointCase - hauteurFinale,
                                             x - pointCase, y - hauteurFinale],
                                             fill = couleurParallelogramme1,
                                             tag = (str(caseX), str(caseY)))
            # Façade droite
            canvas.create_polygon([x, y + pointCase,
                                             x + pointCase, y,
                                             x + pointCase, y - hauteurFinale,
                                             x, y + pointCase - hauteurFinale,],
                                             fill = couleurParallelogramme2,
                                             tag = (str(caseX), str(caseY)))

        # Hauteur de la case
        hauteurMultiplicateur = self.elevation * echelle
        hauteurFinale = hauteur * hauteurMultiplicateur + hauteurMultiplicateur

        # Détermination du type de terrain selon la hauteur
        if hauteur < self.modele.nivEau:
            eau(x, y, hauteur, hauteurFinale, echelle, self.modele.nivEau * hauteurMultiplicateur + hauteurMultiplicateur, eclairage)
        elif hauteur < self.modele.listeTerrain[1][1]:
            terrain(x, y, hauteur, hauteurFinale, echelle, "Sable", eclairage)
        elif hauteur < self.modele.listeTerrain[2][1]:
            terrain(x, y, hauteur, hauteurFinale, echelle, "Gazon", eclairage)
        elif hauteur < self.modele.listeTerrain[3][1]:
            terrain(x, y, hauteur, hauteurFinale, echelle, "Montagne", eclairage)
        else:
            terrain(x, y, hauteur, hauteurFinale, echelle, "Sommet Montagne", eclairage)

    def afficherInspecteur(self, typeEntite):
        for enfant in self.frameInspecteur.winfo_children():
            enfant.pack_forget()

        self.frameInspecteur.place_forget()

        self.frameInspecteur.place(x=50,
                                   y=50,
                                   anchor="nw")

        self.labTitreInspecteur.pack(fill = X)

        for i in range(5):
            self.labInfoInspecteur[i].pack(fill = X)

        if typeEntite == 1:
            for i in range(5, 9):
                self.labInfoInspecteur[i].pack(fill = X)

    def afficherOutilsSim(self):                                                # Affiche le monde de la simulation
        self.nettoyerEcran()

        # Réinitialize les choix
        self.varAjouterAnimal.set(self.choixVarAjouterAnimal[0])
        self.varAjouterPlante.set(self.choixVarAjouterPlante[0])

        self.mondeAffiche = False

        self.frameOutilsSim.pack(side = TOP,
                                 expand = True,
                                 fill = BOTH)

        self.labBGOutilsSim.place(x = 0,
                                  y = 0,
                                  relwidth = 1,
                                  relheight = 1)

        self.frameOutilsSimCentre.pack(side = TOP,
                                       expand = True)

        self.labTitreOutilsSim.pack(fill = X,
                                    padx = 40,
                                    pady = 20)

        self.labOutilSimAjouter.pack(fill = X,
                                     padx = 7,
                                     pady = 7)

        self.frameOutilSimSelection.pack()

        self.outilSimAjouterAnimal.grid(row = 1,
                                        column = 0,
                                        padx = 7,
                                        pady = 7,
                                        sticky = "W")

        self.outilSimAjouterPlante.grid(row = 2,
                                        column = 0,
                                        padx = 7,
                                        pady = 7,
                                        sticky = "W")

        self.btnOutilsSimAjouterAnimal.grid(row = 1,
                                            column = 1,
                                            padx = 7,
                                            pady = 7,
                                            sticky = "W")

        self.btnOutilsSimAjouterPlante.grid(row = 2,
                                            column = 1,
                                            padx = 7,
                                            pady = 7,
                                            sticky = "W")

        self.labOutilSimSupprimer.pack(fill = X,
                                       padx = 7,
                                       pady = 7)

        self.btnOutilsSimSupprimer.pack(fill = X,
                                        padx = 7,
                                        pady = 7)

        self.btnRetourSim.pack(fill = X,
                               padx = 7,
                               pady = 7)

    def appliquerMusique(self):                                                 # Joue la musique ou non
        if self.musique:
            winsound.PlaySound("sounds\\color_of_the_wind.wav", winsound.SND_ASYNC|winsound.SND_LOOP)
        else:
            winsound.PlaySound(None, winsound.SND_PURGE)

    def modifierTemps(self):                                                    # Modifie l'affichage du temps
        # Traduit le mois en français
        if self.modele.temps.strftime("%b") == "Jan":
            mois = "Janvier"
        elif self.modele.temps.strftime("%b") == "Feb":
            mois = "Février"
        elif self.modele.temps.strftime("%b") == "Mar":
            mois = "Mars"
        elif self.modele.temps.strftime("%b") == "Apr":
            mois = "Avril"
        elif self.modele.temps.strftime("%b") == "May":
            mois = "Mai"
        elif self.modele.temps.strftime("%b") == "Jun":
            mois = "Juin"
        elif self.modele.temps.strftime("%b") == "Jul":
            mois = "Juillet"
        elif self.modele.temps.strftime("%b") == "Aug":
            mois = "Août"
        elif self.modele.temps.strftime("%b") == "Sep":
            mois = "Septembre"
        elif self.modele.temps.strftime("%b") == "Oct":
            mois = "Octobre"
        elif self.modele.temps.strftime("%b") == "Nov":
            mois = "Novembre"
        elif self.modele.temps.strftime("%b") == "Dec":
            mois = "Décembre"

        # Affiche la date
        date = self.modele.temps.strftime("%d ") + mois + self.modele.temps.strftime(" %Y - %H:%M")
        self.labTemps.configure(text = date)

    def modifierInspecteur(self):
        if isinstance(self.entiteSelectionnee, vegetaux.Plante):
            if self.entiteSelectionnee in self.modele.vegetauxListe:
                index = self.modele.vegetauxListe.index(self.entiteSelectionnee)
                population = 0

                for value in self.modele.vegetauxListe:
                    if type(self.entiteSelectionnee) is type(value) :
                        if value.attributes["mature"]:
                            population += 1

                self.labInfoInspecteur[0].configure(text = self.entiteSelectionnee.__class__.__name__)
                self.labInfoInspecteur[1].configure(text = "ID : " + str(id(self.modele.vegetauxListe[index])))
                self.labInfoInspecteur[2].configure(text = "Population : " + str(population))
                self.labInfoInspecteur[3].configure(text = "Date De Naissance : " + self.modele.vegetauxListe[index].attributes["naissance"].strftime("%d/%m/%Y - %H:%M"))
                self.labInfoInspecteur[4].configure(text = "Esperence De Vie : " + str(self.modele.vegetauxListe[index].attributes["esperanceVie"]) + " jours")
            else:
                self.frameInspecteur.place_forget()
        elif isinstance(self.entiteSelectionnee, animaux.Animal):
            if self.entiteSelectionnee in self.modele.animauxListe:
                index=self.modele.animauxListe.index(self.entiteSelectionnee)
                population = 0

                for value in self.modele.animauxListe:
                    if type(self.entiteSelectionnee) is type(value) :
                        population += 1

                sexeAnimal = self.modele.animauxListe[index].attributes["sexe"]
                if sexeAnimal:
                    sexe="Une femelle"
                else :
                    sexe="Un male"

                comportement = self.modele.animauxListe[index].attributes["prioriteComportement"]
                dictValuesComportement = {
                    0 : "En fuite",
                    1 : "Sommeil",
                    2 : "Affamé",
                    3 : "Assoifé",
                    4 : "Reproduction",
                    5 : "Aucun prédateur en vue"
                }

                partenaire = self.modele.animauxListe[index].attributes["partenaire"]
                if not partenaire:
                    partenaire = "Aucun partenaire pour le moment"

                self.labInfoInspecteur[0].configure(text = self.entiteSelectionnee.__class__.__name__)
                self.labInfoInspecteur[1].configure(text = "ID : " + str(id(self.modele.animauxListe[index])))
                self.labInfoInspecteur[2].configure(text = "Population : " + str(population))
                self.labInfoInspecteur[3].configure(text = "Sexe : " + sexe)
                self.labInfoInspecteur[4].configure(text = "Date De Naissance : " + self.modele.animauxListe[index].attributes["age"].strftime("%d/%m/%Y - %H:%M"))
                self.labInfoInspecteur[5].configure(text = "Son Comportement : " + dictValuesComportement[comportement])
                self.labInfoInspecteur[6].configure(text = "Ses Partenaires Sont : " + str(partenaire))
                self.labInfoInspecteur[7].configure(text = "Vision : " + str(self.modele.animauxListe[index].attributes["vision"]))
                if len(self.modele.animauxListe[index].attributes["champVision"])<=0:
                    self.labInfoInspecteur[8].configure(text = "Aperçoit : " + str("aucun animal est dans le champ de vision"))
                else:
                    self.labInfoInspecteur[8].configure(text = "Aperçoit : " + str(self.modele.animauxListe[index].attributes["champVision"]))
            else:
                self.frameInspecteur.place_forget()

    def modifierPopulations(self):
        for labPopAnimaux in self.labPopAnimaux:
            compteur = 0

            for animal in self.modele.animauxListe:
                if isinstance(animal, self.modele.dictionnaireAnimaux[labPopAnimaux[1]][0]):
                    compteur += 1

            labPopAnimaux[0].configure(text = labPopAnimaux[1] + ": " + str(compteur))

        for labPopVegetaux in self.labPopVegetaux:
            compteur = 0

            for plante in self.modele.vegetauxListe:
                if isinstance(plante, self.modele.dictionnaireVegetaux[labPopVegetaux[1]][0]):
                    if plante.attributes["mature"]:
                        compteur += 1

            labPopVegetaux[0].configure(text = labPopVegetaux[1] + ": " + str(compteur))

if __name__ == '__main__':
    print("Dans Vue")
