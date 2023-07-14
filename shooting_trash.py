import pygame
import sys
import random
from time import sleep

BLACK = (0, 0, 0)
screen_Width = 480
screen_Height = 640
TrashImage = ['C:/Users/서동혁/Desktop/동아리/trash.png', 'C:/Users/서동혁/Desktop/동아리/food1.png']
def writeMessage(text):
    global Screen
    textfont = pygame.font.Font('LilitaOne-Regular.ttf', 80)
    text = textfont.render(text, True, (0, 0, 0))
    textpos = text.get_rect()
    textpos.center = (screen_Width / 2, screen_Height / 2)
    Screen.blit(text, textpos)
    pygame.display.update()
    sleep(2)
    runGame()

def crash():
    global Screen
    writeMessage('GAMEOVER')

def GameOver():
    global Screen
    writeMessage('GAMEOVER')

def drawObject(obj, x, y):
    global Screen
    Screen.blit(obj, (x,y))

def writeScore(count):
    global Screen
    font = pygame.font.Font('NanumGothic.ttf', 20)
    text = font.render('파괴한 쓰레기 수 : ' + str(count), True, (0,0,0))
    Screen.blit(text, (10, 5))

def writePassed(count):
    global Screen
    font = pygame.font.Font('NanumGothic.ttf', 20)
    text = font.render('놓친 쓰레기 수 : ' + str(count), True, (0,0,0))
    Screen.blit(text, (310, 5))

def initGame():
    global Screen, clock, background, character, missile, explosion
    pygame.init()
    Screen = pygame.display.set_mode((screen_Width, screen_Height))
    pygame.display.set_caption('shooting')
    background = pygame.image.load('C:/Users/서동혁/Desktop/동아리/background.png')
    character = pygame.image.load('C:/Users/서동혁/Desktop/동아리/character.png')
    missile = pygame.image.load('C:/Users/서동혁/Desktop/동아리/weapon.png')
    explosion = pygame.image.load('C:/Users/서동혁/Desktop/동아리/bomb.png')
    clock = pygame.time.Clock()

def runGame():
    global Screen, clock, background, character, missile, explosion

    missileXY = []

    Trash = pygame.image.load(random.choice(TrashImage))
    TrashSize = Trash.get_rect().size
    TrashWidth = TrashSize[0]
    TrashHeight = TrashSize[1]

    TrashX = random.randrange(0, screen_Width - TrashWidth)
    TrashY = 0
    TrashSpeed = 2

    character_Size = character.get_rect().size
    character_Width = character_Size[0]
    character_Height = character_Size[1]

    x = screen_Width * 0.45
    y = screen_Height * 0.9
    characterX = 0

    isShot = False
    shotCount = 0
    TrashPassed = 0

    running = False
    while not running:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:
                pygame.quit()
                sys.exit()

            if event.type in [pygame.KEYDOWN]:
                if event.key == pygame.K_LEFT:
                    characterX -= 5

                elif event.key == pygame.K_RIGHT:
                    characterX += 5

                elif event.key == pygame.K_SPACE:
                    missileX = x + character_Width / 2
                    missileY = y - character_Height
                    missileXY.append([missileX, missileY])

                elif event.key == pygame.K_p:
                    pygame.time.delay(10000)

            if event.type in [pygame.KEYUP]:
                if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                    characterX = 0

        drawObject(background, 0, 0)

        x += characterX
        if x < 0:
            x = 0
        elif x > screen_Width - character_Width:
            x = screen_Width - character_Width

        if y < TrashY + TrashHeight:
            if (TrashX > x and TrashX < x + character_Width) or (TrashX +TrashWidth > x and TrashX + TrashWidth < x + character_Width):
                drawObject(explosion, x, y)
                crash()

        drawObject(character, x, y)

        if len(missileXY) != 0:
            for i, bxy in enumerate(missileXY):
                bxy[1] -= 10
                missileXY[i][1] = bxy[1]

                if bxy[1] < TrashY:
                    if bxy[0] > TrashX and bxy[0] < TrashX + TrashWidth:
                        missileXY.remove(bxy)
                        isShot = True
                        shotCount += 1

                if bxy[1] <= 0:
                    try:
                        missileXY.remove(bxy)
                    except:
                        pass

        if len(missileXY) != 0:
            for bx, by in missileXY:
                drawObject(missile, bx, by)

        writeScore(shotCount)

        TrashY += TrashSpeed

        if TrashY > screen_Height:
            Trash = pygame.image.load(random.choice(TrashImage))
            TrashSize = Trash.get_rect().size
            TrashWidth = TrashSize[0]
            TrashHeight = TrashSize[1]
            TrashX = random.randrange(0, screen_Width - TrashWidth)
            TrashY = 0
            TrashPassed += 1

        if TrashPassed == 3:
            GameOver()

        writePassed(TrashPassed)

        if isShot:

            Trash = pygame.image.load(random.choice(TrashImage))
            TrashSize = Trash.get_rect().size
            TrashWidth = TrashSize[0]
            TrashHeight = TrashSize[1]
            TrashX = random.randrange(0, screen_Width - TrashWidth)
            TrashY = 0
            isShot = False

            TrashSpeed += 0.1
            if TrashSpeed >= 30:
                TrashSpeed = 30

        drawObject(Trash, TrashX, TrashY)

        pygame.display.update()

        clock.tick(60)

    pygame.quit()

initGame()
runGame()












