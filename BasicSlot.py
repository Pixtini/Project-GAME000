
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
        if baseSpin.freeSpinFlag:
            freeSpin = FreeGame(self.slotData.freeReels, self.slotData.paytable, self.slotData.winlines)
            freeSpin.freeSpins(int(self.slotData.freeSpinCount))
            self.report.log(baseSpin.totalPay, freeSpin.totalPay, baseSpin.freeSpinFlag)
        else:
            self.report.log(baseSpin.totalPay, 0, baseSpin.freeSpinFlag)      

    def sim(self):
        for i in range(self.report.spinCount):  
            self.spin()
        self.report.reportPrint()
    
main = Main(1000, config)
main.sim()
