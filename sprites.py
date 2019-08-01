import pygame as pg
import random
from defs import *
from math import *

class TextBox:
    def __init__(self,rect,**kwargs):
        self.rect = pg.Rect(rect)
        self.buffer = []
        self.final = None
        self.rendered = None
        self.render_rect = None
        self.render_area = None
        self.blink = True
        self.blink_timer = 0.0
        self.accepted = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        self.process_kwargs(kwargs)

    def process_kwargs(self,kwargs):
        defaults = {"id" : None,
                    "command" : None,
                    "active" : True,
                    "color" : pg.Color("white"),
                    "font_color" : pg.Color("black"),
                    "outline_color" : pg.Color("black"),
                    "outline_width" : 2,
                    "active_color" : pg.Color("blue"),
                    "font" : pg.font.Font(None, 50),
                    "clear_on_enter" : True,
                    "inactive_on_enter" : False}
        for kwarg in kwargs:
            if kwarg in defaults:
                defaults[kwarg] = kwargs[kwarg]
            else:
                raise KeyError("InputBox accepts no keyword {}.".format(kwarg))
        self.__dict__.update(defaults)

    def get_event(self,event):
        if event.type == pg.KEYDOWN and self.active:
            if event.key in (pg.K_RETURN,pg.K_KP_ENTER):
                self.execute()
            elif event.key == pg.K_BACKSPACE:
                if self.buffer:
                    self.buffer.pop()
            elif event.unicode in self.accepted:
                self.buffer.append(event.unicode)

    def execute(self):
        if self.command:
            self.command(self.id,self.final)
        self.active = not self.inactive_on_enter
        if self.clear_on_enter:
            self.buffer = []

    def update(self):
        new = "".join(self.buffer)
        if new != self.final:
            self.final = new
            self.rendered = self.font.render(self.final, True, self.font_color)
            self.render_rect = self.rendered.get_rect(x=self.rect.x+2,
                                                      centery=self.rect.centery)
            if self.render_rect.width > self.rect.width-6:
                offset = self.render_rect.width-(self.rect.width-6)
                self.render_area = pg.Rect(offset,0,self.rect.width-6,
                                           self.render_rect.height)
            else:
                self.render_area = self.rendered.get_rect(topleft=(0,0))
        if pg.time.get_ticks()-self.blink_timer > 200:
            self.blink = not self.blink
            self.blink_timer = pg.time.get_ticks()

    def draw(self,surface):
        outline_color = self.active_color if self.active else self.outline_color
        outline = self.rect.inflate(self.outline_width*2,self.outline_width*2)
        surface.fill(outline_color,outline)
        surface.fill(self.color,self.rect)
        if self.rendered:
            surface.blit(self.rendered,self.render_rect,self.render_area)
        if self.blink and self.active:
            curse = self.render_area.copy()
            curse.topleft = self.render_rect.topleft
            surface.fill(self.font_color,(curse.right+1,curse.y,2,curse.h))

