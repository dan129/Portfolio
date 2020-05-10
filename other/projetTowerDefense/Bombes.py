# -*- coding: UTF-8 -*-

import helper
import Creeps

class Bombes():
    portee=20 # la circonference où la bombe va pouvoir explosé...
    def __init__(self,parent,x,y):
        self.parent=parent
        self.x=x
        self.y=y
    def Exploser(self,creeps):    
        distance = Helper.calcDistance(self.x, self.y, creep.x, creep.y)
        if distance < self.portee:
            self.compteurTir+=1
            if self.compteurTir == self.vitesseTir:
                self.compteurTir=1
                return 0;
            else:
                return 1
        
        
class BombeDommage(Bombes):       
    portee=100
    degat=5 #detruit le creep 
    
    def __init__(self,parent,x,y):
        Bombes.__init__(self, parent, x, y)
        self.portee=BombeDommage.portee
        self.degat=BombeDommage.degat
    
    
