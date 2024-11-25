
from Reports import *
from SlotLogic import *
from SlotData import *

config = "/Users/connorkelly/Documents/Work/Python/SlotGame/BasicSlot.xlsx"
slotData = SlotData(config)
slotData.importData()

report = Report(10000)

for i in range(report.spinCount):  
    baseSpin = BaseGame(slotData.baseReels, slotData.paytable, slotData.winlines)
    if baseSpin.freeSpinFlag:
        freeSpin = FreeGame(slotData.freeReels, slotData.paytable, slotData.winlines)
        report.log(baseSpin.totalPay, freeSpin.totalPay, baseSpin.freeSpinFlag)
    else:
        report.log(baseSpin.totalPay, 0, baseSpin.freeSpinFlag)

report.reportPrint()
