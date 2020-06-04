import pygame
import sys
import random
import string
import time

# ----------------------------------------------------#
# Initialize global variables#
# ----------------------------------------------------#
pygame.init()

size = width, height = 900, 600
screen = pygame.display.set_mode(size)

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

lines = []
buttons = []
buttonsImg = []
drawTick = []
rightGuesses = []
drawX = []
# Track big word
drawWord = []
spaceOut = []

lives = 10
timing = 120

# Create a list of Uppercase alphabet
alphabetString = string.ascii_uppercase
alphabet = list(alphabetString)

wordFont = pygame.font.Font('freesansbold.ttf', 15)
livesFont = pygame.font.Font('freesansbold.ttf', 25)
clockFont = pygame.font.Font('freesansbold.ttf', 20)
bigFont = pygame.font.Font('freesansbold.ttf', 40)
endFont = pygame.font.Font('freesansbold.ttf', 30)
winLoseFont = pygame.font.Font('freesansbold.ttf', 50)
gameNameFont = pygame.font.Font('freesansbold.ttf', 90)
nameFont = pygame.font.Font('freesansbold.ttf', 10)

hangman1 = pygame.image.load('hangPic1.png')
hangman2 = pygame.image.load('hangPic2.png')
hangman3 = pygame.image.load('hangPic3.png')
hangman4 = pygame.image.load('hangPic4.png')
hangman5 = pygame.image.load('hangPic5.png')
hangman6 = pygame.image.load('hangPic6.png')
hangman7 = pygame.image.load('hangPic7.png')
hangManPic = [hangman1, hangman2, hangman3, hangman4, hangman5, hangman6, hangman7]

tickImg = pygame.image.load('tick.png')
XImg = pygame.image.load('cross.png')

clock = pygame.time.Clock()
FPS = 10

# Initialize clock and lives
def loseCon():
    global lives, timing
    timing -= 0.1
    timing = round(timing, 1)
    livesShow = livesFont.render("Lives: ", True, BLACK)
    timeShow = clockFont.render("Time: ", True, BLACK)

    if timing <= 50:
        timeNum = clockFont.render(str(timing), True, RED)
    else:
        timeNum = clockFont.render(str(timing), True, GREEN)

    if lives >= 7:
        num = livesFont.render(str(lives), True, GREEN)
    elif lives >= 4:
        num = livesFont.render(str(lives), True, YELLOW)
    else:
        num = livesFont.render(str(lives), True, RED)
 
    screen.blit(livesShow, [765, 280])
    screen.blit(num, [850, 280])

    screen.blit(timeShow, [765, 350])
    screen.blit(timeNum, [836, 350])


def hangMan(lis):
    global lives
    index = 0

    if lives == 6:
        index = 1
    elif lives == 5:
        index = 2
    elif lives == 4:
        index = 3
    elif lives == 3:
        index = 4
    elif lives == 2:
        index = 5
    elif lives == 1:
        index = 6

    screen.blit(lis[index], (50, 200))



def word():
    with open('wordList.txt', 'r') as file:
        wordsList = file.readlines()
        ranNum = random.randrange(0, len(wordsList) - 1)
    return wordsList[ranNum]


def centerLine(start, des):
    lineLength = des - start
    angleLength = (width - lineLength) / 2

    return angleLength


def drawLines():
    wordLength = len(randomWord)
    start = 30
    destination = 30 + (50 * wordLength)

    center = centerLine(start, destination)

    # I have no clue how this work, just trying to center those lines depends on the length of the word
    x = int(center) + 38
    y = 550

    xDes = x + 30

    for i in range(wordLength - 1):
        pygame.draw.lines(screen, BLACK, False, [(x, y), (xDes, y)], 5)
        lines.append([x, y])
        x += 50
        xDes += 50


def duplicate(search, lis):
    pos = 0
    positions = []

    while search in lis:
        pos += lis.index(search)
        positions.append(pos)
        lis = lis[lis.index(search) + 1:]
        pos += 1
    return positions


def drawButtons():
    x = 150
    x2 = 150
    halfAlphabet = int(26 / 2)
    maxLength = x + 50 * 13

    for i in range(halfAlphabet):
        buttonsImg.append(pygame.draw.circle(screen, GREEN, [x, 50], 20))
        buttons.append([x, 50])
        x += 50

        if x >= maxLength:
            for j in range(halfAlphabet):
                buttonsImg.append(pygame.draw.circle(screen, GREEN, [x2, 100], 20))
                buttons.append([x2, 100])
                x2 += 50


