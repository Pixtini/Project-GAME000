import pandas as pd, fnmatch

config = "/Users/connorkelly/Documents/Work/Project-GAME000/BasicSlot.xlsx"
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

class SlotData:
    def __init__(self, config):
        self.config = config
        self.baseReels, self.freeReels, self.winlines, self.paytable = [], [], [], []

    def gameDataImport(self):
        gameData = pd.read_excel(self.config, 'GameData')
        self.reelAmount = [i for i in range(int(gameData.loc[gameData["Type"] == "Reels", "Data"]))]
        self.reelHeight = int(gameData.loc[gameData["Type"] == "Height", "Data"])

    def reelImport(self, type):
        reelsImport = pd.read_excel(self.config, type , usecols=self.reelAmount)
        reels = []
        for i in range(len(self.reelAmount)):
            reel = reelsImport[f"Reel {i+1}"].values.tolist()
            wrapping = reel[0:self.reelHeight-1]
            reel.extend(wrapping)
            reels.append(reel)
        return reels
    
    def weightTable(self, sheet ,row, cols):
        wt = pd.read_excel(config, sheet_name=sheet, header=row, usecols=cols).dropna()
        return wt
    
    def sets(self, type):
        gameData = pd.read_excel(self.config, 'GameData')
        setCount = int(gameData.loc[gameData["Type"] == type+"_sets", "Data"])
        sets = [self.reelImport(type+'_'+str(i)) for i in range(setCount)]
        return sets

    def winlineImport(self):
        winlineImport = pd.read_excel(self.config, 'Winlines' , usecols=self.reelAmount)
        return winlineImport.values.tolist()

    def paytableImport(self):
        paytableImport = pd.read_excel(self.config, 'Paytable' , usecols=[0,1,2])
        return paytableImport.values.tolist()
    
    def freeSpinCountImport(self):
        freeSpinAmount = pd.read_excel(self.config, 'Paytable' , usecols=[5])
        freeSpinSymbol = pd.read_excel(self.config, 'Paytable' , usecols=[4])
        return [freeSpinSymbol.values.tolist()[-1][0],freeSpinAmount.values.tolist()[-1][0]]
    
    def importData(self):
        self.gameData = self.gameDataImport()
        self.winlines = self.winlineImport()
        self.paytable = self.paytableImport()
        self.freeSpinCount = self.freeSpinCountImport()
        self.baseSets = self.sets("bg")
        self.freeSets = self.sets('fg')
        
        self.baseSetSelection = self.weightTable('Total Game', 1, 'H:I')
        self.freeSetSelection = self.weightTable('Total Game', 1, 'L:M')



