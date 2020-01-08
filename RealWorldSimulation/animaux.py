
# -*- coding: utf-8 -*-
import random
import vegetaux
import habitation
import datetime as dt
import math
class Animal():
    def __init__(self, parent):
        self.parent = parent
        esperanceHours = 17520+random.randrange(0, 8760)
        self.attributes = {
            "tempsActuelGest": 0,
            "tempsBesoinsGest": None,
            "enGestation": False,
            "partenaire": [],  # liste de partenaire
            "primeMate": False,  # partenaire de reproduction en vue
            "champVision": [],
            "terrestre": False,  # bool if 1 c un terrestre
            "aquatique": False,  # bool if 1 c un aquatique animal
            "vol": False,  # bool if 1 c un bird
            "posX": 0,
            "posY": 0,
            "cibleX": None,
            "cibleY": None,
            "age": self.parent.temps,
            "esperenceVie": esperanceHours,
            "nivSoif": random.randrange(10),
            "nivFaim": random.randrange(0, 50),
            "proie": [],
            "vision": 0,
            "taille": 0,
            "valeurNutritive": None,
            "vie": 100,
            "sante": [],
            "nivSomeil": random.randrange(0, 40),
            "temperature": [],  # array avec min max de temperature est ideal
            "nbrEnfantsPossible": 1,
            "tempsEntre2Portee": 15,  # en jours "intervalle"
            "vitesse": None,
            "state": ["sleep", "hibernation", "awake"],
            "estMalade": False,
            "enemySeen": False,
            "allySeen": False,
            "foodSeen": False,
            "enFuite": False,
            "enFood": False,
            "sexe": random.randrange(0, 2),
            # a verifier pour la fonctionaliter
            "portee": random.randrange(3, 6),
            # 0=danger(fuire) 1=dodo  2=manger  3=boire 4=reproduction 5=deplacementLibrement 6=accouchement(repos sur place)
            "prioriteComportement": 5,
            "ageDeFecondation": 0,
            "nbrAccouchementFaits": 0,  # a verifier pour la fonctionalite
            # [ [listepredateur] [listeBouffe] ]
            "caracteristiqueBiome": [None, [], [],[] ],
            # periodes d activite minuit a 3am et , 6am a 9pm
            "horlogeBio": [[0, 3], [6, 9]],
            "last_sleep": self.parent.temps,
            "last_dinner": self.parent.temps,
            "last_drink": self.parent.temps,
            "avgEnActivite": 4,  # temps moyen que le lapin reste en activite , il devient fatigue
            "tempsAbstentionBouffe": 4,  # apres 4 h il a faim
            "tempsAbstentionBouffeMax": 72,  # apres 72h cest impossible qu il survive
            "litresEauBu": 0,
            # boit entre 50 et 150 ml/jour.
            "litresEauAverage": random.randrange(50, 150),
            "desydratation": 3, # 3 jours maximum sans eau sinon la mort
            "enVoieDeReproduction":0, #0=non 1=oui
            "habitation":[], # liste des habitations
            "dansHabit":False
        }

        self.attributes["gestation"] = [self.attributes["tempsActuelGest"], self.attributes["tempsBesoinsGest"],self.attributes["partenaire"], self.attributes["tempsEntre2Portee"]]
        self.attributes["state"] = "awake"  # reveille  des le depart

    def ageActuelleHours(self):
        """une operation mathematique sur deux dates(dateTime Object retourne un objet TimeDelta)"""
        """afin d extraire l heure ou le jour ou la minute  d<un objet timedelta, il faut appeller la fonction elle retourne un tableau[days,hours,minutes] """

        ageHours = self.days_hours_minutes(self.parent.temps-self.attributes["age"])[1]
        return ageHours

    def genererCibleDepart(self):
        """ Permet de gener une cible de depart , soit une case terreste"""
        cibleX = random.randrange(self.parent.dimensionsTerrain - 1)
        cibleY = random.randrange(self.parent.dimensionsTerrain - 1)
        
        while(self.parent.environnement[cibleY][cibleX][0] < self.parent.nivEau):
            cibleX = random.randrange(self.parent.dimensionsTerrain - 1)
            cibleY = random.randrange(self.parent.dimensionsTerrain - 1)

        self.attributes["cibleY"] = cibleY
        self.attributes["cibleX"] = cibleX

    def verifierLaFaim(self):
        # priorite a la recherche de nourriture  et qu'il y a des proies dans sa liste
        if self.days_hours_minutes(self.parent.temps-self.attributes["last_dinner"])[1] > self.attributes["tempsAbstentionBouffe"]:
            # pour savoir si (depuis combien de temps il a pas mange)> abstention
            # trigger le comportement Faim
            self.attributes["prioriteComportement"] = 2

        if self.attributes["prioriteComportement"] == 2 and len(self.attributes["proie"]) > 0:
            proie = self.attributes["proie"][0]
            self.attributes["cibleX"] = proie.attributes["posX"]
            self.attributes["cibleY"] = proie.attributes["posY"]
            
            if self.attributes["posX"] == self.attributes["cibleX"] and self.attributes["posY"] == self.attributes["cibleY"]:
                if issubclass(type(proie), vegetaux.Plante):
                    self.manger(proie)
                else:
                    if proie.attributes["dansHabit"] == False:
                        self.manger(proie)
                    else:
                        self.attributes["prioriteComportement"] = 2

        elif self.days_hours_minutes(self.parent.temps-self.attributes["last_dinner"])[1] > self.attributes["tempsAbstentionBouffeMax"]:
            # signal trigger la mort dans verifier Mort
            self.attributes["vie"] = 0

    def manger(self, proie):
        # comme une plante peut nourrir plusieurs animaux , elle ne meurt pas directement
        # un animal qui se fait attaquer est mort sur le coup
        nbrVieRetire = 10
        if(issubclass(type(proie), vegetaux.Plante)):
            # meme si on mange cette plante elle restera en vie
            if(proie.attributes["vie"] - nbrVieRetire >= 0):
                proie.attributes["vie"] -= nbrVieRetire
                self.attributes["nivFaim"] = 0

            else:  # si on mange cette plante et qu elle nest plu en vie
                if proie in self.parent.vegetauxListe:
                    self.parent.vegetauxListe.remove(proie)

        elif proie in self.parent.animauxListe:  # soit un animal
            self.attributes["proie"].remove(proie)
            self.parent.animauxListe.remove(proie)

        # timestamp du diner
        self.attributes["last_dinner"] = self.parent.temps
        self.attributes["proie"].clear()
        self.attributes["prioriteComportement"]=5#retour a la normale apres avoir mange

    def boire(self):
        pass

    # fuire est en fait juste un swap de vitesse, donc, on l'utilise aussi pour la chasse
    def fuire(self):
        temp = self.attributes["delaiDeDep"]
        self.attributes["delaiDeDep"] = self.attributes["delaiDeFuite"]
        self.attributes["delaiDeFuite"] = temp

    def maladie(self):
        pass

    def nouvelleDestinationPreferences(self):
        # tant que la cible n est pas de l eau et que les lapins n occupent pas 70% de la map
        # cest ce while qui avait des repercussions majeures sur la lenteur
        cibleX = random.randrange(self.parent.dimensionsTerrain - 1)
        cibleY = random.randrange(self.parent.dimensionsTerrain - 1)
        while (self.parent.environnement[self.attributes["cibleY"]][self.attributes["cibleX"]][0] < self.parent.nivEau and len(self.parent.animauxListe) < ((32*32)*0.7)):
            cibleX = random.randrange(self.parent.dimensionsTerrain - 1)
            cibleY = random.randrange(self.parent.dimensionsTerrain - 1)

        self.attributes["cibleX"] = cibleX
        self.attributes["cibleY"] = cibleY

    def deplacer(self):
        if self.attributes["state"] == "awake":
            deplacementDansEau = True
            self.parent.environnement[self.attributes["posY"]
                                      ][self.attributes["posX"]][1] = None
            prochainX = self.attributes["posX"]
            prochainY = self.attributes["posY"]
            tempX = self.attributes["posX"]
            tempY = self.attributes["posY"]
            vitesse = self.attributes["vitesse"]
            while deplacementDansEau is True:
                if self.attributes["cibleX"] < prochainX:
                    prochainX -= vitesse
                elif self.attributes["cibleX"] > prochainX:
                    prochainX += vitesse
                if self.attributes["cibleY"] < prochainY:
                    prochainY -= vitesse
                elif self.attributes["cibleY"] > prochainY:
                    prochainY += vitesse

                if self.parent.environnement[prochainY][prochainX][0] > self.parent.nivEau:
                    deplacementDansEau = False
                    self.attributes["posX"] = prochainX
                    self.attributes["posY"] = prochainY
                else:
                    self.attributes["cibleX"] = random.randrange(
                        self.parent.dimensionsTerrain - 1)
                    self.attributes["cibleY"] = random.randrange(
                        self.parent.dimensionsTerrain - 1)
                    prochainX = tempX
                    prochainY = tempY

    def isReadyForFecondation(self, i):
        # Condition1= femele peut encore accouche  # une femele ne peut pas accoucher toute sa vie, la portee est le nombre d'accouchement dans l
        # Condition2= sexe est different
        # Condition3= les 2 inidividus ont pour comportement la reproduction
        # Condition4= si  i.age et self.age >=  age de fecondation (maturite sexuelle)
        # condition5= meme espece
        #condition6= last_accouchement > tempsEntre2Portee
        return (self.attributes["nbrAccouchementFaits"] <= self.attributes["portee"] and i.attributes['sexe'] != self.attributes['sexe'] and self.attributes["prioriteComportement"] == 4 and i.attributes["prioriteComportement"] == 4 and all(x >= self.attributes['ageDeFecondation'] for x in (i.ageActuelleHours(), self.ageActuelleHours())) and type(i) is type(self) and self.attributes["last_accouchement"].day >= self.attributes["tempsEntre2Portee"])


    def isReadyForChildbirth(self):
        return self.attributes["gestation"][0].hour >= self.attributes["gestation"][1]

    def startReproduction(self):
        self.attributes["primeMate"] = True
        if(self.attributes["sexe"] == 0):
            self.attributes["enGestation"] = True
            # debut Gestation = date actuelle
            self.attributes["gestation"][0] = self.parent.temps

    def verifierLaNaissance(self):  # jour J pour l accouchement
        if self.attributes["sexe"] == 0 and self.attributes["enGestation"] is True:
            if self.isReadyForChildbirth():
                # les femmes mettent au monde 3 a 12 lapins par portee
                for i in range(self.attributes["nbrEnfantsPossible"]):
                    if(i.__class__.__name__=="Lapin"):
                        enfant = Lapin(self.parent, self.attributes["posX"], self.attributes["posY"], random.randrange(2))
                    elif(i.__class__.__name__=="Loup"):
                        enfant = Loup(self.parent, self.attributes["posX"], self.attributes["posY"], random.randrange(2))

                    elif(i.__class__.__name__=="Ours"):
                        enfant = Ours(self.parent, self.attributes["posX"], self.attributes["posY"], random.randrange(2))
                    # placer enfant dans self.environnement...!!!!!!!!!!!
                    self.parent.animauxListe.append(enfant)

                self.attributes["enGestation"] = False
                self.attributes["gestation"][0] = None
                self.attributes["readyPourReproduction"] = False
                self.attributes["primeMate"] = False  # pas de partenaire
                self.attributes["nbrAccouchementFaits"] += 1
                self.attributes["last_accouchement"]=self.parent.temps
                self.attributes["prioriteComportement"]=6 #repos accouchement
                # self.attributes["joursDepuisLastReproduction"]=0


    def verifierAccouplement(self):
        """ Cette methode verifie si les membres du couple potentiel sont a la meme case"""
        if (self.attributes["enVoieDeReproduction"]) == 1 :
            positionA = (self.attributes["posX"], self.attributes["posY"])
            partenaire = self.attributes["partenaire"][0]
            positionB = (partenaire.attributes["posX"], partenaire.attributes["posY"])
            if(positionA == positionB):
                self.attributes["enVoieDeReproduction"] = 0 #il est arrive au lieu de reproduction
                self.startReproduction()



    def updateChampvision(self,listeToCheck,instanceParentAnimalCall):
        maVisionRayon = int(self.attributes["vision"]/2)
        for i in listeToCheck:
            if(i is not instanceParentAnimalCall):  # to avoid same object comparaison
                # verifier dans son champs de vision  +1 sur la borne exclusive est important
                if (i.attributes["posX"] in range(self.attributes["posX"]-maVisionRayon, self.attributes["posX"]+maVisionRayon+1) and (i.attributes["posY"] in range(self.attributes["posY"]-maVisionRayon,  self.attributes["posY"]+maVisionRayon+1))):
                    self.attributes["champVision"].append(i)

    def verifierAlentour1(self, instanceParentAnimalCall):
        #nested method
        def comportementsSelonChampVision():
            for i in self.attributes["champVision"]:
                # si i est un amimal enemi
                if type(i) in self.attributes["caracteristiqueBiome"][1]:
                    self.attributes["enemySeen"] = True
                    self.attributes["allySeen"] = False
                    break  # break car des qu un enemi est visible, ca ne sert a rien de verifier de la bouffe / reproduction
                if(type(i) is type(self)):
                    self.attributes["allySeen"]=True

                if type(i) in self.attributes["caracteristiqueBiome"][2]:
                    self.attributes["foodSeen"] = True
                    self.attributes["proie"].append(i)
                #caracteristiqueBiome[3] est sa liste d'habitation dans lequel il peut habiter
                if type(i) in self.attributes["caracteristiqueBiome"][3] and len(self.attributes["habitation"]) == 0:
                    # on ajoute l'habitation
                    self.attributes["habitation"].append(i)

                """afin de voir si la femele est en mesure de se reproduire """
                if self.attributes["sexe"] == 0:  # une femele
                    # conditions= aucun partenaire en ce moment pour cette femele et la priorite de comportement est la reproduction
                    if len(self.attributes["partenaire"]) == 0 and self.attributes["prioriteComportement"] == 4:
                        # isReadyForFecondation(i)  pour que la femele respecte les diverses conditions pour la fecondation et ( le male est monogame ou le male fait partie du groupe de polygame)
                        if(type(i)==type(self) and (len(i.attributes["partenaire"]) == 0 or type(i) in self.parent.listePolygamie) and self.isReadyForFecondation(i)  ):
                            self.attributes["enVoieDeReproduction"]=1 #trigger le mode qu il doit se diriger pour la fecondation
                            i.attributes["enVoieDeReproduction"]=1 #trigger le mode qu il doit se diriger pour la fecondation
                            i.attributes["prioriteComportement"] = 4
                            self.attributes["partenaire"].append(i)
                            i.attributes["partenaire"].append(self)  # polygamie possible pour l homme
                            i.attributes["cibleX"] = self.attributes["posX"] # reference vers l objet , donc toujours liee
                            i.attributes["cibleY"] = self.attributes["posY"] # reference vers l objet , donc toujours liee

        self.updateChampvision(self.parent.animauxListe,instanceParentAnimalCall)
        self.updateChampvision(self.parent.vegetauxListe,instanceParentAnimalCall)
        self.updateChampvision(self.parent.habitationList,instanceParentAnimalCall)
        comportementsSelonChampVision() #nested method

    def verifierLaMort(self):
        if self.ageActuelleHours() > self.attributes["esperenceVie"] or self.attributes["vie"] == 0:
            self.parent.environnement[self.attributes["posY"]][self.attributes["posX"]][1] = None
            self.parent.animauxListe.remove(self)

    def vitesseDeFuite(self):
        if self.attributes["prioriteComportement"] == 0:
            if self.attributes["enFuite"] == True:
                pass
            elif self.attributes["enFuite"] == False:
                temp = self.attributes["delaiDeDep"]
                self.delaiDeDep = self.attributes["delaiDeFuite"]
                self.delaiDeFuite = self.delaiDeDep
                self.attributes["enFuite"] = True

    def days_hours_minutes(self, td):
        # retourne un tableau , [0] pour days, [1] pour hours et [2] pour minutes
        return td.days, td.days * 24 +td.seconds//3600 , (td.seconds %3600) //60
    def verifierLaSoif(self):
        """ Cette fonction verifie si il a depasse le nbr de jours sans boire [0] pour jours"""
        if(self.days_hours_minutes(self.parent.temps-self.attributes["last_drink"])[0] > self.attributes["desydratation"]):
            # signal trigger la mort dans verifier Mort
            self.attributes["vie"] = 0
        elif(self.attributes["litresEauBu"] < self.attributes["litresEauAverage"]):
            # missing function to go drink on lake
            self.attributes["prioriteComportement"] = 3

    def croissance(self):
        """Cette fonction determine la croissance du Lapin lors des premiers jours de vie"""
        # a chaque  behavior cette fonction est appellee
        ageHours = self.ageActuelleHours()
        if(ageHours < self.attributes["ageMaturiteCroissancePoids"] ):  # 90 jours , 2160 heures
            self.attributes["poids"] += self.attributes["croissancePoid"] #croissance du poids
        if(ageHours < self.attributes["ageMaturiteCroissanceVision"]):  # 240= 10 jours
            # sa vision grandit pendant sa periode de Lapereau , a la naissance ils sont les yeux fermes
            #lapin a une vision de 2  a sa maturite
            # 2/240heures
            self.attributes["vision"] += self.attributes["croissanceVision"] # a chaque iteration du jeu, son champs de vision grandit
            # ils font 80% du poids des adultes à 3 mois ( soit 1.2kg(1.5*0.8))
            # Ils ouvrent les yeux vers 10-12 jours.

        #lorsqu'on met le gestionnaire de temps (minutes/seconde) elevee , ex: 20jours par secondes, il rentrera 1 fois seulement dans les conditions precedentes,
        # le else permet de mettre la vision et le poids directement a des attributs adultes si le laps de temps est enorme
        else:
            self.attributes["vision"]=2
            self.attributes["poids"]=1.2





    def horlogebiologique(self):
        """Cette fonction determine si le lapin est dans ses intervalles d activites, un lapin est actif durant le matin et durant la soiree"""
        """Cette fonction s occupe  du cycle du sommeil """
        tempsActuelleGameEnHours = (self.parent.temps).hour
        count = 0

        for intervallesActivite in self.attributes["horlogeBio"]:
            count += 1

            # si le temps du jeu est dans ses intervalles d activites est qu il etait en train de dormir

            if(self.attributes["state"] == "awake" and tempsActuelleGameEnHours in range(intervallesActivite[0], intervallesActivite[1]+1)):
                break
            if(self.attributes["state"] == "sleep" and tempsActuelleGameEnHours not in range(intervallesActivite[0], intervallesActivite[1]+1) and count == 2):
                break
            # il dort est cest le moment de son activite
            if self.attributes["state"] == "sleep" and tempsActuelleGameEnHours in range(intervallesActivite[0], intervallesActivite[1]+1):
                self.attributes["state"] = "awake"  # il se reveille
                # il faut noter l heure de son reveil
                self.attributes["last_sleep"] = self.parent.temps
                self.attributes["nivSomeil"] = 0  # il a dormi

                break
            # si il est reveille et que le temps du jeu nest pas dans ses differentes  intervalles d activite, donc il est l heure de dormir pour lui
            if(self.attributes["state"] == "awake" and tempsActuelleGameEnHours not in range(intervallesActivite[0], intervallesActivite[1]+1) and count == 2):
                # on verifie s'il a une habitation
                if len(self.attributes["habitation"]) != 0:
                    # s'il est a son habitation, on dort
                    self.attributes["cibleX"] = self.attributes["habitation"][0].attributes["posX"]
                    self.attributes["cibleY"] = self.attributes["habitation"][0].attributes["posY"]
                    if self.attributes["posX"] == self.attributes["habitation"][0].attributes["posX"] and self.attributes["posY"] == self.attributes["habitation"][0].attributes["posY"]:
                        self.attributes["dansHabit"] = True
                        self.attributes["state"] = "sleep"
                # si on a pas d'habitation, on dort quand meme mais l'animal est vulnerable
                else:
                    self.attributes["state"] = "sleep"

    def determinerLaPrioriteDeComportement(self):
        """Cette fonction determine si le comportement du Lapin"""
        """
        L’activité du lapin est matinale, crépusculaire et nocturne.
        La nuit, l’activité est entrecoupée de petits épisodes de repos en gîte ou en terrier.
        40 à 60% du temps est consacré à l’alimentation, 20% aux relations sociales et le reste à la toilette et au repos
        """
        # 0=danger(fuire) 1=dodo  2=manger  3=boire 4=reproduction 5=deplacementLibrement
        # Importance de mettre en ordre les conditions!!!!
        if(self.attributes["state"] == "sleep"):
            self.attributes["prioriteComportement"] = 1
        elif self.attributes["enemySeen"]is True:
            self.attributes["prioriteComportement"] = 0
        # METHODE def verifierLaFaim SOCCUPE DE LA FAIM
        # METHODE def verifierLasoif SOCCUPE DE LA soif

    def countPredateurs(self):
        count=0
        if(len(self.attributes["caracteristiqueBiome"][1]) >0 ): #il possede des predateurs
            for animal in self.parent.animauxListe:
                if(animal.__class__ in self.attributes["caracteristiqueBiome"][1]): #animal est un predateur
                    count+=1

        return count

    def countPropreEspece(self):
        count=0
        for animal in self.parent.animauxListe:
             if(animal.__class__ == self.__class__):
                count+=1
        return count
    def projectionPopulation(self,projectionCreationAnimale):
        difficulteProbabilite=0 #difficulte permet d ajuster la probabibilite afin de suivre la courbe d approximation
        if(self.countPropreEspece()>int(projectionCreationAnimale)):#plus d espece que la projection , alors la probabilite se retrecit
            difficulteProbabilite+=85
        elif(self.countPropreEspece()<int(projectionCreationAnimale)) :
            difficulteProbabilite=-25
        for i in range(int(projectionCreationAnimale)):
            randX=random.randrange(self.parent.dimensionsTerrain - 1)
            randY=random.randrange(self.parent.dimensionsTerrain - 1)
            while(self.parent.environnement[randY][randX][0] <=  self.parent.nivEau):
                randX=random.randrange(self.parent.dimensionsTerrain - 1)
                randY=random.randrange(self.parent.dimensionsTerrain - 1)

            if(self.countPropreEspece() > self.countPredateurs()):
                resultatProbabilite=random.randint(0,50+difficulteProbabilite)
            else:
                resultatProbabilite=random.randint(0,100+difficulteProbabilite)
                
            if(resultatProbabilite<1):

                if(self.__class__.__name__=="Lapin"):
                        enfant = Lapin(self.parent, randX,randY, random.randrange(2))
                elif(self.__class__.__name__=="Loup"):
                        enfant = Loup(self.parent,  randX,randY, random.randrange(2))

                elif(self.__class__.__name__=="Ours"):
                        enfant = Ours(self.parent, randX,randY,random.randrange(2))
                elif(self.__class__.__name__=="Lievre"):
                        enfant = Lievre(self.parent, randX,randY,random.randrange(2))
                elif(self.__class__.__name__=="Bison"):
                        enfant = Lievre(self.parent, randX,randY,random.randrange(2))

                    # placer enfant dans self.environnement...!!!!!!!!!!!
                self.parent.animauxListe.append(enfant)



