
from Reports import *
from SlotLogic import *
from SlotData import *

config = "/Users/connorkelly/Documents/Work/BasicSlotGame/BasicSlot.xlsx"

class BaseGame(Spin):
    def __init__(self):
        super().__init__()
    
    def baseSpin(self):
        super().spin()
        self.totalPay = self.slotGame.totalPayout
        self.freeSpinFlag = self.slotGame.freeGameCheck


class FreeGame(Spin):
    def __init__(self):
        super().__init__()

    def freeSpin(self):
        self.totalFreePay = 0
        for _ in range(int(self.slotData.freeSpinCount)):
            super().spin()
            self.totalFreePay += self.slotGame.totalPayout

class Main:
    def __init__(self, spinCount, config):
        self.slotData = SlotData(config)
        self.slotData.importData()
        self.report = Report(spinCount)
        self.baseSpin = BaseGame()
        self.freeSpin = FreeGame()

    def spin(self): 
        self.baseSpin.baseSpin()
        if self.baseSpin.freeSpinFlag == 3:
            self.freeSpin.freeSpin()
            self.report.log(self.baseSpin.totalPay, self.freeSpin.totalFreePay, self.baseSpin.freeSpinFlag)
        else:
            self.report.log(self.baseSpin.totalPay, 0, self.baseSpin.freeSpinFlag)      

    def sim(self):
        for i in range(self.report.spinCount):  
            self.spin()
            if i % (self.report.spinCount/10) == 0:
                print(f"{i / (self.report.spinCount/10) }")
        self.report.reportPrint()
    
main = Main(1000000, config)
main.sim()
