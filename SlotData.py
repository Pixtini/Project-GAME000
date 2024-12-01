import pandas as pd, fnmatch
config = "/Users/connorkelly/Documents/Work/BasicSlotGame/BasicSlot.xlsx"

class SlotData:
    def __init__(self, config):
        self.config = config
        self.baseReels, self.freeReels, self.winlines, self.paytable = [], [], [], []
        reelsLen = pd.read_excel(config, 'BaseReels').columns.get_loc("Reel 1.1") - 1 
        self.reelAmount = [i for i in range(reelsLen)]

    def reelImport(self, type):
        reelsImport = pd.read_excel(self.config, type , usecols=self.reelAmount)
        reels = []
        for i in range(5):
            reel = reelsImport[f"Reel {i+1}"].values.tolist()
            wrapping = reel[0:2]
            reel.extend(wrapping)
            reels.append(reel)
        return reels

    def winlineImport(self):
        winlineImport = pd.read_excel(self.config, 'Winlines' , usecols=self.reelAmount)
        return winlineImport.values.tolist()

    def paytableImport(self):
        paytableImport = pd.read_excel(self.config, 'Paytable' , usecols=[0,1,2])
        return paytableImport.values.tolist()
    
    def freeSpinCountImport(self):
        paytableImport = pd.read_excel(self.config, 'Paytable' , usecols=[5])
        return paytableImport.values.tolist()[-1][0]
    
    def importData(self):
        self.baseReels = self.reelImport('BaseReels')
        self.freeReels = self.reelImport('FreeReels')
        self.winlines = self.winlineImport()
        self.paytable = self.paytableImport()
        self.freeSpinCount = self.freeSpinCountImport()