# -------------------------------------------------------------------------------------------------------------------------


class Lapin(Animal):
    # newX et newY est la position de la mere quand il y a naissance
    def __init__(self, parent, newX, newY, sexe):
        super().__init__(parent)
        # les attributs sont deja herites du parent, ici je fais un update
        esperanceHours = 17520+random.randrange(0, 8760)
        self.attributes.update(
            {
                "posX": newX,
                "posY": newY,
                "age": self.parent.temps,
                # A CHANGER car Le lapin peut vivre au maximum 9 ans
                # 2 a 3 ans Le lapin peut vivre au maximum 9 ans mais, à l'état sauvage, sa longévité ne dépasse guère les 2 ans car le lapin doit faire face à grand nombre de prédateurs
                "esperenceVie": esperanceHours,
                "nivSoif": 0,
                "nivFaim": random.randrange(0, 50),
                "vision": 3,  # Ils ouvrent les yeux vers 10-12 jours.
                "taille": random.randrange(34, 50),
                "force": 0,
                "sante": True,
                "terrestre": True,
                "temperature": None,  # to complete
                "vitesse": 1,
                # 0=danger(fuire) 1=dodo  2=manger  3=boire 4=reproduction 5=deplacementLibrement
                "prioriteComportement": 5,
                "compteurDeDelai": 0,
                "delaiDeDep": 4,
                "delaiDeFuite": 2,
                # Il délimite son territoire par son urine et par ses crottes.
                "excrement": [],
                # Un lapin adulte mange entre 200 à 500 grammes de plantes par jour.
                "valeurNutritive": 0,
                # de 1.1 à 2.1 kg (moyenne 1.5 kg)
                "poids": 0.6,  # poids a la naissance
                # femele=0 et male=1 Le lapin mâle est polygame
                "sexe": sexe,
                "readyPourReproduction": False,  # to add to class animal
                # reproduction a lieu février à août
                # La maturité sexuelle des femelle commence à 3,5 mois et à 4 mois chez les mâles
                # en d autres mots maturite Sexuelle (male 4mois donc 2880 heures)
                "ageDeFecondation": 1,
                # [ PartnerClassForReproduction , [listepredateur], [listeBouffe] ]
                "caracteristiqueBiome": [Lapin, [], [vegetaux.Ble, vegetaux.Laitue,vegetaux.Sapin,vegetaux.Cerisier],[habitation.Terrier]], #lOUP1
                "horlogeBio": [[0, 3], [6, 10]],
                "state": ["sleep", "hibernation", "awake"],
                "last_sleep": self.parent.temps,
                "last_dinner": self.parent.temps,
                "last_drink": self.parent.temps,
                "avgEnActivite": 4,  # temps moyen que le lapin reste en activite , il devient fatigue
                "tempsAbstentionBouffe": 4,  # apres 4 h il a faim
                "tempsAbstentionBouffeMax": 96,  # apres 72h cest impossible qu il survive
                "litresEauBu": 0,
                # Le lapin boit entre 50 et 150 ml/jour.
                "litresEauAverage": random.randrange(50, 150),
                "desydratation": 3,  # 3 jours maximum sans eau sinon la mort
                "ageMaturiteCroissancePoids":2160,
                "ageMaturiteCroissanceVision":240,
                "croissancePoid":0.00027,
                "croissanceVision":random.uniform(0.0020,0.0060)
                # pour plus d infos http://www.jaitoutcompris.com/animaux/le-lapin-de-garenne-58.php
                # http://ecologie.nature.free.fr/pages/mammiferes/lapin_de_garenne.htm
            })
        if(sexe == 0):  # femelle =rajouts d attributs
            self.attributes["tempsBesoinsGest"]=720
            self.attributes["tempsEntre2Portee"]= 30  # L'intervalle minimum entre 2 portées est de 30 jours
            # Les femelles mettent au monde chaque année de 15 à 25 petits en 3 à 5 portées.
            self.attributes["nbrEnfantsPossible"]= random.randrange(3, 12)
            self.attributes["portee"]= random.randrange(3, 6)
            self.attributes["nbrAccouchementFaits"]= 0
            # en d autres mots maturite Sexuelle (femelle 3.5mois donc 2520 heures)
            self.attributes["ageDeFecondation"]= 1
            self.attributes["last_accouchement"]= self.parent.temps

            # 35 jours pour donner naissance

            self.attributes["gestation"] = [self.attributes["tempsActuelGest"], self.attributes["tempsBesoinsGest"],self.attributes["partenaire"], self.attributes["tempsEntre2Portee"]]



        self.genererCibleDepart()
        self.attributes["state"] = "awake"  # lapin commence en etant reveille

    def behavior(self):

        positionActuelle = (self.attributes["posX"], self.attributes["posY"])
        positionCible = (self.attributes["cibleX"], self.attributes["cibleY"])
        if(positionActuelle == positionCible):  # arrive au point de destination
            self.nouvelleDestinationPreferences()


            if self.attributes["compteurDeDelai"] >= self.attributes["delaiDeDep"]:
                self.deplacer()
                self.attributes["compteurDeDelai"] = 0

        if self.attributes["compteurDeDelai"] >= self.attributes["delaiDeDep"]:
            self.horlogebiologique()  # verfie toujours les heures d activite

            if(self.parent.multiplicateurTemps>60): #lorsque la simulation est sur du long terme
                projectionPopulation=0.5*math.sqrt((self.parent.temps-dt.datetime(1,1,1)).days) #f(x)=0.5 log 2 (x), courbe d appproximation
                self.projectionPopulation(projectionPopulation)
            # si il est dans ses heures d activite, alors on verifie tout
            if  self.attributes["state"] == "awake":
                """
                if(self.ageActuelleHours()<= self.attributes["ageMaturiteCroissanceVision"]):
                    self.croissance()
                else:
                """
                self.croissance()
                self.verifierAlentour1(self)
                #start = time.time()
                self.determinerLaPrioriteDeComportement()

                if( self.attributes["enemySeen"]==False):
                    self.verifierLaFaim()
                    #self.verifierLaSoif() a faire
                    self.verifierAccouplement() #
                    self.verifierLaNaissance()

                else:
                    self.vitesseDeFuite()

                self.deplacer()
                self.verifierLaMort()
            self.attributes["compteurDeDelai"] = 0
        # on ne garde pas le champ de vision puisquon verifie chaque fois
        self.attributes["champVision"].clear()
        self.attributes["proie"].clear()
        self.attributes["allySeen"] = False
        self.attributes["enemySeen"] = False
        self.attributes["compteurDeDelai"] += 1

