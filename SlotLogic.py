import random
from Reports import Report

class Reels:
    ''' Reel Data and Creates ViewPort

    Attributes:
        reels: The Reels of the slot game
    '''
    def __init__(self, reels):
        '''
        Inits Reels with reels
        '''
        self.reels = reels
    
class Viewport:
    def __init__(self, reels):
        self.reels = reels

    def viewPortLooker(self, reelstops):
        '''
        Creates the viewport

        Args:
            reelstops: Where each reel stops , should be random most of the time
        
        Returns: 
            5x3 Array that is the viewport
        '''
        return [[self.reels[i][reelstops[i]+j] for j in range(3)] for i in range(5)]   

class SlotGame:
    ''' Slot game class

    Takes the viewport, and translates it to the winlines, checks for wins and free spins

    Attributes:
        viewPort:
        paytable:
        winlines:

    '''

    def __init__(self, viewPort, paytable, winlines):
        '''
        Inits Reels with viewport, paytable, winlines
        '''
        self.viewPort, self.paytable, self.winlines = viewPort, paytable, winlines 

    def viewPortToWinlines(self):
        '''
        Translates viewport to the winlines
        
        Returns: 
            Array that has each winline from the viewport
        '''
        return [[self.viewPort[j][self.winlines[i][j]] for j in range(5)] for i in range(len(self.winlines))]
    
    def checkForWin(self, currentWinline):
        '''
        Takes a winline and checks it for the largest win

        Args:
            currentWinline: Array of the winline
        
        Returns: 
            Position on Paytable that is the largest win detected on that winline, [0,3] if no win
        ''' 
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
        
        return payout

    def allPayouts(self, allWinlines):        
        '''
        Checks Payout for all winlines

        Args:
            allWinLines: Array that contains all the winlines
        
        Returns: 
            Array of all the valid win positions
        ''' 
        return [self.checkForWin(winline) for winline in allWinlines if self.checkForWin(winline)[1] != 3 ]

    def retrievePayouts(self, payouts):
        '''
        Collects Payouts

        Args:
            payouts: Array that contains all the payout locations
        
        Returns: 
            Float value that is the total win for that current viewport
        ''' 
        totalPayout = 0
        for payout in payouts:
            totalPayout += self.paytable[payout[0]][payout[1]]
        return totalPayout
    
    def freeSpinCheck(self):
        '''
        Checks for freeSpins
        
        Returns: 
            Boolean based on wether free spins or not
        ''' 
        return (sum([reel.count(9) for reel in self.viewPort]) == 3)
    
    def winInstance(self):
        '''
        Brings everything togethor, takes viewport and performs all steps
        
        Returns: 
            Float of the win total
        ''' 
        allWinlines = self.viewPortToWinlines()
        payouts = self.allPayouts(allWinlines)
        totalPay = self.retrievePayouts(payouts)
        return totalPay

class Spin:  
    ''' Spin class, performs the RNG for that spin

    Obtains random reelstops , and then returns the current viewport instance based on those stops

    Attributes:
        reels:
        paytable:
        winlines:
    '''
    def __init__(self, reels, paytable, winlines):
        '''
        Inits Reels with viewport, paytable, winlines
        '''
        self.reels, self.paytable, self.winlines = reels, paytable, winlines
        self.viewPortInstance = []
        self.randomReelStops = [random.randint(0,len(self.reels[i])-3) for i in range(5)]
    
    def performSpin(self):
        '''
        Inits game reels, and retrieves viewport from random reelstops
        
        Returns: 
           2D Array of the Viewport Instance
        ''' 
        viewport = Viewport(self.reels)
        self.viewPortInstance = viewport.viewPortLooker(self.randomReelStops)
        return self.viewPortInstance
    
    def spin(self):
        self.slotGame = SlotGame(self.viewPortInstance, self.paytable, self.winlines)
        self.totalPay = self.slotGame.winInstance()


class BaseGame(Spin):
    def __init__(self, reels, paytable, winlines):
        super().__init__(reels, paytable, winlines)
        self.viewPortInstance = self.performSpin()
    
    def baseSpin(self):
        super().spin()
        self.freeSpinFlag = self.slotGame.freeSpinCheck()

class FreeGame(Spin):
    def __init__(self, reels, paytable, winlines):
        super().__init__(reels, paytable, winlines)
        self.viewPortInstance = self.performSpin()

    def freeSpin(self):
        super().spin()

    
