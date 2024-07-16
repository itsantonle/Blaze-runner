from pygame.locals import *
from pygame import mixer
import pygame
import os
import sys
import math
import random


pygame.mixer.pre_init(44100,-16,2,512)
mixer.init()
pygame.init()

W, H = 800, 437  # sets the height of the window
win = pygame.display.set_mode((W, H))
pygame.display.set_caption('Blaze Scroller') #sets the name of the window
img_ico = pygame.image.load('icon.jpg')
pygame.display.set_icon(img_ico) #sets the icon of the window
bg = pygame.image.load(os.path.join('images', 'bg.png')).convert()
    #os.path gets the relative position of the folder of the image
#   two images so it never goes blank screen
bgX = 0  #the initial position of background
bgX2 = bg.get_width() #sets the position of bgx2 at the width of the bg image so it doesn't appear yet

clock = pygame.time.Clock()
#   used to track the amount of time- usually in miliseconds
#   it is required since we base the score of the time the user has surived without hitting obstacles
class StartMenu:
    def __init__(self):
        self.font = pygame.font.SysFont('comicsans', 40)
        self.start_button = pygame.Rect(300, 150, 200, 50)
        self.exit_button = pygame.Rect(300, 250, 200, 50)
        self.hover_sound = pygame.mixer.Sound("sounds/menu_hover.wav")
        self.click_sound = pygame.mixer.Sound("sounds/menu_click.wav")
        self.hover_sound_played = False
        self.hover_sound.set_volume(0.4)

        #   define the class init for the start menu sounds


    def draw(self):
        start_text = self.font.render('Play', True, (255, 255, 255))
        exit_text = self.font.render('Exit', True, (255, 255, 255))
        win.blit(start_text, (self.start_button.x + 50, self.start_button.y + 10))
        win.blit(exit_text, (self.exit_button.x + 50, self.exit_button.y + 10))

        #   draws the menu on the screen using the pygame win.blit
    def is_clicked(self, pos):
        return self.start_button.collidepoint(pos) or self.exit_button.collidepoint(pos)

        #   returns mouse position

    def play_hover_sound(self):
        if not self.hover_sound_played:
            self.hover_sound.play()
            self.hover_sound_played = True

        #   plays sound when mouse position is on top of button

    def play_click_sound(self):
        self.click_sound.play()

def start_menu():
    pygame.mixer.music.load("sounds/menu_bgm.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
    #   define volume and sound

    menu = StartMenu()
    clock = pygame.time.Clock()
    menu_bg = pygame.image.load("images/bg.png")
    #   define start menue, clock and bg menu

    while True:
        clock.tick(30)
        #clock and time management

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                #       quits the program
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu.is_clicked(pygame.mouse.get_pos()):
                    menu.play_click_sound() # at hover play sound
                    pygame.mixer.music.stop()
                    if menu.start_button.collidepoint(pygame.mouse.get_pos()):
                        return
                    elif menu.exit_button.collidepoint(pygame.mouse.get_pos()):
                        pygame.quit() # if it is on top of the exit button then quit
                        sys.exit()

        mouse_pos = pygame.mouse.get_pos()  #gets mouse position
        if menu.is_clicked(mouse_pos):
            menu.play_hover_sound()
            #will only play sound if hovered over
        else:
            menu.hover_sound_played = False

        win.blit(menu_bg,(0,0))
        menu.draw()
        pygame.display.flip()
        #display.flip updates the entire screen instead of an object or portion
        # slightly synonymous to display.update() with empty parameters so th eentire screen updates
        # cannot be used for OpenGL displays unlike display.flip()
#calls for start menu
start_menu()
# the animations work by getting setting x in terms of ranges and converting it to string
# to access the name of the file with the extension .png using list comprehension and str(int)
# run and jump use ranges but slide and fall animations are manually inputted
class player(object):
    run = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(8, 16)]
    jump = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(1, 8)]
    slide = [pygame.image.load(os.path.join('images', 'S1.png')), pygame.image.load(os.path.join('images', 'S2.png')),
             pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')),
             pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')),
             pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')),
             pygame.image.load(os.path.join('images', 'S3.png')), pygame.image.load(os.path.join('images', 'S4.png')),
             pygame.image.load(os.path.join('images', 'S5.png'))]

    fall = pygame.image.load(os.path.join('images', '0.png'))
    #fall means the death of the character ig?

    #this basically just deals with the sequence of the jump animation
    jumpList = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4,
                4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1,
                -1, -1, -1, -1, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3,
                -3, -3, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4]

