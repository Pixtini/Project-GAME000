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

def drawWinline(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

def winDisplay(win):
    font = pygame.font.SysFont('freesanbold.ttf', 25)
    winText = font.render('Total Win = £' + str(win), True, (0, 255, 0))
    textRect = winText.get_rect()
    textRect.center = (100, 475)
    scrn.blit(winText, textRect)


    main = MainGame(1, config)
    main.spin()
def gameLoop(pay, viewport, winlines):
    scrn.fill([0,0,0])
    winDisplay(pay)
    symbolLoad(viewport)
    winlineLoad(winlines)
    pygame.display.flip()
    pygame.time.wait(5000)



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
                gameLoop(main.baseSpin.baseEvents.basePay, main.baseSpin.baseEvents.baseViewport, main.baseSpin.baseEvents.baseActiveWinlines)
                pygame.display.flip()
                pygame.time.wait(5000)
                
                if(main.baseSpin.baseEvents.freeSpinFlag):
                    scrn.fill([0,0,0])
                    font = pygame.font.SysFont('freesanbold.ttf', 55)
                    winText = font.render('FREEGAMES!', True, (0, 255, 0))
                    textRect = winText.get_rect()
                    textRect.center = (200, 275)
                    scrn.blit(winText, textRect)
                    pygame.display.flip()
                    pygame.time.wait(5000)





pygame.quit()