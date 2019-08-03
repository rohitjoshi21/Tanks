import pygame as pg
from pygame.locals import *

pg.init()

FULL_SCREEN = True

#COLORS
bgcolor = (204, 221, 255)
white = (255,255,255)
gray = (100,100,100)
black = (0,0,0)
blue = (0,0,255)
red = (200,0,0)
light_red = (255,0,0)
yellow = (200,200,0)
light_yellow = (255,255,0)
green = (34,177,76)
light_green = (0,255,0)
wheelColor = (100,100,100)
groundColor = pg.Color(10,10,255,10)
    
#DISPLAY_WINDOW

if FULL_SCREEN == True:
    screen = pg.display.set_mode((0,0),FULLSCREEN)
    groundHeight = 60
    dWidth,dHeight = pg.display.Info().current_w,pg.display.Info().current_h

else:
    dWidth = 800
    dHeight = 600
    groundHeight = 50
    screen = pg.display.set_mode((dWidth,dHeight))



pg.display.set_caption('Battle Tanks')

#Sounds
SOUND = True
try:
    pg.mixer.init()
except:
    SOUND = False
    print("No sound device found")

if SOUND:
    boom_sound = pg.mixer.Sound("Sounds/boom.wav")
    boom_sound.set_volume(0.1)
    gameover_sound = pg.mixer.Sound("Sounds/gameover.wav")
    shot_sound = pg.mixer.Sound("Sounds/firecracker.wav")
    ##pg.mixer.music.load("Sounds/ingame.it")
    ##pg.mixer.music.play(-1)
def playSound(sound_name):
    if SOUND:
        pg.mixer.Sound.play(sound_name)

#Images        
images = {}
images['bg'] = {}
images['bg']['intro'] = pg.image.load("Photos/tank.jpg")
images['bg']['main'] = pg.image.load("Photos/cover.jpeg")

for name,image in zip(images['bg'].keys(),images['bg'].values()):
    images['bg'][name] = pg.transform.scale(image, (dWidth,dHeight))
    
images['boom'] = pg.image.load("Photos/bang1.png")

image = pg.image.load('Photos/cloud.png')
images['cloud'] = pg.transform.scale(image,(int(dWidth/5),int(dHeight/5)))
                                     



clock = pg.time.Clock()

#Game_data
gHeight = groundHeight
tankWidth = 40
tankHeight = 20
turretWidth = 3
turretLength = 25
wheelWidth = 4
barrierWidth = 50
maxPower = 100
maxHealth = 100
barrierHealth = 100
gravity = 6
bombRadius = 4

#FONT_SIZES
small = 25
mid = 45
smallFont = 25
midFont = 45
large = 75

#CLOCK
FPS = 60

def limit(minval,currval,maxval):
    if currval < minval:
        currval = minval
    elif currval > maxval:
        currval = maxval

    return currval
        
