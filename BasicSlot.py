
from Reports import *
from SlotLogic import *
from SlotData import *

config = "/Users/connorkelly/Documents/Work/BasicSlotGame/BasicSlot.xlsx"  

class Main:
    def __init__(self, spinCount, config):
        self.slotData = SlotData(config)
        self.slotData.importData()
        self.report = Report(spinCount)
        self.baseSpin = BaseGame(self.slotData.baseReels, self.slotData.paytable, self.slotData.winlines)
        self.freeSpin = FreeGame(self.slotData.freeReels, self.slotData.paytable, self.slotData.winlines)

    def spin(self): 
        #Viewport Can Be edited here
        self.baseSpin.baseSpin()
        if self.baseSpin.freeSpinFlag:
            freeSpinPay = 0
            for _ in range(int(self.slotData.freeSpinCount)):
                #Viewport Can Be edited here
                self.freeSpin.freeSpin()
                freeSpinPay += self.freeSpin.totalPay
            self.report.log(self.baseSpin.totalPay, freeSpinPay, self.baseSpin.freeSpinFlag)
        else:
            self.report.log(self.baseSpin.totalPay, 0, self.baseSpin.freeSpinFlag)      

    def sim(self):
        for i in range(self.report.spinCount):  
            self.spin()
            if i % (self.report.spinCount/10) == 0:
                print(f"{i / (self.report.spinCount/10) }")
        self.report.reportPrint()
    
main = Main(10000, config)
main.sim()
