import pygame as pg
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

#Sounds
boom_sound = pg.mixer.Sound("Sounds/boom.wav")
gameover_sound = pg.mixer.Sound("Sounds/gameover.wav")
shot_sound = pg.mixer.Sound("Sounds/firecracker.wav")

boom_image = pg.image.load("Photos/bang1.png")

##pg.mixer.music.load("Sounds/ingame.it")
##pg.mixer.music.play(-1)

#DISPLAY_WINDOW
dWidth = 800
dHeight = 600
block_size = 20
dWidth = round(dWidth/block_size) *block_size
dHeight = round(dHeight/block_size)*block_size
screen = pg.display.set_mode((dWidth,dHeight))
#pg.display.set_caption('Tanks')


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
FPS = 15
