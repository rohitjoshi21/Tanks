#!/usr/bin/python3

import pygame as pg
import random
from math import sin, cos, tan, pi
import time

pg.init()

#COLORS
bgcolor = (204, 221, 255)
white = (255,255,255)
black = (0,0,0)
blue = (0,0,255)
red = (200,0,0)
light_red = (255,0,0)
yellow = (200,200,0)
light_yellow = (255,255,0)
green = (34,177,76)
light_green = (0,255,0)

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
pg.display.set_caption('Tanks')

#Game_data
gHeight = 35
tankWidth = 40
tankHeight = 20
turretWidth = 3
turretLength = 30
wheelWidth = 5
barW = 50

#FONT_SIZES
smallFont = 25
midFont = 45
large = 75

#CLOCK
FPS = 15
clock = pg.time.Clock()

class Tank:
    def __init__(self,player,angle,power = 50, machine = False):
        self.pow = power
        self.ang = angle
        self.p = player
        if player == -1:
            self.tankX = dWidth * 0.1
        else:
            self.tankX = dWidth * 0.9
        self.tankY = dHeight * 0.9
        self.health = 100
        self.moveX = 0
        self.chgAng = 0
        self.chgPow = 0
        self.damage = 0
        self.auto = machine

    def change(self):
        if self.auto != True:
            self.tankX += self.moveX
            self.ang += self.chgAng
            self.pow += self.chgPow
            
        elif self.auto == True:
            self.tankX += random.randint(-15,15)
            
            
        self.health -= self.damage
        self.damage = 0
        if self.pow > 100:
            self.pow = 100
        elif self.pow <= 0:
            self.pow = 1
            
    def draw_tank(self):
        self.turEnd = self.Ends()
        x = int(self.tankX)
        y= int(self.tankY)
        pg.draw.circle(screen, black,(x,y), int(tankHeight/2))
        pg.draw.rect(screen, black, (x-tankHeight,y,tankWidth, tankHeight))
        pg.draw.line(screen, black, (x,y),self.turEnd,turretWidth)
        startX = 15
        for i in range(7):
            pg.draw.circle(screen,black,(x-startX,y+20),wheelWidth)
            startX -= 5

    def healthBar(self):
        if self.health > 75:
            color1 = green
        elif self.health > 30:
            color1 = yellow
        else:
            color1 = red
            
        if self.health > 0:
            pg.draw.rect(screen,color1,(dWidth/2 + self.p*dWidth/4 -50,50,self.health,25))
        else:
            pass
        
    def calculatePower(self,mX,angle,eX,g):
        power = ( ( (mX-eX)*(-g) )/sin(2*angle) )**(1/2)
        randomizer = random.randint(-10,10)/100

        power =  int(power + power * randomizer)
        if power > 100:
            return 100
        elif power < 0:
            return 0
        else:
            return int(power)
        
    def fire(self, enemyX):
        xy = self.turEnd
        pos = list(self.turEnd)
        fire = True
        g = 6
        x,y = 0,0
        damage = 0
        self.pow = self.calculatePower(self.tankX,self.ang,enemyX,g) if self.auto else self.pow
        t = 0
        while fire:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    close_game()
            screen.fill(bgcolor)
            pg.draw.circle(screen, red, (int(pos[0]),int(pos[1])),5)
            draw_objects(p1,p2)
            x = self.pow * cos(self.ang) * t
            y = x * tan(self.ang) - g/(2*(self.pow*cos(self.ang))**2) * x**2
            t += 0.2
            pos[0] = xy[0] + x
            pos[1] = xy[1] - y
            if pos[1] >= dHeight-gHeight:
                fire = False
                pg.mixer.Sound.play(boom_sound)
                hit_x = int(pos[0]*(dHeight-gHeight)/pos[1])
                hit_y = dHeight-gHeight
                self.explosion(hit_x, hit_y)
                if enemyX-35 < hit_x < enemyX+35:
                    damage = 25 - abs((hit_x - enemyX)/7)
                    
                
            check_x1 = pos[0] <= barX + barW
            check_x2 = pos[0] >= barX

            check_y1 = pos[1] <= dHeight
            check_y2 = pos[1] >= dHeight - barH

            if check_x1 and check_x2 and check_y1 and check_y2:
                fire = False
                pg.mixer.Sound.play(boom_sound)
                hit_x = int(pos[0])
                hit_y = int(pos[1])
                self.explosion(hit_x, hit_y)
                
               
            pg.display.update()
            clock.tick(100)
        return damage
    
    def explosion(self,x,y ):
        #time.sleep(0.01)
        width = 20
        height = 20
        for i in range(10):
            boom = pg.transform.scale(boom_image,(width,height))
            boom_rect = boom.get_rect()
            boom_rect.center = x, y
            screen.blit(boom, boom_rect)
            pg.display.update()
            clock.tick(50)
            width += 5
            height += 5
                    

    def Ends(self):
        return (self.tankX+turretLength * cos(self.ang),self.tankY - turretLength * sin(self.ang))
    
    def show_power(self):
        message_to_screen("Power: "+ str(self.pow)+"%",black,x_displace = self.p*dWidth/4, y_displace = -dHeight/2 +20, size = smallFont)