class Lievre(Animal):
    # newX et newY est la position de la mere quand il y a naissance
    def __init__(self, parent, newX, newY, sexe):
        super().__init__(parent)
        # les attributs sont deja herites du parent, ici je fais un update
        esperanceHours = 21900+random.randrange(0, 21900)
        self.attributes.update(
            {
                "posX": newX,
                "posY": newY,
                "age": self.parent.temps,
                # A CHANGER car Le lapin peut vivre au maximum 9 ans
                # 2 a 3 ans Le lapin peut vivre au maximum 9 ans mais, à l'état sauvage, sa longévité ne dépasse guère les 2 ans car le lapin doit faire face à grand nombre de prédateurs
                "esperenceVie": esperanceHours,
                "nivSoif": 0,
                "nivFaim": random.randrange(0, 50),
                "vision": 3,  # Ils ouvrent les yeux vers 10-12 jours.
                "taille": random.randrange(34, 50),
                "force": 0,
                "sante": True,
                "terrestre": True,
                "temperature": None,  # to complete
                "vitesse": 1,
                # 0=danger(fuire) 1=dodo  2=manger  3=boire 4=reproduction 5=deplacementLibrement
                "prioriteComportement": 5,
                "compteurDeDelai": 0,
                "delaiDeDep": 4,
                "delaiDeFuite": 2,
                # Il délimite son territoire par son urine et par ses crottes.
                "excrement": [],
                # Un lapin adulte mange entre 200 à 500 grammes de plantes par jour.
                "valeurNutritive": 0,
                # de 1.1 à 2.1 kg (moyenne 1.5 kg)
                "poids": 1.5,  # poids a la naissance
                # femele=0 et male=1 Le lapin mâle est polygame
                "sexe": sexe,
                "readyPourReproduction": False,  # to add to class animal
                # reproduction a lieu février à août
                # La maturité sexuelle des femelle commence à 3,5 mois et à 4 mois chez les mâles
                # en d autres mots maturite Sexuelle (male 4mois donc 2880 heures)
                "ageDeFecondation": 1,
                # [ PartnerClassForReproduction , [listepredateur], [listeBouffe] ]
                "caracteristiqueBiome": [Lievre, [], [vegetaux.Ble, vegetaux.Laitue, vegetaux.Cerisier,vegetaux.Sapin],[habitation.Terrier]], #lOUP1
                "horlogeBio": [[0, 7], [17, 23]],
                "state": ["sleep", "hibernation", "awake"],
                "last_sleep": self.parent.temps,
                "last_dinner": self.parent.temps,
                "last_drink": self.parent.temps,
                "avgEnActivite": 4,  # temps moyen que le lapin reste en activite , il devient fatigue
                "tempsAbstentionBouffe": 4,  # apres 4 h il a faim
                "tempsAbstentionBouffeMax": 96,  # apres 72h cest impossible qu il survive
                "litresEauBu": 0,
                # Le lapin boit entre 50 et 150 ml/jour.
                "litresEauAverage": random.randrange(50, 150),
                "desydratation": 3,  # 3 jours maximum sans eau sinon la mort
                "ageMaturiteCroissancePoids":4320,
                "ageMaturiteCroissanceVision":240,
                "croissancePoid":0.00027,
                "croissanceVision":random.uniform(0.0020,0.0060)
                # pour plus d infos http://www.jaitoutcompris.com/animaux/le-lapin-de-garenne-58.php
                # http://ecologie.nature.free.fr/pages/mammiferes/lapin_de_garenne.htm
            })
        if(sexe == 0):  # femelle =rajouts d attributs
            self.attributes["tempsBesoinsGest"]=900
            self.attributes["tempsEntre2Portee"]= 30  # L'intervalle minimum entre 2 portées est de 30 jours
            # Les femelles mettent au monde chaque année de 15 à 25 petits en 3 à 5 portées.
            self.attributes["nbrEnfantsPossible"]= random.randrange(3, 12)
            self.attributes["portee"]= random.randrange(3, 6)
            self.attributes["nbrAccouchementFaits"]= 0
            # en d autres mots maturite Sexuelle (femelle 3.5mois donc 2520 heures)
            self.attributes["ageDeFecondation"]= 1
            self.attributes["last_accouchement"]= self.parent.temps

            # 35 jours pour donner naissance

            self.attributes["gestation"] = [self.attributes["tempsActuelGest"], self.attributes["tempsBesoinsGest"],self.attributes["partenaire"], self.attributes["tempsEntre2Portee"]]



        self.genererCibleDepart()
        self.attributes["state"] = "awake"  # lapin commence en etant reveille

    def behavior(self):

        positionActuelle = (self.attributes["posX"], self.attributes["posY"])
        positionCible = (self.attributes["cibleX"], self.attributes["cibleY"])
        if(positionActuelle == positionCible):  # arrive au point de destination
            self.nouvelleDestinationPreferences()

        if self.attributes["compteurDeDelai"] >= self.attributes["delaiDeDep"]:
            self.horlogebiologique()  # verfie toujours les heures d activite
            if(self.parent.multiplicateurTemps>60): #lorsque la simulation est sur du long terme
                projectionPopulation=0.5*math.sqrt((self.parent.temps-dt.datetime(1,1,1)).days) #f(x)=0.5 log 2 (x), courbe d appproximation
                self.projectionPopulation(projectionPopulation)

            # si il est dans ses heures d activite, alors on verifie tout
            if  self.attributes["state"] == "awake":
                """
                if(self.ageActuelleHours()<= self.attributes["ageMaturiteCroissanceVision"]):
                    self.croissance()
                else:
                """
                self.croissance()
                self.verifierAlentour1(self)
                #start = time.time()
                self.determinerLaPrioriteDeComportement()

                if( self.attributes["enemySeen"]==False):
                    self.verifierLaFaim()
                    #self.verifierLaSoif() a faire
                    self.verifierAccouplement() #
                    self.verifierLaNaissance()

                else:
                    self.vitesseDeFuite()

                self.deplacer()
                self.verifierLaMort()
            self.attributes["compteurDeDelai"] = 0
            
        # on ne garde pas le champ de vision puisquon verifie chaque fois
        self.attributes["champVision"].clear()
        self.attributes["proie"].clear()
        self.attributes["allySeen"] = False
        self.attributes["enemySeen"] = False
        self.attributes["compteurDeDelai"] += 1