def drawAlphabet():
    global alphabet, buttons
    for i in range(len(alphabet)):
        letter = wordFont.render(alphabet[i], True, BLACK)
        # Center the letters into the circle
        screen.blit(letter, (buttons[i][0] - 5, buttons[i][1] - 5))


def buttonHit(x, y):
    for i, _ in enumerate(buttons):
        if buttons[i][0] + 20 > x > buttons[i][0] - 20:
            if buttons[i][1] + 20 > y > buttons[i][1] - 20:
                return True, i
    return False, None


def split(word):
    return [char for char in word]


def guessed(letter, word):
    global lives

    if letter.lower() in word:
        return True
    else:
        lives -= 1

    return False


def win(word, right):
    if len(word) == len(right) + 1:
        return True
    return False


def endText(win):
    global width, height, randomWord

    halfW, halfH = width / 2 - 200, height / 2

    lostTxt = "You Lost"
    winTxt = "You Win"

    againTxt = "Press any key to play again"
    againTxt2 = winLoseFont.render(againTxt, True, GREEN)

    wordWas = "The word was: " + randomWord.strip()
    if win:
        text = winLoseFont.render(winTxt, True, BLACK)
    else:
        text = winLoseFont.render(lostTxt, True, BLACK)
        wordWas2 = endFont.render(wordWas, True, BLACK)
        screen.blit(wordWas2, (round(halfW + 50), round(halfH)))

    screen.blit(text, (round(halfW + 120), round(halfH - 100)))
    screen.blit(againTxt2, (round(halfW - 100), round(halfH + 80)))

    pygame.display.update()
    again = True
    while again:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                again = False
    restart()


def restart():
    global lives, wordList, wordListClone, drawX, drawTick, drawWord, randomWord, timing, lines, rightGuesses
    drawTick = []
    drawX = []
    # Track big word
    drawWord = []
    lines = []
    rightGuesses = []
    lives = 10
    timing = 180
    randomWord = word()
    wordList = wordListClone
    wordList = split(randomWord)


randomWord = word()
wordList = split(randomWord)
wordListClone = wordList

def nonDupList(lis):
    return list(dict.fromkeys(lis))

def draw(lis):
    for i in range(len(lis)):
        screen.blit(lis[i][0], lis[i][1])


def mainGame():
    global lives, wordListClone, rightGuesses, randomWord, wordList
    gameRun = True

    while gameRun:
        clock.tick(FPS)
        screen.fill(WHITE)

        drawLines()
        drawButtons()
        drawAlphabet()
        hangMan(hangManPic)
        loseCon()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x = event.pos[0]
                y = event.pos[1]

                i = buttonHit(x, y)[1]

                if buttonHit(x, y)[0]:
                    if guessed(alphabet[i], wordList):
                        drawTick.append([tickImg, [buttons[i][0], buttons[i][1]]])
                        indexes = duplicate(alphabet[i].lower(), wordList)
                        spaceOut.append(buttons[i][1] - 100)

                        for x in indexes:
                            right = bigFont.render(wordList[x], True, BLACK)
                            drawWord.append([right, (lines[x][0], lines[x][1] - 50)])
                            rightGuesses.append(i)

                    else:
                        drawX.append([XImg, [buttons[i][0], buttons[i][1]]])

        wordListClone = nonDupList(wordListClone)
        rightGuesses = nonDupList(rightGuesses)
        
        draw(drawX)
        draw(drawWord)
        draw(drawTick)

        if win(wordListClone, rightGuesses):
            endText(True)
            wordList = split(randomWord)
            wordListClone = wordList

        if lives == 0 or timing == 0:
            time.sleep(0.2)
        
            endText(False)
            wordList = split(randomWord)
            wordListClone = wordList

        pygame.display.update()


def start():
    global width, height

    pygame.display.set_caption('Hang man')
    halfW, halfH = width / 2 - 200, height / 2
    screen.fill(GREEN)

    gameName = "HANG MAN"
    text = "Press any key to start"
    name = "@Made by Mark"

    game = gameNameFont.render(gameName, True, WHITE)
    screen.blit(game, (220, 50))

    start = bigFont.render(text, True, WHITE)
    screen.blit(start, (round(halfW), round(halfH - 30)))

    myName = nameFont.render(name, True, BLACK)
    screen.blit(myName, (round(halfW + 180), round(halfH + 30)))
    pygame.display.update()

    play = True
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                mainGame()
                play = False


start()
pygame.quit()