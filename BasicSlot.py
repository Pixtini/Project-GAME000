
from Reports import *
from SlotLogic import *
from SlotData import *

config = "/Users/connorkelly/Documents/Work/BasicSlotGame/BasicSlot.xlsx"  

class Main:
    def __init__(self, spinCount, config):
        self.slotData = SlotData(config)
        self.slotData.importData()
        self.report = Report(spinCount)

    def spin(self): 
        baseSpin = BaseGame(self.slotData.baseReels, self.slotData.paytable, self.slotData.winlines)
        #Viewport Can Be edited here
        baseSpin.baseSpin()
        if baseSpin.freeSpinFlag:
            freeSpinPay = 0
            for _ in range(int(self.slotData.freeSpinCount)):
                freeSpin = FreeGame(self.slotData.freeReels, self.slotData.paytable, self.slotData.winlines)
                #Viewport Can Be edited here
                freeSpin.freeSpin()
                freeSpinPay += freeSpin.totalPay
            self.report.log(baseSpin.totalPay, freeSpinPay, baseSpin.freeSpinFlag)
        else:
            self.report.log(baseSpin.totalPay, 0, baseSpin.freeSpinFlag)      

    def sim(self):
        for i in range(self.report.spinCount):  
            self.spin()
            if i % (self.report.spinCount/10) == 0:
                print(f"{i / (self.report.spinCount/10) }")
        self.report.reportPrint()
    
main = Main(100_000_000, config)
main.sim()