class Loup(Animal):
    def __init__(self,parent,newX,newY,sexe):
        super().__init__(parent)
        esperanceHours = 86400+random.randrange(0, 52000)
        self.attributes.update({
            "wolfPack":None,
            "posX":newX,
            "posY":newY,
            "cibleX":None,
            "cibleY":None,
            "age": self.parent.temps,
            "esperenceVie": esperanceHours,
            "nivSoif":0,
             "sexe": sexe,
            "vision":1, #la vision cest le range de vue, comme la map est petite il faut le limiter
            "taille":0,
            "sante":True,
            "terrestre":False,
            "temperature":None,
            "vitesse":1,
            "readyPourReproduction":True,
            "joursDepuisLastReproduction": 0,
            "prioriteComportement":5,
            "ageDeFecondation":2520, #15840
            "compteurDeDelai":0,
            "delaiDeDep":6,
            "caracteristiqueBiome": [Loup, [], [Lapin,Lievre],[]],
            "delaiDeFuite":4, #delai de chasse va utiliser aussi cette var, delaiDeFuite est en fait sa vitesse quand il cour

    # [ PartnerClassForReproduction , [listepredateur], [listeBouffe] ]
            "poids":20, #20kg
            "horlogeBio": [[20,23], [0,8]], #de 20h a 23h et de 0h a 8h, le loup est un animal nocturne
            "state": ["sleep", "hibernation", "awake"],
            "last_sleep": self.parent.temps,
            "last_dinner": self.parent.temps,
            "last_drink": self.parent.temps,
            "avgEnActivite": 4,  # temps moyen que le lapin reste en activite , il devient fatigue
            "tempsAbstentionBouffe": 4,  # apres 4 h il a faim
            "tempsAbstentionBouffeMax": 336,  # apres 72h cest impossible qu il survive
            "litresEauBu": 0,
            # Le lapin boit entre 50 et 150 ml/jour.
            "litresEauAverage": random.randrange(50, 150),
            "desydratation": 3,  # 3 jours maximum sans eau sinon la mort
            "ageMaturiteCroissancePoids":25940,
            "ageMaturiteCroissanceVision":240,
            "croissancePoid":0.0019,
            "croissanceVision":random.uniform(0.0020,0.0060)
                # pour plus d infos http://www.jaitoutcompris.com/animaux/le-lapin-de-garenne-58.php
                # http://ecologie.nature.free.fr/pages/mammiferes/lapin_de_garenne.htm
            })
        if(sexe == 0):  # femelle =rajouts d attributs
            self.attributes["tempsBesoinsGest"]=720
            self.attributes["tempsEntre2Portee"]= 30  # L'intervalle minimum entre 2 portées est de 30 jours
            # Les femelles mettent au monde chaque année de 15 à 25 petits en 3 à 5 portées.
            self.attributes["nbrEnfantsPossible"]= random.randrange(3, 12)
            self.attributes["portee"]= random.randrange(3, 6)
            self.attributes["nbrAccouchementFaits"]= 0
            # en d autres mots maturite Sexuelle (femelle 3.5mois donc 2520 heures)
            self.attributes["ageDeFecondation"]= 2520
            self.attributes["gestation"] = [self.attributes["tempsActuelGest"], self.attributes["tempsBesoinsGest"],self.attributes["partenaire"], self.attributes["tempsEntre2Portee"]]
            self.attributes["last_accouchement"]= self.parent.temps

            # 35 jours pour donner naissance

        self.genererCibleDepart()
        self.attributes["state"] = "awake"  # lapin commence en etant reveille

    def behavior(self):

        positionActuelle = (self.attributes["posX"], self.attributes["posY"])
        positionCible = (self.attributes["cibleX"], self.attributes["cibleY"])
        if(positionActuelle == positionCible):  # arrive au point de destination
            self.nouvelleDestinationPreferences()

        if self.attributes["compteurDeDelai"] >= self.attributes["delaiDeDep"]:
            self.horlogebiologique()  # verfie toujours les heures d activite
            if(self.parent.multiplicateurTemps>60): #lorsque la simulation est sur du long terme
                projectionPopulation=0.5*math.sqrt((self.parent.temps-dt.datetime(1,1,1)).days) #f(x)=0.5 log 2 (x), courbe d appproximation
                self.projectionPopulation(projectionPopulation)

            # si il est dans ses heures d activite, alors on verifie tout
            if  self.attributes["state"] == "awake":
                """
                if(self.ageActuelleHours()<= self.attributes["ageMaturiteCroissanceVision"]):
                    self.croissance()
                else:
                """
                self.croissance()
                self.verifierAlentour1(self)
                #start = time.time()
                self.determinerLaPrioriteDeComportement()


                if( self.attributes["enemySeen"]==False):
                    self.verifierLaFaim()
                    #self.verifierLaSoif() a faire
                    self.verifierAccouplement() #
                    self.verifierLaNaissance()
                else:
                    self.vitesseDeFuite()

                self.deplacer()
                self.verifierLaMort()
                
            self.attributes["compteurDeDelai"] = 0
            
        # on ne garde pas le champ de vision puisquon verifie chaque fois
        self.attributes["champVision"].clear()
        self.attributes["proie"].clear()
        self.attributes["allySeen"] = False
        self.attributes["enemySeen"] = False
        self.attributes["compteurDeDelai"] += 1



