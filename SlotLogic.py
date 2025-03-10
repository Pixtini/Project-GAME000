import random
from Reports import Report
from SlotData import *
import numpy as np
config = "/Users/connorkelly/Documents/Work/Project-GAME000/BasicSlot.xlsx"

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
        self.payouts, self.totalPayout, self.activeWinlines = [], 0, []
    
    def checkForWins(self):
        '''
        Main win check module, checks each winlines for the largest win on that winline

        Uses winlineSymbols, and paytable

        Return: 
            float of the total win
            array of each location of the paytable which the wins come from
        ''' 
        self.payouts, self.totalPayout, paytableSize, self.activeWinlines= [], 0, len(self.paytable[0]) , []
        for currentWinlineIndex, currentWinlineSymbols in enumerate(self.winlineSymbols):
            payout = [0,paytableSize] #Default for no win

            for i in range(self.screenSize[0],2,-1): #Loops over possible win lengths
                if currentWinlineSymbols[:i].count(0) == i: #Checks if the first i positions are wilds
                    payout = [0,i-paytableSize]
                    break

            try: #Checks for first possible none wild win
                firstNoneWild = [sym for sym in currentWinlineSymbols if sym != 0][0]
                for i in range(self.screenSize[0],2,-1): #Checks for Wild Wins
                    if currentWinlineSymbols[:i].count(0) + currentWinlineSymbols[:i].count(firstNoneWild) == i: #Takes the slice of size i, checks if that is just 1 symbol and/or wilds
                        if payout == [0,paytableSize]: #If there is no win
                            payout = [firstNoneWild,i-paytableSize]
                            break
                        elif self.paytable[firstNoneWild][i-paytableSize] > self.paytable[payout[0]][payout[1]]:
                            payout = [firstNoneWild,i-paytableSize]
                            break
            except:
                pass
            
            if payout != [0,paytableSize]: #Data appends and totalling
                self.payouts.append(payout)
                self.totalPayout += self.paytable[payout[0]][payout[1]]
                self.activeWinlines.append(currentWinlineIndex)


class Spin:  
    def __init__(self):
        self.slotData = SlotData(config)
        self.slotData.importData()
        self.reels, self.paytable, self.winlines, self.screenSize, self.freegameSymbol = [], self.slotData.paytable, self.slotData.winlines, [5,3], self.slotData.freeSpinCount[0]
    
    def spin(self):
        self.randomReelStops = [random.randint(0,len(self.reels[i])-self.screenSize[1]) for i in range(self.screenSize[0])]  # Amount of random numbers of the screens length 
        self.viewport = Viewport(self.reels, self.screenSize, self.randomReelStops) # X x Y random symbols, whats visible on the screen
        self.viewport.viewport = self.viewportMod(self.viewport.viewport) # Changes the Viewport from the previous, function to be overridden in child class
        self.slotGame = SlotGame(self.viewport.viewport, self.paytable, self.winlines, self.freegameSymbol, self.screenSize) # Inits Slot Logic
        self.slotGame.checkForWins() # Analyse the current viewport for all the wins of each winline
        self.activeWinlines = self.slotGame.activeWinlines 
        self.slotGame.totalPayout *= self.payoutMod() # Modifies the win total, i.e. Multipliers, function to be overriden in child class

    def viewportMod(self, viewport):
        '''
        Takes the current viewport and modifies it via some game method , example, upgrading symbols
        ''' 
        viewport[4] = [10,10,10]
        return viewport

    def payoutMod(self):
        '''
        Creates a multiplier to target the total, example, multiplier symbols on reels
        ''' 
        mod = 1 
        return mod
    
    def symCount(self, sym):
        return sum([reel.count(sym) for reel in self.viewport.viewport])
        
    
