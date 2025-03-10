#This is in the new Project
from Reports import *
from SlotLogic import *
from SlotData import *
import numpy as np

config = "/Users/connorkelly/Documents/Work/Project-GAME000/BasicSlot.xlsx"

class BaseGame(Spin): 
    def __init__(self):
        super().__init__()
        self.baseEvents = Events()
    
    def baseSpin(self):
        self.slotData.baseSetSelection['p'] = (self.slotData.baseSetSelection.setSelectBG_weight)/(self.slotData.baseSetSelection.setSelectBG_weight.sum())
        self.reels = self.slotData.baseSets[int(np.random.choice(self.slotData.baseSetSelection['setSelectBG'],1 ,p = self.slotData.baseSetSelection['p'], replace= False )[0])]
        
        super().spin() #Spin function from parent class
        self.totalPay = self.slotGame.totalPayout
        self.freeSpinFlag = self.slotGame.freeGameCheck #To check if trigger FG
        
        self.baseEvents.basePay = self.slotGame.totalPayout
        self.baseEvents.baseViewport = self.viewport.viewport
        self.baseEvents.baseActiveWinlines = self.activeWinlines
        if self.freeSpinFlag == 3:
            self.baseEvents.freeSpinFlag = True


class FreeGame(Spin):
    def __init__(self):
        super().__init__()
        self.freeEvents = Events()

    def freeSpin(self):
        self.totalFreePay = 0 
        for i in range(int(self.slotData.freeSpinCount[1])):
            self.slotData.freeSetSelection['p'] = (self.slotData.freeSetSelection.setSelectFG_weight)/(self.slotData.freeSetSelection.setSelectFG_weight.sum())
            self.reels = self.slotData.freeSets[int(np.random.choice(self.slotData.freeSetSelection['setSelectFG'],1 ,p = self.slotData.freeSetSelection['p'], replace= False )[0])]
            super().spin()
            self.totalFreePay += self.slotGame.totalPayout
            
            self.freeEvents.freePay[i] = self.slotGame.totalPayout
            self.freeEvents.freeViewport[i]= self.viewport.viewport
            self.freeEvents.freeActiveWinlines[i] = self.activeWinlines

class Events():
    def __init__(self):
        self.slotData = SlotData(config)
        self.slotData.importData()
        
        self.basePay = 0
        self.baseViewport = []
        self.baseActiveWinlines = []
        self.freeSpinFlag = False

        self.freePay = [0 for _ in range(int(self.slotData.freeSpinCount[1]))]
        self.freeViewport = [[] for _ in range(int(self.slotData.freeSpinCount[1]))]
        self.freeActiveWinlines = [[] for _ in range(int(self.slotData.freeSpinCount[1]))]



class MainGame:
    def __init__(self, spinCount, config):
        self.slotData = SlotData(config)
        self.slotData.importData()
        self.report = Report(spinCount) #Inits the report to log later
        self.baseSpin = BaseGame()
        self.freeSpin = FreeGame()
    
    def spin(self): 
        self.baseSpin.baseSpin()
        
        if self.baseSpin.freeSpinFlag == 3:         
            self.freeSpin.freeSpin()
            self.report.log(self.baseSpin.totalPay, self.freeSpin.totalFreePay, self.baseSpin.freeSpinFlag) #Logs data, to be printed into the report
        else:
            self.report.log(self.baseSpin.totalPay, 0, self.baseSpin.freeSpinFlag)  # Zero for no free game pay 
        




    def sim(self):
        for i in range(self.report.spinCount):  
            self.spin()
            if i % (self.report.spinCount/10) == 0:
                print(f"{i / (self.report.spinCount/10) }")
        self.report.reportPrint()
    
main = MainGame(1, config)


