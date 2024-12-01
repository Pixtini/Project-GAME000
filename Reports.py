import datetime, numpy, time

class Report:
    def __init__(self, spinCount):
        self.totalWin, self.baseWin, self.freegameWin = [], [], []
        self.freeGameCount = 0
        self.spinCount = spinCount
        self.t1 = time.time()
        self.winMap = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    
    def winDisCreator(self, winType):
        d = dict.fromkeys(winType, 0)
        for win in winType:
            d[win] += 1
        return d
    
    def log(self, baseWin, freeWin, freeGameFlag):
        self.baseWin.append(baseWin)
        if freeGameFlag == 3:
            self.freeGameCount += 1
            self.freegameWin.append(freeWin)
            self.totalWin.append(baseWin+freeWin)
        else:
            self.totalWin.append(baseWin)
        

    def reportPrint(self):
        f = open(f"Report {datetime.datetime.now()}.txt", "a")
        f.write(f"OVERALL STATS\nSPIN COUNT\t{self.spinCount}\nTOTAL WIN\t{sum(self.totalWin)}\nBASE WIN\t{sum(self.baseWin)}\nFREE WIN\t{sum(self.freegameWin)}\nFREE TRIGGERS\t{self.freeGameCount}\n\n")

        f.write(f"RTP\t{sum(self.totalWin)/self.spinCount*100}\n")

        f.write(f"TOTAL WIN DIST\t {numpy.std(self.totalWin)}\n")
        totalWinDist = self.winDisCreator(self.totalWin)
        for win in totalWinDist:
            f.write(f"{win}\t{totalWinDist[win]}\n")
        f.write(f"\n")
        
        f.write(f"BASE WIN DIST\t {numpy.std(self.baseWin)}\n")
        baseWinDist = self.winDisCreator(self.baseWin)
        for win in baseWinDist:
            f.write(f"{win}\t{baseWinDist[win]}\n")
        f.write(f"\n")

        f.write(f"FREE WIN DIST\t {numpy.std(self.freegameWin)}\n")
        freeWinDist = self.winDisCreator(self.freegameWin)
        for win in freeWinDist:
            f.write(f"{win}\t{freeWinDist[win]}\n")
        f.write(f"\n")
        
        f.close()
        print(time.time() - self.t1)