#   defines the init function or the initialization func
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.sliding = False
        self.falling = False
        self.slideCount = 0
        self.jumpCount = 0
        self.runCount = 0
        self.slideUp = False

    def draw(self, win):
        #draws on the screen using the convenient pygame blit method
        #self.falling is set to False, but if true will blit the falling animation on the coordinates provided

        if self.falling:
            win.blit(self.fall, (self.x, self.y + 30)) # going down

        elif self.jumping: #jumping hitbox change
            self.y -= self.jumpList[self.jumpCount] * 1.3 # assign the y coordinate based on jumplist
            win.blit(self.jump[self.jumpCount // 18], (self.x, self.y))  #blits coordinate on every 18 frames
            self.jumpCount += 1
            if self.jumpCount > 108:  #jump count is 108 max then resets 6 images, 18 frames
                # take note this is bcuz len(jumplist == 109)
                self.jumpCount = 0
                self.jumping = False  #after the jump count exceeds 108, resume running
                self.runCount = 0
            self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 10)  #the hitbox for jump
        elif self.sliding or self.slideUp: #sliding hitbox change
            if self.slideCount < 20: #you sliding down fr
                self.y += 1
                self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 10)
            elif self.slideCount == 80: #   once 80 over you go up sliding is g so u go up
                self.y -= 19
                self.sliding = False
                self.slideUp = True
            elif self.slideCount > 20 and self.slideCount < 80: #middle slide, the character is lying down
                self.hitbox = (self.x, self.y + 3, self.width - 8, self.height - 35)
                #lying down hitbox

            if self.slideCount >= 110:
                self.slideCount = 0
                self.runCount = 0
                self.slideUp = False
                self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 10)
            win.blit(self.slide[self.slideCount // 10], (self.x, self.y))
            self.slideCount += 1
            # when we about to stand up and run again fr

        else:
            if self.runCount > 42:
                self.runCount = 0
            win.blit(self.run[self.runCount // 6], (self.x, self.y))
            self.runCount += 1
            self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 13)

        # pygame.draw.rect(win, (255,0,0),self.hitbox, 2)


class saw(object):  # animation for the saw
    rotate = [pygame.image.load(os.path.join('images', 'SAW0.PNG')),
              pygame.image.load(os.path.join('images', 'SAW1.PNG')),
              pygame.image.load(os.path.join('images', 'SAW2.PNG')),
              pygame.image.load(os.path.join('images', 'SAW3.PNG'))]

    #list for the images animation of the saw animation

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotateCount = 0
        self.vel = 1.4

    def draw(self, win):
        self.hitbox = (self.x + 10, self.y + 5, self.width - 20, self.height - 5)
        # pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        # note that the hitbox is basically relative to the x and y coordinate of the object
        if self.rotateCount >= 8:  #restart count to 0
            self.rotateCount = 0
        win.blit(pygame.transform.scale(self.rotate[self.rotateCount // 2], (64, 64)), (self.x, self.y))
        # uses integer division to blit  image on the screen at rotate count increases, every 2 frames, draw 1 frame of
        # use 8 cuz there was 4 so 4 x 2 = 8

        self.rotateCount += 1

    def collide(self, rect): #deals with the collision even
        #rect refers to the rectangle hitbox we create loll (character)
        #self.hitbox refers tot he hitbox of the object
        # rect = [x, y, width, height]
        # rect[0] = x position of hitbox
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            #checks if x coordinates overlap
            if rect[1] + rect[3] > self.hitbox[1]:
                #checks if y coordinates overlap
                return True
        return False


class spike(saw): # parent class is saw, means inherit init from saw
    img = pygame.image.load(os.path.join('images', 'spike.png')) #defines the img of spike

    def draw(self, win):
        self.hitbox = (self.x + 10, self.y, 28, 315)
        # hitbox is relative to the position of self.x and self.y which the y and x coordinate of the object
        # pygame.draw.rect(win, (255,0,0), self.hitbox, 2) (this comment is the visual representation of the hitbox)
        # if you want to visualize the hitbox uncomment
        win.blit(self.img, (self.x, self.y))  #blits img, on x and y
    def collide(self, rect):
        # rect refers to the rectangle hitbox we create loll (character)
        # self.hitbox refers to the hitbox of the object
        # rect = [x, y, width, height]
        # rect[0] = x position of hitbox
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            #checks if x coordinates overlap
            if rect[1] < self.hitbox[3]:
                #checks if y coordinates overlap
                return True
        return False


def updateFile(): # file handling of scores
    f = open('scores.txt', 'r')
    # the second parameter, 'r' means we're reading it
    file = f.readlines()
    last = int(file[0])
    #since it's a string we need to convert it to int, it won't work tho if the file
    # is empty a

    if last < int(score):
        f.close()
        file = open('scores.txt', 'w')
        file.write(str(score))
        file.close()
        #compares the last or the lines inside txt file with score
        # if score larger than the date in scores.txt rewrite and chane to score

        return score

    return last

#function for the bgm
def play_bgm():
    pygame.mixer.music.load("sounds/main_ingame_bgm.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

#function for the end screen
def play_end_screen_music():
    pygame.mixer.music.load("sounds/death_audio_screen.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play()

def endScreen():
    #variables are set to global so we can acess them in the endScreen()
    global pause, score, speed, obstacles
    pygame.mixer.music.stop()
    #stops previous music
    play_end_screen_music()
    #plays the end music
    pause = 0
    speed = 30

    #resets default stuff
    obstacles = []

    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
                runner.falling = False
                runner.sliding = False
                runner.jumping = False
        #blits the bg
        win.blit(bg, (0, 0))
        largeFont = pygame.font.SysFont('comicsans', 80)
        lastScore = largeFont.render('Best Score: ' + str(updateFile()), 1, (255, 255, 255))
        currentScore = largeFont.render('Score: ' + str(score), 1, (255, 255, 255))
        win.blit(lastScore, (W / 2 - lastScore.get_width() / 2, 150))
        win.blit(currentScore, (W / 2 - currentScore.get_width() / 2, 240))
        #all of this just deals with the text on the screen
        pygame.display.update()
    score = 0
    runner.falling = False


def redrawWindow():
    largeFont = pygame.font.SysFont('comicsans', 20)  #this is basically just to create a text with the
    #attributes that we listed here.
    win.blit(bg, (bgX, 0))
    win.blit(bg, (bgX2, 0))
    text = largeFont.render('Score: ' + str(score), 1, (255, 255, 255))
    runner.draw(win)
    # draws the runner in the window named win

    for obstacle in obstacles:
        # draws the obstacle from the list
        obstacle.draw(win)

    win.blit(text, (700, 10))
    pygame.display.update()


pygame.time.set_timer(USEREVENT + 1, 500) #rate of increase of player spped, use a timer event
#user event triggers true at every 500 mili
pygame.time.set_timer(USEREVENT + 2, 5000) #rate of appearance of obstacles
speed = 30 #default speed of the player

score = 0

run = True  # to initialize the screen
runner = player(200, 313, 64, 64)  #this is the player 64x64 sprite, 313 ground level
#x and y based on the size of the png

obstacles = []
# creates variables pause and fall speed to handle the delay to move on to endscreen()
pause = 0
fallSpeed = 0
play_bgm()
#calls for the bgm()

while run:
    if pause > 0:  # if you have collided with an object pause = 1 then increment
        # the fall speed is the speed of the object when death
        # at instance pause is greater than fallspeed *2 move on to the endscreen
        pause += 1
        if pause > fallSpeed * 2:
            endScreen()

    score = speed // 10 - 3  # the score increases on how long the player runs
    #take not the score is relative to the speed
    # speed is 30 so 30// 10 - 3 = 0

    for obstacle in obstacles:
        if obstacle.collide(runner.hitbox):  #if the obstacle hitbox overlaps with the runner then
            #proceed to falling or dead animation
            runner.falling = True

            if pause == 0:  #means you haven't collided it yet
                pause = 1
                fallSpeed = speed
        if obstacle.x < -64:
            obstacles.pop(obstacles.index(obstacle))
            # if you cant see the object anymore, you can remove the object using the index
            # list.pop(index) - takes integer value
            # index = list.index(obj)- find the index of the value
        else:
            obstacle.x -= 1.4   #moves the x coordinate of the obstacles to the left so it looks natural

    bgX -= 1.4  #infinte scroll background, the bgX moves to the left from 0
    bgX2 -= 1.4 #after bgx comes bgx2, then reverts back into a lopp

    if bgX < bg.get_width() * -1: #from negative to positive
        bgX = bg.get_width()
    if bgX2 < bg.get_width() * -1: #object is behidn bgx to replae it ASAP
        bgX2 = bg.get_width()

#scrolls through the events within the window
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            sys.exit()

        if event.type == USEREVENT + 1:
            speed += 1  #every 500 mili  + 1 speed

        if event.type == USEREVENT + 2:
            r = random.randrange(0, 2) # you do rand range to make obj appear
            # a rand range between 1 or 0 will make either saw or spike appear
            if r == 0:
                obstacles.append(saw(810, 310, 64, 64))
                # x, y, width, height 64 x 64, make at the right screen with positive x, y positive is going down
            elif r == 1:
                obstacles.append(spike(810, 0, 48, 310))

    if runner.falling == False:
        # if not dead then running and you can press keys
        keys = pygame.key.get_pressed()
        #basically you just use a shortcut by seeting pygame.key.get_pressed() to a variable

        if keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]:
            if not (runner.jumping):  #if the player is not already jumping, then jump
                runner.jumping = True

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            if not (runner.sliding): #if not already sliding then slide
                runner.sliding = True

    clock.tick(speed)
    # the clock uses the players speed to advance, the player speed increases the clock increases
    redrawWindow()
    #calls function redrawwindow