"""
    http://www.oiseau-libre.net/Animaux/Animaux-sauvages/Grands-predateurs/Ours.html
    l'ours est un plus ou moins nocture (17h a 3h)animal nocturne, 1 a 3 enfants par reproduction, interval entre deux reproduction =220 jours
"""
class Ours(Animal):
    def __init__(self,parent,newX,newY,sexe):
        super().__init__(parent)
        esperanceHours = 17520+random.randrange(0, 8760)
        #150000+random.randrange(0, 150000)
        self.attributes.update({
            "posX":newX,
            "posY":newY,
            "cibleX":None,
            "cibleY":None,
            "age": self.parent.temps,
            "esperenceVie": esperanceHours,
            "nivSoif":0,
            "vision":2,
            "taille":0,
            "sante":True,
            "terrestre":False,
            "temperature":None,
            "vitesse":1,
            "sexe": sexe,
            "readyPourReproduction":True,
            "joursDepuisLastReproduction": 0,
            "prioriteComportement":0,
            "ageDeFecondation":2520, #150000
            "compteurDeDelai":0,
            "delaiDeDep":8,
            "poids":10, #10 kg
            "caracteristiqueBiome": [Ours, [Loup], [vegetaux.Cerisier],[habitation.Caverne]],
            "delaiDeFuite":4,  #delai de chasse va utiliser aussi cette var, delaiDeFuite est en fait sa vitesse quand il cour
            "horlogeBio": [[17, 23], [0, 3]],
            "state": ["sleep", "hibernation", "awake"],
            "last_sleep": self.parent.temps,
            "last_dinner": self.parent.temps,
            "last_drink": self.parent.temps,
            "avgEnActivite": 4,  # temps moyen que le lapin reste en activite , il devient fatigue
            "tempsAbstentionBouffe": 4,  # apres 4 h il a faim
            "tempsAbstentionBouffeMax": 2400,  # apres 72h cest impossible qu il survive
            "litresEauBu": 0,
            # Le lapin boit entre 50 et 150 ml/jour.
            "litresEauAverage": random.randrange(50, 150),
            "desydratation": 3,  # 3 jours maximum sans eau sinon la mort
            "ageMaturiteCroissancePoids":34560,
            "ageMaturiteCroissanceVision":240,
            "croissancePoid":0.007,
            "croissanceVision": random.uniform(0.0020,0.0060)
                # pour plus d infos http://www.jaitoutcompris.com/animaux/le-lapin-de-garenne-58.php
                # http://ecologie.nature.free.fr/pages/mammiferes/lapin_de_garenne.htm
            })
        if(sexe == 0):  # femelle =rajouts d attributs
            self.attributes["tempsBesoinsGest"]=720 #30j
            self.attributes["tempsEntre2Portee"]= 30  # L'intervalle minimum entre 2 portées est de 30 jours
            # Les femelles mettent au monde chaque année de 15 à 25 petits en 3 à 5 portées.
            self.attributes["nbrEnfantsPossible"]= random.randrange(3, 12)
            self.attributes["portee"]= random.randrange(3, 6)
            self.attributes["nbrAccouchementFaits"]= 0
            # en d autres mots maturite Sexuelle (femelle 3.5mois donc 2520 heures)
            self.attributes["ageDeFecondation"]= 2520
            self.attributes["last_accouchement"]= self.parent.temps
            self.attributes["gestation"] = [self.attributes["tempsActuelGest"], self.attributes["tempsBesoinsGest"],self.attributes["partenaire"], self.attributes["tempsEntre2Portee"]]


            # 35 jours pour donner naissance


        self.genererCibleDepart()
        self.attributes["state"] = "awake"  # lapin commence en etant reveille

    def behavior(self):

        positionActuelle = (self.attributes["posX"], self.attributes["posY"])
        positionCible = (self.attributes["cibleX"], self.attributes["cibleY"])
        if(positionActuelle == positionCible):  # arrive au point de destination
            self.nouvelleDestinationPreferences()

        if self.attributes["compteurDeDelai"] >= self.attributes["delaiDeDep"]:
            self.horlogebiologique()  # verfie toujours les heures d activite
            if(self.parent.multiplicateurTemps>60): #lorsque la simulation est sur du long terme
                projectionPopulation=0.5*math.sqrt((self.parent.temps-dt.datetime(1,1,1)).days) #f(x)=0.5 log 2 (x), courbe d appproximation
                self.projectionPopulation(projectionPopulation)

            # si il est dans ses heures d activite, alors on verifie tout
            if  self.attributes["state"] == "awake":
                """
                if(self.ageActuelleHours()<= self.attributes["ageMaturiteCroissanceVision"]):
                    self.croissance()
                else:
                """
                self.croissance()
                self.verifierAlentour1(self)
                #start = time.time()
                self.determinerLaPrioriteDeComportement()

                if( self.attributes["enemySeen"]==False):
                    self.verifierLaFaim()
                    #self.verifierLaSoif() a faire
                    self.verifierAccouplement() #
                    self.verifierLaNaissance()

                else:
                    self.vitesseDeFuite()

                self.deplacer()
                self.verifierLaMort()
                
            self.attributes["compteurDeDelai"] = 0
            
        # on ne garde pas le champ de vision puisquon verifie chaque fois
        self.attributes["champVision"].clear()
        self.attributes["proie"].clear()
        self.attributes["allySeen"] = False
        self.attributes["enemySeen"] = False
        self.attributes["compteurDeDelai"] += 1

