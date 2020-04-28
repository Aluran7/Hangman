
## File Name: hangman.py                               ##
## Description: Starter for Hangman project - ICS3U    ##
#########################################################
import random
import pygame


pygame.init()
WINHEIGHT = 480
WINWIDTH = 700
win=pygame.display.set_mode((WINWIDTH, WINHEIGHT))
#---------------------------------------#
# initialize global variables/constants #
#---------------------------------------#
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (102, 255, 255)

BTN_FONT = pygame.font.SysFont("arial", 20)
GUESS_FONT = pygame.font.SysFont("monospace", 24)
LOST_FONT = pygame.font.SysFont('arial', 45)
WORD = ''
BUTTONS = []
GUESSED = []
HANGMANPICS = [pygame.image.load('hangman0.png'), pygame.image.load('hangman1.png'), pygame.image.load('hangman2.png'), pygame.image.load('hangman3.png'), pygame.image.load('hangman4.png'), pygame.image.load('hangman5.png'), pygame.image.load('hangman6.png')]

LIMBS = 0


def redraw_game_window():
    global GUESSED
    global HANGMANPICS
    global LIMBS
    win.fill(BLUE)
    # BUTTONS
    for i in range(len(BUTTONS)):
        if BUTTONS[i][4]:
            pygame.draw.circle(win, BLACK, (BUTTONS[i][1], BUTTONS[i][2]), BUTTONS[i][3])
            pygame.draw.circle(win, BUTTONS[i][0], (BUTTONS[i][1], BUTTONS[i][2]), BUTTONS[i][3] - 2
                               )
            label = BTN_FONT.render(chr(BUTTONS[i][5]), 1, BLACK)
            win.blit(label, (BUTTONS[i][1] - (label.get_width() / 2), BUTTONS[i][2] - (label.get_height() / 2)))

    spaced = spacedOut(WORD, GUESSED)
    label1 = GUESS_FONT.render(spaced, 1, BLACK)
    rect = label1.get_rect()
    length = rect[2]

    win.blit(label1, (WINWIDTH/2 - length/2, 400))

    pic = HANGMANPICS[LIMBS]
    win.blit(pic, (WINWIDTH/2 - pic.get_width()/2 + 20, 150))
    pygame.display.update()


def randomWORD():
    file = open('WORDs.txt')
    f = file.readlines()
    i = random.randrange(0, len(f) - 1)

    return f[i][:-1]


def hang(guess):
    global WORD
    if guess.lower() not in WORD.lower():
        return True
    else:
        return False


def spacedOut(WORD, GUESSED=[]):
    spacedWORD = ''
    GUESSEDLetters = GUESSED
    for x in range(len(WORD)):
        if WORD[x] != ' ':
            spacedWORD += '_ '
            for i in range(len(GUESSEDLetters)):
                if WORD[x].upper() == GUESSEDLetters[i]:
                    spacedWORD = spacedWORD[:-2]
                    spacedWORD += WORD[x].upper() + ' '
        elif WORD[x] == ' ':
            spacedWORD += ' '
    return spacedWORD
            

def buttonHit(x, y):
    for i in range(len(BUTTONS)):
        if x < BUTTONS[i][1] + 20 and x > BUTTONS[i][1] - 20:
            if y < BUTTONS[i][2] + 20 and y > BUTTONS[i][2] - 20:
                return BUTTONS[i][5]
    return None


def end(winner=False):
    global LIMBS
    lostTxt = 'You Lost, press any key to play again...'
    winTxt = 'WINNER!, press any key to play again...'
    redraw_game_window()
    pygame.time.delay(1000)
    win.fill(GREEN)

    if winner == True:
        label = LOST_FONT.render(winTxt, 1, BLACK)
    else:
        label = LOST_FONT.render(lostTxt, 1, BLACK)

    WORDTxt = LOST_FONT.render(WORD.upper(), 1, BLACK)
    WORDWas = LOST_FONT.render('The phrase was: ', 1, BLACK)

    win.blit(WORDTxt, (WINWIDTH/2 - WORDTxt.get_width()/2, 295))
    win.blit(WORDWas, (WINWIDTH/2 - WORDWas.get_width()/2, 245))
    win.blit(label, (WINWIDTH / 2 - label.get_width() / 2, 140))
    pygame.display.update()
    again = True
    while again:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                again = False
    reset()


def reset():
    global LIMBS
    global GUESSED
    global BUTTONS
    global WORD
    for i in range(len(BUTTONS)):
        BUTTONS[i][4] = True

    LIMBS = 0
    GUESSED = []
    WORD = randomWORD()

#MAINLINE


# Setup BUTTONS
increase = round(WINWIDTH / 13)
for i in range(26):
    if i < 13:
        y = 40
        x = 25 + (increase * i)
    else:
        x = 25 + (increase * (i - 13))
        y = 85
    BUTTONS.append([WHITE, x, y, 20, True, 65 + i])
    # BUTTONS.append([color, x_pos, y_pos, radius, visible, char])

WORD = randomWORD()
inPlay = True

while inPlay:
    redraw_game_window()
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                inPlay = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clickPos = pygame.mouse.get_pos()
            letter = buttonHit(clickPos[0], clickPos[1])
            if letter != None:
                GUESSED.append(chr(letter))
                BUTTONS[letter - 65][4] = False
                if hang(chr(letter)):
                    if LIMBS != 5:
                        LIMBS += 1
                    else:
                        end()
                else:
                    print(spacedOut(WORD, GUESSED))
                    if spacedOut(WORD, GUESSED).count('_') == 0:
                        end(True)

pygame.quit()

# always quit pygame when done!