def choosePlayer():
    intro = True
    while intro == True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                close_game()
            
        screen.fill(bgcolor)
        message_to_screen("Choose player mode",green,y_displace = -150,size = large)

        button("Single Player",330,400,200,50, green, light_green, "single")
        button("Multiplayer",330,500,200,50, yellow, light_yellow, "multi")
        pg.display.update()
        clock.tick(5)
        
def gameIntro():
    intro = True
    while intro == True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                close_game()
            
        screen.fill(bgcolor)
        message_to_screen("Welcome to Tanks",green,y_displace = -100,size = large)
        message_to_screen("The objective of the game is to shoot destroy",black,y_displace = -30)
        message_to_screen("the enemy tank before they destroy you.",black,y_displace = 10)

        button("Play",150,500,100,50, green, light_green, "start")
        button("Controls",350,500,100,50, yellow, light_yellow, "controls")
        button("Quit",550,500,100,50, red, light_red, "quit")
        
        pg.display.update()
        clock.tick(5)        

def game_controls():
    controls = True
    while controls == True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                close_game()
                    
        screen.fill(bgcolor)
        message_to_screen("Controls",green,y_displace = -200,size = large)
        message_to_screen("Player 1             Player 2",black,x = 350, y = 200)
        message_to_screen("Fire:                    Spacebar          Spacebar",black,x = 150, y = 250)
        message_to_screen("Change Angle:        W,S          Up & Down arrows",black,x = 150, y = 300)
        message_to_screen("Move Tank:             A,D         Left & Right arrows",black,x = 150, y = 350)
        message_to_screen("Change Power:        Q,E                Alt & Ctrl",black,x = 150, y = 400)
        
        
        button("Play",150,500,100,50, green, light_green, "start")
        button("Back",0,0,100,50, yellow, light_yellow, "main")
        button("Quit",550,500,100,50, green, light_yellow, "quit")
        
        pg.display.update()
        clock.tick(5)

def message_to_screen(msg,color, x_displace = 0,y_displace=0, size = smallFont,x = None ,y = None):
    font = pg.font.SysFont('comicsansms', size)
    screen_text = font.render(msg, True, color)
    text_rect = screen_text.get_rect()
    if x == None and y == None:
        text_rect.center = (dWidth/2)+x_displace, (dHeight/2)+y_displace
    else:
        text_rect.topleft = x, y
    screen.blit(screen_text, text_rect)

def close_game():
    pg.quit()
    import sys
    sys.exit()

def draw_barrier(xlocation, barrierHeight, barrierWidth):
    pg.draw.rect(screen, black, [xlocation, dHeight-barrierHeight,barrierWidth,barrierHeight])
    
def text_to_button(msg, color, x, y, width, height, size = 25):
    font = pg.font.SysFont('comicsansms', size)
    screen_text = font.render(msg, True, color)
    text_rect = screen_text.get_rect()
    text_rect.center = (x+(width/2)), (y+(height/2))
    screen.blit(screen_text, text_rect)
    
def button(text, x, y, width, height,inactive_color,active_color, action=None):
    cur = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()
    global multiplayer
    if x < cur[0] < x+width and y < cur[1] < y+height:
        pg.draw.rect(screen, active_color, (x,y,width,height))
        
        if click[0] == 1 and action != None:
            
            if action == "start":
                choosePlayer()
            elif action == "quit":
                close_game()
            elif action == "controls":
                game_controls()
            elif action == "main":
                gameIntro()
            elif action == 'single':
                multiplayer = False
                gameLoop()
            elif action == 'multi':
                multiplayer = True
                gameLoop()
    else:
        pg.draw.rect(screen, inactive_color, (x,y,width,height))
    text_to_button(text, black, x, y, width, height)
    
