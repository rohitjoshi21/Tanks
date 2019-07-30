import pygame as pg
from defs import *
import random
from math import *

class Object:
    def __init__(self):
        self.screen = screen
        
class Tank(Object):
    def __init__(self,name,posX,human = True,color = (0,0,0)):
        Object.__init__(self)
        self.name = name
        self.power = 50
        self.score = 0
        self.ang = pi/4
        self.color = color
        self.midX = posX
        self.midY = dHeight - (groundHeight+tankHeight+wheelWidth)
        self.health = 100
        self.moveX = 0
        self.chgAng = 0
        self.chgPow = 0
        self.damage = 0
        self.human = human
        self.movable = True
        self.draw_tank()
        
    def change_values(self):
        
        if self.human == True:
            
            self.lastmove = self.moveX
            self.ang += self.chgAng
            self.power += self.chgPow
            
        elif self.human == False:
            self.midX += random.randint(-15,15)
            
        if self.movable:
            self.midX += self.moveX
        else:
            self.moveX = 0
        
            
        self.health -= self.damage
        self.damage = 0
        if self.power > maxPower:
            self.power = maxPower
        elif self.power <= 0:
            self.power = 1
    
    def draw_tank(self):
        #Drawing Tank
        self.turEnd = self.Ends()
        x = int(self.midX)
        y= int(self.midY)
        pg.draw.circle(self.screen, self.color,(x,y), int(tankHeight/2))
        self.rect = pg.draw.rect(self.screen, self.color, (x-tankWidth/2,y,tankWidth, tankHeight))
        pg.draw.line(self.screen, black, (x,y),self.turEnd,turretWidth)

        #Drawing Wheels of Tank
        numberOfWheel = tankWidth/wheelWidth
        startX = int(tankWidth/2) - int((numberOfWheel - int(numberOfWheel))/2) - int(wheelWidth/2)
        for i in range(int(numberOfWheel)):
            pg.draw.circle(self.screen,wheelColor,(x-startX,y+tankHeight+int(wheelWidth/2)),int(wheelWidth/2))
            startX -= wheelWidth

    def gethealth(self):
        bgcolor = gray
        if self.health > maxPower*0.75:
            color = green
        elif self.health > maxPower*0.3:
            color = yellow
        else:
            color = red

        return self.health,color,bgcolor
    
##        if self.health > 0:
##            pg.draw.rect(self.screen,color1,(dWidth/2 + -1*dWidth/4 -50,50,self.health,25))
##        else:
##            pass


    def nearestEnemy(self,players):
        nearest = None
        eX = dWidth
        for player in players:
            if player == self:
                continue
            newex = abs(player.rect.centerx - self.midX)
            if newex < eX:
                nearest = player
                ex = newex
        return nearest
                
    def calculatePower(self,players,randomize = True):
        mX = self.midX
        angle = self.ang
        g = gravity

        nearest = self.nearestEnemy(players)
        if nearest == None:return
        eX = nearest.midX
        Hrange = abs(mX-eX)
        power = abs((-Hrange*g)/sin(2*angle))**(1/2) #Using formula for velocity in projectile motion
        if randomize:
            randomizer = random.randint(-10,10)/100
        else:
            randomizer = 0
        power =  int(power + power * randomizer)
        if power > maxPower:
            self.power = maxPower
        elif power < 0:
            #print(power)
            self.power = int(abs(power))
        else:
            self.power = int(power)               

    def calculateAngle(self,players):
        angle = pi/4
        nearest = self.nearestEnemy(players)
        if nearest == None:return
        if nearest.midX < self.midX:
            angle = 3*pi/4

        self.ang = angle
        

    def Ends(self):
        return (self.midX+turretLength * cos(self.ang),self.midY - turretLength * sin(self.ang))


class Barrier(Object):
    def __init__(self,color = black):
        Object.__init__(self)
        self.screen = screen
        self.color = color
        self.barWidth = barrierWidth
        self.barX = (dWidth/2) + random.randint(int(-0.2*dWidth),int(0.2*dWidth))
        self.barH = random.randrange(int(dHeight*0.3), int(dHeight*0.7))
        self.barHeight = self.barH
        self.damage = 0
        self.health = 200

    def draw(self):
        self.rect = pg.draw.rect(self.screen, self.color, [self.barX, dHeight-self.barHeight,self.barWidth,self.barHeight])


class Terrain(Object):
    def __init__(self,color,height,strength = 0):
        Object.__init__(self)
        self.color = color
        self.height = height
        self.strength = strength
        self.damage = 0
        
    def draw(self):
        self.rect = pg.draw.rect(self.screen,self.color,[0,dHeight-self.height,dWidth,dHeight])
        
class Missile(Object):
    def __init__(self,radius,damage,color = red):
        Object.__init__(self)
        self.radius = radius
        self.damage = damage
        self.color = color
        self.screen = screen
        
    def draw(self,X,Y):
        self.rect = pg.draw.circle(self.screen,self.color,(X,Y),self.radius)
        
    def explode(self):
        boom_sound.set_volume(0.1)
        pg.mixer.Sound.play(boom_sound)
        #time.sleep(0.01)
        width = 20
        height = 20
        x,y = self.rect.center
        for i in range(10):
            boom = pg.transform.scale(boom_image,(width,height))
            boom_rect = boom.get_rect()
            boom_rect.center = x, y
            self.screen.blit(boom, boom_rect)
            pg.display.update()
            clock.tick(50)
            width += 5
            height += 5