class Radio:
    def __init__(self,x,y,group = None,**kwargs):
        self.group = group
        self.center = (x,y)
        self.process_kwargs(kwargs)

    def process_kwargs(self,kwargs):
        defaults = {"id" : None,
                    "command" : None,
                    "active" : True,
                    "checkbox":False,
                    "outer_radius":10,
                    "inner_radius":7,
                    "main_color" : pg.Color("green"),
                    "selected_color":pg.Color("black"),
                    "outline_color" : pg.Color("black"),
                    "outline_width" : 2,
                    "active_color" : pg.Color("blue")}
        
        for kwarg in kwargs:
            if kwarg in defaults:
                defaults[kwarg] = kwargs[kwarg]
            else:
                raise KeyError("InputBox accepts no keyword {}.".format(kwarg))

        self.__dict__.update(defaults)
        
    def get_event(self,event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            x,y = event.pos
            h,k = self.center
            r = self.outer_radius
            if (x-h)**2 + (y-k)**2 <= r**2:
                self.execute()
                
    def execute(self):
        if self.active and self.checkbox:
            self.active = False

        else:
            if self.group:
                for butt in self.group:
                    butt.active = False
            self.active = True
        
        if self.command:
            self.command(self.main_color,self.active)

    def draw(self,surface):
        pg.draw.circle(surface,self.outline_color,self.center,int(self.outer_radius+self.outline_width))
        pg.draw.circle(surface,self.main_color,self.center,self.outer_radius)
        if self.active:
            pg.draw.circle(surface,self.selected_color,self.center,self.inner_radius)
            
class Object:
    def __init__(self):
        self.screen = screen
        
class Tank(Object):
    def __init__(self,name,posX,human = True,color = pg.Color('black')):
        Object.__init__(self)
        self.name = name
        self.power = maxPower/2
        self.score = 0
        self.ang = pi/4
        self.color = color
        self.midX = posX
        self.midY = dHeight - (groundHeight+tankHeight+wheelWidth)
        self.health = maxHealth
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
        self.turEnd = self.getTurEnd()
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

    def gethealthdata(self):
        bgcolor = gray
        if self.health > maxHealth*0.75:
            color = green
        elif self.health > maxHealth*0.25:
            color = yellow
        else:
            color = red

        return self.health,color,bgcolor


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
                
    def calculatePower(self,players,wind = 10,randomize = True):
        mX = self.midX
        A = self.ang
        g = gravity
        w = wind
        nearest = self.nearestEnemy(players)
        if nearest == None:return
        
        eX = nearest.midX
        R = abs(mX-eX)
        

        randomizer = 0
        if randomize:
            randomizer = random.randint(-100,100)

        R =  int(R + randomizer)

        power = abs(( (R*(g**2))/(g*sin(2*A)+2*w*(cos(A)**2)) )**(1/2))
        
        #power = abs((-R*g)/sin(2*A))**(1/2) #Using formula for velocity in projectile motion

        self.power = int(power)  
        if power > maxPower:
            self.power = maxPower
        elif power < maxPower*0.1:
            self.power = int(maxPower*0.1)               

    def calculateAngle(self,players):
        angle = pi/3
        nearest = self.nearestEnemy(players)
        if nearest == None:return
        if nearest.midX < self.midX:
            angle = 3*pi/2

        self.ang = angle
        

    def getTurEnd(self):
        return (self.midX+turretLength * cos(self.ang),self.midY - turretLength * sin(self.ang))


class Barrier(Object):
    def __init__(self,color = pg.Color("brown")):
        Object.__init__(self)
        self.screen = screen
        self.color = color
        self.barWidth = barrierWidth
        self.barX = (dWidth/2) + random.randint(int(-0.3*dWidth),int(0.3*dWidth))
        self.barHeight = random.randrange(int(dHeight*0.3), int(dHeight*0.6))
        self.damage = 0
        self.health = barrierHealth

    def draw(self):
        self.rect = pg.draw.rect(self.screen, self.color, [self.barX, dHeight-self.barHeight,self.barWidth,self.barHeight])


class Terrain(Object):
    def __init__(self,height,strength = 0,color = (102, 153, 153,5)):
        Object.__init__(self)
        self.color = color
        self.height = height
        self.strength = strength
        self.damage = 0
        
    def draw(self):
        self.rect = pg.draw.rect(self.screen,self.color,[0,dHeight-self.height,dWidth,dHeight],1)

        
class Missile(Object):
    def __init__(self,radius,strength,color = pg.Color('red')):
        Object.__init__(self)
        self.radius = radius
        self.strength = strength
        self.color = color
        self.exploded = False
        
    def draw(self,X,Y):
        self.rect = pg.draw.circle(self.screen,self.color,(X,Y),self.radius)
        
    def explode(self):
        playSound(boom_sound)
        width = 20
        height = 20
        x,y = self.rect.center
        for i in range(10):
            boom = pg.transform.scale(images['boom'],(width,height))
            boom_rect = boom.get_rect()
            boom_rect.center = x, y
            self.screen.blit(boom, boom_rect)
            pg.display.update()
            clock.tick(50)
            width += 5
            height += 5
        self.exploded = True
        
class Cloud(Object):
    
    def __init__(self):
        Object.__init__(self)
        self.image = images['cloud']
        self.rect = self.image.get_rect()
        self.rect.left = dWidth
        self.rect.top = 100
        self.speed = 0
        self.counter = 0
        self.destroyable = False
        self.obstacle = False
        
    def update(self):
        if self.counter > 50:
            self.counter = 0
            self.speed += random.randint(-2,2)
        else:
            self.counter += 1

        if self.speed > 10:
            self.speed = 10
        
        self.rect.centerx += self.speed

        if self.rect.right <= 0:
            self.rect.left = dWidth
        elif self.rect.left > dWidth:
            self.rect.right = 0
            
        
    def draw(self):
        self.update()
        self.screen.blit(self.image,self.rect)
        return self.speed
        
    
