import random

class Plante():
    def __init__ (self,parent,posX,posY,dict,dateNaissance):
        self.parent=parent
        self.dict=dict
        self.attributes={
            "posX":posX,
            "posY":posY,
            "age":None,
            "naissance":dateNaissance,
            "valCritique":40,
            "esperanceVie":None, #heures -> 3 mois
            "nivEau":50,
            "nivSoleil":50,
            "nutriments":50, #max 100
            "consommation":random.randrange(3,10),
            "taille":random.randrange(3,6),
            "tailleLimite" :None,
            "sante":True,
            "terrestre":False,
            "aquatique":False,
            "temperatureIdeale":None, #temperature [ideale,min,max]
            "temperatureMin":None,
            "temperatureMax":None,
            "mort":False,
            "valeurMax":100,
            "semence":0,
            "vie":100, #la vie de la plante losrqu'elle va se faire manger
            "sensibiliteTemp":None,
            "periodeDeLAnnee":False,
            "moisMontaison":None,
            "perteFeuilles":False,
            "mature":False
            }

    def tuer(self):
        self.attributes["mort"] = True
    def perteFeuilles(self):
        if self.parent.getSaison() == "hiver":
            self.attributes["perteFeuilles"] = True
        elif self.parent.getSaison() == "printemps":
            if (random.randrange(30)) == 1:     #afin qu'ils perdent pas tous leur feuilles en même temps
                self.attributes["perteFeuilles"] = False
        elif self.parent.getSaison() == "ete":
            self.attributes["perteFeuilles"] = False
        elif self.parent.getSaison() == "automne":
            if (random.randrange(30)) == 1:     #afin qu'ils perdent pas tous leur feuilles en même temps
                self.attributes["perteFeuilles"] = True


    def verifierSaison(self):
        if self.parent.temps.month == self.attributes["moisMontaison"]:
            self.attributes["periodeDeLAnnee"] = True
            self.attributes["mature"] = True
        else:
            self.attributes["periodeDeLAnnee"] = False
        self.perteFeuilles()

    def vieillir(self):
        self.attributes["age"] = (self.parent.temps-self.attributes["naissance"]).days
    def vivre(self):
        self.verifierSaison()
        if self.attributes["age"] < self.attributes["esperanceVie"] and self.attributes["vie"] > 0 and self.attributes["mort"] == False:
            self.manger()
            self.croissance()
            self.maladie()
            self.vieillir()
            if self.attributes["nivSoleil"] < 0:
                self.attributes["nivSoleil"] = 0
            if self.attributes["nivEau"] < 0:
                self.attributes["nivEau"] = 0
            if self.attributes["nutriments"] < 0:
                self.attributes["nutriments"] = 0
        else:
            self.attributes["mort"]=True

        if self.attributes["mort"]==True:
            nbSemence = 1
            if random.randrange(1000) == 5: # 1 fois sur 1000 il est possible qu'une plante dépose 2 semences a la place de 1
                nbSemence = 2
            self.attributes["semence"] += nbSemence
            self.reproduction()


    def croissance(self):
        self.attributes["nutriments"] = self.attributes["nutriments"] - self.attributes["consommation"]
        self.attributes["nivEau"] = self.attributes["nivEau"] - self.attributes["consommation"]
        self.attributes["nivSoleil"]= self.attributes["nivEau"] - self.attributes["consommation"]
        if self.attributes["nutriments"] > self.attributes["valCritique"] and self.attributes["nivSoleil"] > self.attributes["valCritique"] and self.attributes["nivEau"] > self.attributes["valCritique"] and self.attributes["sante"] == True:
            if self.attributes["taille"] < self.attributes["tailleLimite"]:
                self.attributes["taille"] += 1
        elif self.attributes["nutriments"] > 0 and self.attributes["nivSoleil"] > 0 and self.attributes["nivEau"] > 0 and self.attributes["sante"] == True:
                pass
        else:
            if self.attributes["taille"] > 0:
                self.attributes["taille"] -= 1
            else:
                self.attributes["mort"] = True

    def manger(self):

        #niveau de soleil
        if self.parent.dictBiomePlaine.get('temperature') > self.attributes["temperatureMin"] and  self.parent.dictBiomePlaine.get('temperature') < self.attributes["temperatureMax"] and self.parent.dictBiomePlaine.get('ensoleille') == True:
            if self.attributes["nivSoleil"] < self.attributes["valeurMax"]:
                if self.parent.dictBiomePlaine.get('temperature') >= self.attributes["temperatureIdeale"] + self.attributes["sensibiliteTemp"] or self.parent.dictBiomePlaine.get('temperature') >= self.attributes["temperatureIdeale"] - self.attributes["sensibiliteTemp"]:
                    self.attributes["nivSoleil"] += random.randrange(4,10)
                else:
                    self.attributes["nivSoleil"] -= random.randrange(10,25)

        if self.attributes["nivSoleil"] > self.attributes["valeurMax"]:
            self.attributes["nivSoleil"] = self.attributes["valeurMax"]

        #niveau de l'eau
        if self.parent.dictBiomePlaine.get('humiditeSol') > self.attributes["valCritique"]:
           self.attributes["nivEau"] += random.randrange(10,15)
        elif self.parent.dictBiomePlaine.get('humiditeSol') < self.attributes["valCritique"] and self.parent.dictBiomePlaine.get('humiditeSol') > 0:
            self.attributes["nivEau"] += random.randrange(2,5)
        else:
            self.attributes["nivEau"] -= random.randrange(5,15)

        if self.attributes["nivEau"] > self.attributes["valeurMax"]:
               self.attributes["nivEau"] = self.attributes["valeurMax"]


        #niveau nutriments
        if self.parent.dictBiomePlaine.get('nutrimentSol') > self.attributes["valCritique"]:
            self.attributes["nutriments"] += random.randrange(10,15)
        elif self.parent.dictBiomePlaine.get('nutrimentSol') < self.attributes["valCritique"] and self.parent.dictBiomePlaine.get('nutrimentSol') > 0:
            self.attributes["nutriments"] += random.randrange(2,5)
        else:
            self.attributes["nutriments"] -= random.randrange(5,15)

        if self.attributes["nutriments"] > self.attributes["valeurMax"]:
            self.attributes["nutriments"] = self.attributes["valeurMax"]

    def reproduction(self):
        pass

    def maladie(self):
        if random.randrange(0,10000)==1:
            self.attributes["sante"]=False
