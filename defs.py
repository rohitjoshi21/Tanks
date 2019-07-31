import pygame as pg
from pygame.locals import *
pg.init()

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

#DISPLAY_WINDOW
dWidth = 800
dHeight = 600
##dWidth,dHeight = pg.display.Info().current_w,pg.display.Info().current_h
##block_size = 20
##dWidth = round(dWidth/block_size) *block_size
##dHeight = round(dHeight/block_size)*block_size
##
##
##screen = pg.display.set_mode((0,0),FULLSCREEN)
screen = pg.display.set_mode((dWidth,dHeight))
pg.display.set_caption('Tanks')

#Sounds
boom_sound = pg.mixer.Sound("Sounds/boom.wav")
gameover_sound = pg.mixer.Sound("Sounds/gameover.wav")
shot_sound = pg.mixer.Sound("Sounds/firecracker.wav")

images = {}
images['bg'] = {}
images['bg']['intro'] = pg.image.load("tank.jpg")
images['bg']['main'] = pg.image.load("cover.jpeg")

for name,image in zip(images['bg'].keys(),images['bg'].values()):
    images['bg'][name] = pg.transform.scale(image, (dWidth,dHeight))
    
images['boom'] = pg.image.load("Photos/bang1.png")

image = pg.image.load('cloud.png')
images['cloud'] = pg.transform.scale(image,(int(dWidth/6),int(dHeight/5)))
                                     
##introbg = pg.transform.scale(introbg, (dWidth,dHeight))
##boom_image = pg.image.load("Photos/bang1.png")

##pg.mixer.music.load("Sounds/ingame.it")
##pg.mixer.music.play(-1)

clock = pg.time.Clock()

#Game_data
groundHeight = 35
gHeight = groundHeight
tankWidth = 40
tankHeight = 20
turretWidth = 3
turretLength = 25
wheelWidth = 4
barrierWidth = 50
maxPower = 100
gravity = 6
bombRadius = 4

#FONT_SIZES
smallFont = 25
midFont = 45
large = 75

#CLOCK
FPS = 50
