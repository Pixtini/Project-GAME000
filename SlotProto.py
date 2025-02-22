import pygame
from BasicSlot import *
from SlotData import *

pygame.init()
X = 750
Y = 500
config = "/Users/connorkelly/Documents/Work/Project-GAME000/BasicSlot.xlsx"
path = "/Users/connorkelly/Documents/Work/Project-GAME000/symbols/"
symbolMap = ["Wild", "R1","R2","Y1","Y2","B1","B2","G1","G2","G3","Scatter"]
scrn = pygame.display.set_mode((X, Y))

def symbolLoad(viewport):
    for x, view in enumerate(viewport):
        for y, sym in enumerate(view):
            scrn.blit(pygame.image.load(path+symbolMap[sym]+".png").convert(), (x*150, y*150))

def winDisplay(win):
    font = pygame.font.SysFont('freesanbold.ttf', 25)
    winText = font.render('Total Win = £' + str(win), True, (0, 255, 0))
    textRect = winText.get_rect()
    textRect.center = (100, 475)
    scrn.blit(winText, textRect)

status = True
while (status):
    for i in pygame.event.get():

        if i.type == pygame.QUIT:
            status = False

        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_SPACE:
                
                scrn.fill([0,0,0])
                main = MainGame(1, config)
                eventData = main.spin()
                winDisplay(eventData[0])
                symbolLoad(eventData[1])
                pygame.display.flip()


pygame.quit()