class Bison(Animal):
    def __init__(self,parent,newX,newY,sexe):
        super().__init__(parent)
        esperanceHours = 150000+random.randrange(0, 175200)
        self.attributes.update({
            "posX":newX,
            "posY":newY,
            "cibleX":None,
            "cibleY":None,
            "age": self.parent.temps,
            "esperenceVie": esperanceHours,
            "nivSoif":0,
             "sexe": sexe,
            "vision":1, #la vision cest le range de vue, comme la map est petite il faut le limiter
            "taille":0,
            "sante":True,
            "terrestre":False,
            "temperature":None,
            "vitesse":1,
            "readyPourReproduction":True,
            "joursDepuisLastReproduction": 0,
            "prioriteComportement":5,
            "ageDeFecondation":2520, #15840
            "compteurDeDelai":0,
            "delaiDeDep":6,
            "caracteristiqueBiome": [Bison, [Loup], [vegetaux.Ble],[]],
            "delaiDeFuite":4, #delai de chasse va utiliser aussi cette var, delaiDeFuite est en fait sa vitesse quand il cour

    # [ PartnerClassForReproduction , [listepredateur], [listeBouffe] ]
            "poids":20, #20kg
            "horlogeBio": [[9,15], [16,19]], #de 20h a 23h et de 0h a 8h, le loup est un animal nocturne
            "state": ["sleep", "hibernation", "awake"],
            "last_sleep": self.parent.temps,
            "last_dinner": self.parent.temps,
            "last_drink": self.parent.temps,
            "avgEnActivite": 4,  # temps moyen que le lapin reste en activite , il devient fatigue
            "tempsAbstentionBouffe": 4,  # apres 4 h il a faim
            "tempsAbstentionBouffeMax": 336,  # apres 72h cest impossible qu il survive
            "litresEauBu": 0,
            # Le lapin boit entre 50 et 150 ml/jour.
            "litresEauAverage": random.randrange(50, 150),
            "desydratation": 3,  # 3 jours maximum sans eau sinon la mort
            "ageMaturiteCroissancePoids":25940,
            "ageMaturiteCroissanceVision":240,
            "croissancePoid":0.0019,
            "croissanceVision":random.uniform(0.0020,0.0060)
                # pour plus d infos http://www.jaitoutcompris.com/animaux/le-lapin-de-garenne-58.php
                # http://ecologie.nature.free.fr/pages/mammiferes/lapin_de_garenne.htm
            })
        if(sexe == 0):  # femelle =rajouts d attributs
            self.attributes["tempsBesoinsGest"]=720
            self.attributes["tempsEntre2Portee"]= 30  # L'intervalle minimum entre 2 portées est de 30 jours
            # Les femelles mettent au monde chaque année de 15 à 25 petits en 3 à 5 portées.
            self.attributes["nbrEnfantsPossible"]= random.randrange(3, 12)
            self.attributes["portee"]= random.randrange(3, 6)
            self.attributes["nbrAccouchementFaits"]= 0
            # en d autres mots maturite Sexuelle (femelle 3.5mois donc 2520 heures)
            self.attributes["ageDeFecondation"]= 2520
            self.attributes["gestation"] = [self.attributes["tempsActuelGest"], self.attributes["tempsBesoinsGest"],self.attributes["partenaire"], self.attributes["tempsEntre2Portee"]]
            self.attributes["last_accouchement"]= self.parent.temps

            # 35 jours pour donner naissance
        self.genererCibleDepart()
        self.attributes["state"] = "awake"  # lapin commence en etant reveille

    def behavior(self):

        positionActuelle = (self.attributes["posX"], self.attributes["posY"])
        positionCible = (self.attributes["cibleX"], self.attributes["cibleY"])
        if(positionActuelle == positionCible):  # arrive au point de destination
            self.nouvelleDestinationPreferences()

        if self.attributes["compteurDeDelai"] >= self.attributes["delaiDeDep"]:
            self.horlogebiologique()  # verfie toujours les heures d activite
            if(self.parent.multiplicateurTemps>60): #lorsque la simulation est sur du long terme
                projectionPopulation=0.5*math.sqrt((self.parent.temps-dt.datetime(1,1,1)).days) #f(x)=0.5 log 2 (x), courbe d appproximation
                self.projectionPopulation(projectionPopulation)

            # si il est dans ses heures d activite, alors on verifie tout
            if  self.attributes["state"] == "awake":
                """
                if(self.ageActuelleHours()<= self.attributes["ageMaturiteCroissanceVision"]):
                    self.croissance()
                else:
                """
                self.croissance()
                self.verifierAlentour1(self)
                #start = time.time()
                self.determinerLaPrioriteDeComportement()


                if( self.attributes["enemySeen"]==False):
                    self.verifierLaFaim()
                    #self.verifierLaSoif() a faire
                    self.verifierAccouplement() #
                    self.verifierLaNaissance()
                else:
                    self.vitesseDeFuite()

                self.deplacer()
                self.verifierLaMort()
                
            self.attributes["compteurDeDelai"] = 0
            
        # on ne garde pas le champ de vision puisquon verifie chaque fois
        self.attributes["champVision"].clear()
        self.attributes["proie"].clear()
        self.attributes["allySeen"] = False
        self.attributes["enemySeen"] = False
        self.attributes["compteurDeDelai"] += 1


if __name__ == '__main__':
    print("Dans Animaux")
