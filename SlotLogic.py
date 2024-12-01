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
    def __init__(self, viewPort, paytable, winlines, freeGameSymbol, screenSize):
        self.viewPort, self.paytable, self.winlines, self.screenSize = viewPort, paytable, winlines, screenSize
        # Maps each winline to the current viewport
        self.winlineSymbols = [[self.viewPort[j][self.winlines[i][j]] for j in range(5)] for i in range(len(self.winlines))]
        # Counts Free Game Scatters
        self.freeGameCheck = sum([reel.count(freeGameSymbol) for reel in self.viewPort])
        self.payouts, self.totalPayout = [], 0
    
    def checkForWins(self):
        '''
        Main win check module, checks each winlines for the largest win on that winline

        Uses winlineSymbols, and paytable

        Return: 
            float of the total win
            array of each location of the paytable which the wins come from
        ''' 
        self.payouts, self.totalPayout = [], 0
        for currentWinline in self.winlineSymbols:
            payout = [0,3] #Default for no win

            for i in range(self.screenSize[0],2,-1): #Loops over possible win lengths
                if currentWinline[:i].count(0) == i: #Checks if the first i positions are wilds
                    payout = [0,i-3]
                    break

            try:
                firstNoneWild = [sym for sym in currentWinline if sym != 0][0]
                for i in range(self.screenSize[0],2,-1): #Checks for Wild Wins
                    if currentWinline[:i].count(0) + currentWinline[:i].count(firstNoneWild) == i:
                        if payout == [0,3]:
                            payout = [firstNoneWild,i-3]
                        elif self.paytable[firstNoneWild][i-3] > self.paytable[payout[0]][payout[1]]:
                            payout = [firstNoneWild,i-3]
            except:
                pass

            if payout != [0,3]:
                self.payouts.append(payout)
                self.totalPayout += self.paytable[payout[0]][payout[1]]


class Spin:  
    def __init__(self, reelType):
        self.slotData = SlotData(config)
        self.slotData.importData()
        self.reels, self.paytable, self.winlines = reelType, self.slotData.paytable, self.slotData.winlines
    
    def spin(self):
        self.randomReelStops = [random.randint(0,len(self.reels[i])-3) for i in range(5)]
        self.viewport = Viewport(self.reels,[5,3],self.randomReelStops)
        self.viewport.viewport = self.viewportMod(self.viewport.viewport)
        self.slotGame = SlotGame(self.viewport.viewport, self.paytable, self.winlines, 9,[5,3])
        self.slotGame.checkForWins()
        self.slotGame.totalPayout *= self.payoutMod()

    def viewportMod(self, viewport):
        return viewport

    def payoutMod(self):
        mod = 1 
        return mod
    