class Ble(Plante):
    def __init__ (self,parent,posX,posY,dict,temps):
        Plante.__init__ (self,parent,posX,posY,dict,temps)
        self.parent=parent
        self.dict=dict
        self.attributes={
            "posX":posX,
            "posY":posY,
            "age":0,
            "naissance":temps,
            "valCritique":40,
            "esperanceVie":random.randrange(80,105), #jours -> 3 mois
            "nivEau":80,
            "nivSoleil":80,
            "nutriments":80, #max 100
            "consommation":random.randrange(3,10),
            "taille":random.randrange(3,6),
            "tailleLimite" :20,
            "sante":True,
            "terrestre":True,
            "aquatique":False,
            "temperatureIdeale":21,
            "temperatureMin":15,
            "temperatureMax":32,
            "mort":False,
            "valeurMax":100,
            "semence":0,
            "vie":100, #la vie de la plante losrqu'elle va se faire manger
            "sensibiliteTemp":2,
            "periodeDeLAnnee":False,
            "moisMontaison": 5,        #mois de mai
            "perteFeuilles":False,
            "mature":False
            }

    def maladie(self):
        if self.parent.dictBiomePlaine.get('humiditeAir') > 60:
            if random.randrange(0,10)==1:
                self.attributes["sante"]=False
        else:
            if random.randrange(0,10000)==1:
                self.attributes["sante"]=False

    def reproduction(self):
        self.parent.genPlante(Ble, self.attributes["semence"])

class Cerisier(Plante):
    def __init__ (self,parent,posX,posY,dict,temps):
        Plante.__init__ (self,parent,posX,posY,dict,temps)
        self.dict=dict
        self.attributes={
            "posX":posX,
            "posY":posY,
            "age":0,
            "naissance":temps,
            "valCritique":40,
            "esperanceVie":random.randrange(18250,36500), #jours -> 50-100 ans
            "nivEau":100,
            "nivSoleil":100,
            "nutriments":100, #max 100
            "consommation":random.randrange(3,10),
            "taille":random.randrange(3,6),
            "tailleLimite": 500,
            "sante":True,
            "terrestre":True,
            "aquatique":False,
            "temperatureIdeale":18,
            "temperatureMin":-12,
            "temperatureMax":32,
            "mort":False,
            "valeurMax":100,
            "semence":0,
            "vie":100, #la vie de la plante losrqu'elle va se faire manger
            "sensibiliteTemp":10,
            "periodeDeLAnnee":False,
            "moisMontaison":1,       #mois de mars
            "perteFeuilles":False,
            "mature":False
            }

    def saison(self):
        pass
    def reproduction(self):
        self.parent.genPlante(Cerisier, self.attributes["semence"])

