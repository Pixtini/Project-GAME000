import random
from Reports import Report
from SlotData import *
config = "/Users/connorkelly/Documents/Work/BasicSlotGame/BasicSlot.xlsx"  

class Reels:
    def __init__(self, reels):
        self.reels = reels
 
class Viewport:
    def __init__(self, reels, screenSize, reelstops):
        self.reels = reels
        #Viewport object, based on where reels stopped and screen size, can be edited later based on features.
        self.viewport = [[self.reels[i][reelstops[i]+j] for j in range(screenSize[1])] for i in range(screenSize[0])] 

class SlotGame:
    def __init__(self, viewPort, paytable, winlines):
        self.viewPort, self.paytable, self.winlines = viewPort, paytable, winlines 
        # Maps each winline to the current viewport
        self.winlineSymbols = [[self.viewPort[j][self.winlines[i][j]] for j in range(5)] for i in range(len(self.winlines))]
        self.freeGameCheck = (sum([reel.count(9) for reel in self.viewPort]) == 3)
        self.payouts, self.totalPayout = [], 0
    
    def checkForWins(self):
        '''
        Takes a winline and checks it for the largest win

        Args:
            currentWinline: Array of the winline
        
        Return: 
            Position on Paytable that is the largest win detected on that winline, [0,3] if no win
        ''' 
        for currentWinline in self.winlineSymbols:
            payout = [0,3]

            for i in range(5,2,-1): #Checks for Wild Win
                if currentWinline[:i].count(0) == i:
                    if payout == [0,3]:
                        payout = [0,i-3]
                    elif self.paytable[0][i-3] > self.paytable[payout[0]][payout[1]]:
                        payout = [0,i-3]
            
            try:
                firstNoneWild = [sym for sym in currentWinline if sym != 0][0]
            except:
                firstNoneWild = 0

            if firstNoneWild != 0:
                for i in range(5,2,-1): #Checks for Wild Wins
                    if currentWinline[:i].count(0) + currentWinline[:i].count(firstNoneWild) == i:
                        if payout == [0,3]:
                            payout = [firstNoneWild,i-3]
                        elif self.paytable[firstNoneWild][i-3] > self.paytable[payout[0]][payout[1]]:
                            payout = [firstNoneWild,i-3]

            if payout != [0,3]:
                self.payouts.append(payout)
                self.totalPayout += self.paytable[payout[0]][payout[1]]


class Spin:  
    def __init__(self):
        self.slotData = SlotData(config)
        self.slotData.importData()
        self.reels, self.paytable, self.winlines = self.slotData.baseReels, self.slotData.paytable, self.slotData.winlines

    
    def spin(self):
        self.randomReelStops = [random.randint(0,len(self.reels[i])-3) for i in range(5)]
        self.viewport = Viewport(self.reels,[5,3],self.randomReelStops)
    
    def winprocess(self, viewport):
        self.slotGame = SlotGame(viewport, self.paytable, self.winlines)
        self.slotGame.checkForWins()



    
