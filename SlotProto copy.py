import pygame
from BasicSlot import *
from SlotData import *

pygame.init()
X = 750
Y = 500
config = "/Users/connorkelly/Documents/Work/Project-GAME000/BasicSlot.xlsx"
path = "/Users/connorkelly/Documents/Work/Project-GAME000/"
symbolMap = ["Wild","R1","R2","Y1","Y2","B1","B2","G1","G2","G3","Scatter"]
winlineMap = [(75,75), (75, 225), (75, 375), (75,75), (75,75)]
scrn = pygame.display.set_mode((X, Y))

class Prototype():
    def __init__(self):
        self.symbolMap = ["Wild","R1","R2","Y1","Y2","B1","B2","G1","G2","G3","Scatter"]
        self.winlineMap = [(75,75), (75, 225), (75, 375), (75,75), (75,75)]
        self.scrn = pygame.display.set_mode((X, Y))
        
        main = MainGame(1, config)
        main.spin()
        self.viewport = main.baseSpin.baseEvents.baseViewport       
        self.activeWinlines = main.baseSpin.baseEvents.baseActiveWinlines
        self.win = main.baseSpin.baseEvents.basePay
        self.totalFreePay = 0
        self.freeSpinNum = 0
        self.freeGame = False
        
        data = SlotData(config)
        data.importData()
        self.freeGameSpinCount = data.freeSpinCount[0]

    def symbolLoad(self):
        for x, view in enumerate(self.viewport):
            for y, sym in enumerate(view):
                scrn.blit(pygame.image.load(path+"symbols/"+self.symbolMap[sym]+".png").convert(), (x*150, y*150))

    def winlineLoad(self):
        for x, winline in enumerate(self.activeWinlines):
            if winline <= 2:
                pygame.draw.line(scrn, (0,255,0), (75,75+150*winline), (675,75+150*winline), width=4)
            if winline == 3:
                pygame.draw.line(scrn, (0,255,0), (75,75), (375,375), width=6)
                pygame.draw.line(scrn, (0,255,0), (375,375), (675,75), width=6)
            if winline == 4:
                pygame.draw.line(scrn, (0,255,0), (75,375), (375,75), width=6)
                pygame.draw.line(scrn, (0,255,0), (375,75), (675,375), width=6)

    def winDisplay(self):
        font = pygame.font.SysFont('freesanbold.ttf', 25)
        if self.freeGame:
            winText = font.render('Total FREE Win = £' + str(self.win) + " Spin Count : " + str(self.freeGameSpinCount) + "/5", True, (0, 255, 0))
        else:
            winText = font.render('Total Win = £' + str(self.win), True, (0, 255, 0))
        textRect = winText.get_rect()
        textRect.center = (200, 475)
        scrn.blit(winText, textRect)


    def baseGameLoop(self):
        scrn.fill([0,0,0])   
        self.symbolLoad()
        self.winlineLoad()
        pygame.display.flip()
        pygame.time.wait(800)
        self.winDisplay()
        pygame.display.flip()
        pygame.time.wait(3000)



prototype = Prototype()
status = True
while (status): 
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            status = False
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_SPACE:
                prototype.baseGameLoop()
                pygame.display.flip()
                pygame.time.wait(800)
            
                        
pygame.quit()