def gameOver(winner, loser):
    pg.mixer.Sound.play(gameover_sound)
    over = True
    while over == True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                close_game()
            
        screen.fill(bgcolor)
        message_to_screen("%s wins"%winner,black,y_displace = -100,size = midFont)
        message_to_screen("%s loses"%loser,black,y_displace = -30, size = midFont)

        button("Play Again",150,500,150,50, green, light_green, "start")
        button("Home",350,500,100,50, yellow, light_yellow, "main")
        button("Quit",550,500,100,50, green, light_yellow, "quit")
        pg.display.update()
        clock.tick(5)

def draw_objects(x,y,displace_message = None):
    x.draw_tank()
    y.draw_tank()
    x.show_power()
    y.show_power()
    x.healthBar()
    y.healthBar()
    draw_barrier(barX, barH, barW)
    screen.fill(green, [0,dHeight-gHeight,dWidth,gHeight])
    if displace_message != None:
        message_to_screen("Your Turn",black,x_displace = displace_message,size = smallFont)

def gameLoop():
    print('run')
    game = True
    global barX, barH, p1, p2
    barX = (dWidth/2) + random.randint(-0.2*dWidth,0.2*dWidth)
    barH = random.randrange(dHeight*0.1, dHeight*0.6)
    p1 = Tank(-1, pi/4)
    if not multiplayer:
        p2 = Tank(1, 3*pi/4,machine = True)
    else:
        p2 = Tank(1, 3*pi/4)
    turn = 1
    while game:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                close_game()
            if event.type == pg.KEYDOWN:
                if turn == 1:
                    if event.key == pg.K_a:
                        p1.moveX = -5
                    elif event.key == pg.K_d:
                        p1.moveX = 5
                    elif event.key == pg.K_w:
                        p1.chgAng = 0.1
                    elif event.key == pg.K_s:
                        p1.chgAng = -0.1
                    elif event.key == pg.K_e:
                        p1.chgPow = 1
                    elif event.key == pg.K_q:
                        p1.chgPow = -1
                    elif event.key == pg.K_SPACE:
                        p2.damage = p1.fire(p2.tankX)
                        turn = 2
                        

                elif turn == 2 and multiplayer == True:
                    if event.key == pg.K_LEFT:
                        p2.moveX = -5
                    elif event.key == pg.K_RIGHT:
                        p2.moveX = 5
                    elif event.key == pg.K_UP:
                        p2.chgAng = -0.1
                    elif event.key == pg.K_DOWN:
                        p2.chgAng = 0.1
                    elif event.key == 305:
                        p2.chgPow = 1
                    elif event.key == 307:
                        p2.chgPow = -1
                    elif event.key == pg.K_SPACE:
                        p1.damage = p2.fire(p1.tankX)
                        turn = 1
            if event.type == pg.KEYUP:
                if event.key in (pg.K_UP, pg.K_DOWN):
                    p2.chgAng = 0
                elif event.key in (pg.K_w, pg.K_s):
                    p1.chgAng = 0
                elif event.key in (pg.K_a, pg.K_d):
                    p1.moveX = 0
                elif event.key in (pg.K_LEFT, pg.K_RIGHT):
                    p2.moveX = 0
                elif event.key in (pg.K_q, pg.K_e):
                    p1.chgPow = 0
                elif event.key in (305, 307):
                    p2.chgPow = 0
                    
        screen.fill(bgcolor)
        
        p1.change()

        if multiplayer == True:
            p2.change()
        
        if p1.tankX + 20 > barX: p1.tankX -= 5
        if p1.tankX - 20 < 0: p1.tankX += 5
        
        if p2.tankX - 20 < barX + barW: p2.tankX += 5
        if p2.tankX + 20 > dWidth: p2.tankX -=5

        if turn == 1:
            x_displace = -dWidth/3
        elif turn == 2:
            x_displace = dWidth/3
            
        draw_objects(p1,p2,x_displace)
        pg.display.update()
        clock.tick(FPS)
        
        if multiplayer == False and turn == 2:
            time.sleep(3)
            p2.change()
            p1.damage = p2.fire(p1.tankX)
            turn = 1
            
        if p2.health <= 0: gameOver("Player 1","Player 2")
        if p1.health <= 0: gameOver("Player 2","Player 1")


gameIntro()
gameLoop()
        
