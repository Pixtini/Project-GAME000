import pandas as pd

class SlotData:
    def __init__(self, config):
        self.config = config
        self.baseReels, self.freeReels, self.winlines, self.paytable = [], [], [], []

    def reelImport(self, type):
        reelsImport = pd.read_excel(self.config, type ,nrows = 40, usecols=[0,1,2,3,4])
        reels = []
        for i in range(5):
            reel = reelsImport[f"Reel {i+1}"].values.tolist()
            wrapping = reel[0:2]
            reel.extend(wrapping)
            reels.append(reel)
        return reels

    def winlineImport(self):
        winlineImport = pd.read_excel(self.config, 'Winlines' ,nrows = 5, usecols=[0,1,2,3,4])
        return winlineImport.values.tolist()

    def paytableImport(self):
        paytableImport = pd.read_excel(self.config, 'Paytable' ,nrows = 10, usecols=[0,1,2])
        return paytableImport.values.tolist()
    
    def freeSpinCountImport(self):
        paytableImport = pd.read_excel(self.config, 'Paytable' ,nrows = 10, usecols=[5])
        return paytableImport.values.tolist()[-1][0]
    
    def importData(self):
        self.baseReels = self.reelImport('BaseReels')
        self.freeReels = self.reelImport('FreeReels')
        self.winlines = self.winlineImport()
        self.paytable = self.paytableImport()
        self.freeSpinCount = self.freeSpinCountImport()

