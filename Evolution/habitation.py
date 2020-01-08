# -*- coding: utf-8 -*-
"""
*********************************************************
*class habitation contient un X et Y qui vont etre declarer par superclass
************************************************************
"""
class Habitation():
    def __init__(self,parent):
        self.parent = parent
        self.attributes = {
            "posX":None,
            "posY":None
            }
"""
******************************************************
* terrier est une super class d'habitation pour les lapin,contient X et Y
* les lapins vont contenir les attributs habitX et habitY qui sont les coords
* de position X et Y de son terrier, la methode dormir va le faire deplacer au terrier
* avant de pouvoir dormir
*******************************************************
"""  
class Terrier(Habitation):
    def __init__(self, parent,newX,newY):
        super().__init__(parent)
        self.attributes.update({
            "posX":newX,
            "posY":newY
            })

"""
*****************************************************
* caverne pour les ours, les cavernes vont etre genere
* au debut de la simulation (selon une valeur de perlin noise peut etre?)
*******************************************************
"""
class Caverne(Habitation):
    def __init__(self, parent,newX,newY):
        super().__init__(parent)
        self.attributes.update({
        "posX":newX,
        "posY":newY
        })