class Erable(Plante):
    def __init__ (self,parent,posX,posY,dict,temps):
        Plante.__init__ (self,parent,posX,posY,dict,temps)
        self.dict=dict
        self.attributes={
            "posX":posX,
            "posY":posY,
            "age":0,
            "naissance":temps,
            "valCritique":40,
            "esperanceVie":random.randrange(16425,21900), #jours -> 45-60 ans
            "nivEau":100,
            "nivSoleil":100,
            "nutriments":100, #max 100
            "consommation":random.randrange(3,10),
            "taille":random.randrange(3,6),
            "tailleLimite" :500,
            "sante":True,
            "terrestre":True,
            "aquatique":False,
            "temperatureIdeale":18,
            "temperatureMin":-18,
            "temperatureMax":30,
            "mort":False,
            "valeurMax":100,
            "semence":0,
            "vie":100, #la vie de la plante losrqu'elle va se faire manger
            "sensibiliteTemp":5,
            "periodeDeLAnnee":False,
            "moisMontaison":1,#3        #mois de mars
            "perteFeuilles":False,
            "mature":False
            }

    def saison(self):
        pass
    def reproduction(self):
        self.parent.genPlante(Erable, self.attributes["semence"])

class Laitue(Plante):
    def __init__ (self,parent,posX,posY,dict,temps):
        Plante.__init__ (self,parent,posX,posY,dict,temps)
        self.dict=dict
        self.attributes={
            "posX":posX,
            "posY":posY,
            "age":0,
            "naissance":temps,
            "valCritique":40,
            "esperanceVie":random.randrange(55,75), #jours
            "nivEau":100,
            "nivSoleil":100,
            "nutriments":100, #max 100
            "consommation":random.randrange(3,10),
            "taille":random.randrange(3,6),
            "tailleLimite" :100,
            "sante":True,
            "terrestre":True,
            "aquatique":False,
            "temperatureIdeale":18,
            "temperatureMin":-18,
            "temperatureMax":30,
            "mort":False,
            "valeurMax":100,
            "semence":0,
            "vie":100, #la vie de la plante losrqu'elle va se faire manger
            "sensibiliteTemp":5,
            "periodeDeLAnnee":False,
            "moisMontaison":5,        #mois de mai
            "perteFeuilles":False,
            "mature":False
            }

    def maladie(self):
        if self.parent.dictBiomePlaine.get('humiditeAir') > 60:
            if random.randrange(0,10)==1:
                self.attributes["sante"]=False
        else:
            if random.randrange(0,10000)==1:
                self.attributes["sante"]=False
    def reproduction(self):
        self.parent.genPlante(Laitue, self.attributes["semence"])

class Peuplier(Plante):
    def __init__ (self,parent,posX,posY,dict,temps):
        Plante.__init__ (self,parent,posX,posY,dict,temps)
        self.dict=dict
        self.attributes={
            "posX":posX,
            "posY":posY,
            "age":0,
            "naissance":temps,
            "valCritique":40,
            "esperanceVie":random.randrange(21900,29200), #jours -> 60-80 ans
            "nivEau":100,
            "nivSoleil":100,
            "nutriments":100, #max 100
            "consommation":random.randrange(3,10),
            "taille":random.randrange(45,75),
            "tailleLimite" :900,
            "sante":True,
            "terrestre":True,
            "aquatique":False,
            "temperatureIdeale":18,
            "temperatureMin":-20,
            "temperatureMax":25,
            "mort":False,
            "valeurMax":100,
            "semence":0,
            "vie":100, #la vie de la plante losrqu'elle va se faire manger
            "sensibiliteTemp":10,
            "periodeDeLAnnee":False,
            "moisMontaison":1,#3        #mois de mars
            "perteFeuilles":False,
            "mature":False
            }

    def saison(self):
        pass
    def reproduction(self):
        self.parent.genPlante(Peuplier, self.attributes["semence"])

class Sapin(Plante):
    def __init__ (self,parent,posX,posY,dict,temps):
        Plante.__init__ (self,parent,posX,posY,dict,temps)
        self.dict=dict
        self.attributes={
            "posX":posX,
            "posY":posY,
            "age":0,
            "naissance":temps,
            "valCritique":40,
            "esperanceVie":random.randrange(73000,110000), #jours -> 200-300 ans
            "nivEau":100,
            "nivSoleil":100,
            "nutriments":100, #max 100
            "consommation":random.randrange(3,8),
            "taille":random.randrange(10,25),
            "tailleLimite" :1000,
            "sante":True,
            "terrestre":True,
            "aquatique":False,
            "temperatureIdeale":0,
            "temperatureMin":-35,
            "temperatureMax":28,
            "mort":False,
            "valeurMax":100,
            "semence":0,
            "vie":10000, #la vie de la plante losrqu'elle va se faire manger
            "sensibiliteTemp":10,
            "periodeDeLAnnee":False,
            "moisMontaison":1,
            "perteFeuilles":False,
            "mature":False
            }

    def saison(self):
        pass
    def reproduction(self):
        self.parent.genPlante(Sapin, self.attributes["semence"])

if __name__ == '__main__':
    print("Dans Vegetaux")
