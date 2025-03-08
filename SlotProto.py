import pygame
from BasicSlot import *
from SlotData import *

class SlotGame:
    def __init__(self, config, path, symbolMap, winlineMap, screen_size):
        pygame.init()
        self.config = config
        self.path = path
        self.symbolMap = symbolMap
        self.winlineMap = winlineMap
        self.scrn = pygame.display.set_mode(screen_size)
        self.status = True

        self.baseEvents = []
        self.freeEvents = []
        self.totalFreeGamePay = 0

    def symbolLoad(self, viewport):
        for x, view in enumerate(viewport):
            for y, sym in enumerate(view):
                self.scrn.blit(pygame.image.load(self.path + "symbols/" + self.symbolMap[sym] + ".png").convert(), (x * 150, y * 150))

    def winlineLoad(self, activeWinlines):
        for x, winline in enumerate(activeWinlines):
            if winline <= 2:
                pygame.draw.line(self.scrn, (0, 255, 0), (75, 75 + 150 * winline), (675, 75 + 150 * winline), width=4)
            if winline == 3:
                pygame.draw.line(self.scrn, (0, 255, 0), (75, 75), (375, 375), width=6)
                pygame.draw.line(self.scrn, (0, 255, 0), (375, 375), (675, 75), width=6)
            if winline == 4:
                pygame.draw.line(self.scrn, (0, 255, 0), (75, 375), (375, 75), width=6)
                pygame.draw.line(self.scrn, (0, 255, 0), (375, 75), (675, 375), width=6)

    def winDisplay(self, win, freeGame, spinCount):
        font = pygame.font.SysFont('freesanbold.ttf', 25)
        if freeGame:
            winText = font.render('Total FREE Win = £' + str(win) + " Spin Count : " + str(spinCount) + "/5", True, (0, 255, 0))
        else:
            winText = font.render('Total Win = £' + str(win), True, (0, 255, 0))
        textRect = winText.get_rect()
        textRect.center = (200, 475)
        self.scrn.blit(winText, textRect)

    def eventRequest(self):
        main = MainGame(1, self.config)
        main.spin()
        self.baseEvents = main.baseSpin.baseEvents
        self.freeEvents = main.freeSpin.freeEvents

    def freegameSplash(self):
        self.scrn.fill([0, 0, 0])
        font = pygame.font.SysFont('freesanbold.ttf', 55)
        winText = font.render('FREEGAMES!', True, (0, 255, 0))
        textRect = winText.get_rect()
        textRect.center = (200, 275)
        self.scrn.blit(winText, textRect)
        pygame.display.flip()
        pygame.time.wait(800)

    def basegameLoop(self):
        self.scrn.fill([0, 0, 0])
        self.symbolLoad(self.baseEvents.baseViewport)
        self.winlineLoad(self.baseEvents.baseActiveWinlines)
        self.winDisplay(self.baseEvents.basePay, False, 0)
        pygame.display.flip()
        pygame.time.wait(3000)

    def freegameLoop(self, freeSpinNum):
        self.scrn.fill([0, 0, 0])
        self.symbolLoad(self.freeEvents.freeViewport[freeSpinNum])
        self.winlineLoad(self.freeEvents.freeActiveWinlines[freeSpinNum])
        self.winDisplay(self.totalFreeGamePay, True, freeSpinNum + 1)
        pygame.display.flip()
        pygame.time.wait(3000)

    def spin(self):
        self.scrn.fill([0, 0, 0])
        self.eventRequest()
        self.basegameLoop()
        pygame.time.wait(800)
        
        if self.baseEvents.freeSpinFlag:
            self.freegameSplash()
            for i in range(int(main.slotData.freeSpinCount[1])):
                self.totalFreeGamePay += self.freeEvents.freePay[i]
                self.freegameLoop(i)
            self.totalFreeGamePay = 0

    def run(self):
        while self.status:
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    self.status = False
                if i.type == pygame.KEYDOWN:
                    if i.key == pygame.K_SPACE:
                        self.spin()

        pygame.quit()


if __name__ == "__main__":
    config = "/Users/connorkelly/Documents/Work/Project-GAME000/BasicSlot.xlsx"
    path = "/Users/connorkelly/Documents/Work/Project-GAME000/"
    symbolMap = ["Wild", "R1", "R2", "Y1", "Y2", "B1", "B2", "G1", "G2", "G3", "Scatter"]
    winlineMap = [(75, 75), (75, 225), (75, 375), (75, 75), (75, 75)]
    screen_size = (750, 500)

    game = SlotGame(config, path, symbolMap, winlineMap, screen_size)
    game.run()