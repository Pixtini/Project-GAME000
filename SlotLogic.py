import random
from Reports import Report

class Reels:
    def __init__(self, reels):
        self.reels = reels

    def viewPortLooker(self, reelstops):
        return [[self.reels[i][reelstops[i]+j] for j in range(3)] for i in range(5)]

class SlotGame:
    def __init__(self, viewPort, paytable, winlines):
        self.viewPort, self.paytable, self.winlines = viewPort, paytable, winlines 

    def viewPortToWinlines(self):
        return [[self.viewPort[j][self.winlines[i][j]] for j in range(5)] for i in range(len(self.winlines))]
    
    def checkForWin(self, currentWinline):
        
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
        return [self.checkForWin(winline) for winline in allWinlines if self.checkForWin(winline)[1] != 3 ]

    def retrievePayouts(self, payouts):
        totalPayout = 0
        for payout in payouts:
            totalPayout += self.paytable[payout[0]][payout[1]]
        return totalPayout
    
    def freeSpinCheck(self):
        return (sum([reel.count(9) for reel in self.viewPort]) == 3)
    
    def winInstance(self):
        allWinlines = self.viewPortToWinlines()
        payouts = self.allPayouts(allWinlines)
        totalPay = self.retrievePayouts(payouts)
        return totalPay

class Spin:
    def __init__(self, reels, paytable, winlines):
        self.reels, self.paytable, self.winlines = reels, paytable, winlines
        self.viewPortInstance = []
        self.randomReelStops = [random.randint(0,len(self.reels[i])-3) for i in range(5)]
    
    def performSpin(self):
        gameReels = Reels(self.reels)
        self.viewPortInstance = gameReels.viewPortLooker(self.randomReelStops)
        return self.viewPortInstance

class BaseGame(Spin):
    def __init__(self, reels, paytable, winlines):
        super().__init__(reels, paytable, winlines)
        self.viewPortInstance = self.performSpin()
        self.slotGame = SlotGame(self.viewPortInstance, self.paytable, self.winlines)
        self.totalPay = self.slotGame.winInstance()
        self.freeSpinFlag = self.slotGame.freeSpinCheck()

class FreeGame(Spin):
    def __init__(self, reels, paytable, winlines):
        super().__init__(reels, paytable, winlines)
        self.viewPortInstance = self.performSpin()
        self.slotGame = SlotGame(self.viewPortInstance, self.paytable, self.winlines)
        self.totalPay = self.slotGame.winInstance()

    
