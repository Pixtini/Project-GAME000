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

def symbolLoad(viewport):
    for x, view in enumerate(viewport):
        for y, sym in enumerate(view):
            scrn.blit(pygame.image.load(path+"symbols/"+symbolMap[sym]+".png").convert(), (x*150, y*150))

def winlineLoad(activeWinlines):
    for x, winline in enumerate(activeWinlines):
        if winline <= 2:
            pygame.draw.line(scrn, (0,255,0), (75,75+150*winline), (675,75+150*winline), width=4)
        if winline == 3:
            pygame.draw.line(scrn, (0,255,0), (75,75), (375,375), width=6)
            pygame.draw.line(scrn, (0,255,0), (375,375), (675,75), width=6)
        if winline == 4:
            pygame.draw.line(scrn, (0,255,0), (75,375), (375,75), width=6)
            pygame.draw.line(scrn, (0,255,0), (375,75), (675,375), width=6)

def winDisplay(win, freeGame, spinCount):
    font = pygame.font.SysFont('freesanbold.ttf', 25)
    if freeGame:
        winText = font.render('Total FREE Win = £' + str(win) + " Spin Count : " + str(spinCount) + "/5", True, (0, 255, 0))
    else:
        winText = font.render('Total Win = £' + str(win), True, (0, 255, 0))
    textRect = winText.get_rect()
    textRect.center = (200, 475)
    scrn.blit(winText, textRect)

def gameLoop(pay, viewport, winlines, freeGame, totalFreeGamePay, freeSpinNum):
    scrn.fill([0,0,0])
    symbolLoad(viewport)
    winlineLoad(winlines)
    if freeGame:
        winDisplay(totalFreeGamePay, True, freeSpinNum)
    else:
        winDisplay(pay, False, 0)
    pygame.display.flip()
    pygame.time.wait(3000)



status = True
while (status): 
    for i in pygame.event.get():

        if i.type == pygame.QUIT:
            status = False

        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_SPACE:
                scrn.fill([0,0,0])
                main = MainGame(1, config)
                main.spin()
                gameLoop(main.baseSpin.baseEvents.basePay, main.baseSpin.baseEvents.baseViewport, main.baseSpin.baseEvents.baseActiveWinlines, False, 0, 0)
                pygame.display.flip()
                pygame.time.wait(800)
                
                if(main.baseSpin.baseEvents.freeSpinFlag):
                    scrn.fill([0,0,0])
                    font = pygame.font.SysFont('freesanbold.ttf', 55)
                    winText = font.render('FREEGAMES!', True, (0, 255, 0))
                    textRect = winText.get_rect()
                    textRect.center = (200, 275)
                    scrn.blit(winText, textRect)
                    pygame.display.flip()
                    pygame.time.wait(800)

                    totalFreeGamePay = 0
                    for i in range(int(main.slotData.freeSpinCount[1])):
                        totalFreeGamePay += main.freeSpin.freeEvents.freePay[i]
                        gameLoop(main.freeSpin.freeEvents.freePay[i], main.freeSpin.freeEvents.freeViewport[i], main.freeSpin.freeEvents.freeActiveWinlines[i], True, totalFreeGamePay, i+1)
                        pygame.display.flip()
                        





pygame.quit()