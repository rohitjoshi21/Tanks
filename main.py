import pygame as pg
from defs import *
from sprites import *
from math import *
import random
import time
from textbox import *
from radiobutton import Radio

players = []
playersinfo = []
totalplayers = 3
objects = []
wind = 0
clock = pg.time.Clock()
scores = {}
colors = ['red','blue','green','pink','yellow','gray','orange']

def check_events():
    for event in pg.event.get():
            if event.type == pg.QUIT:
                close_game()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    close_game()

def check_quit_event(event):
    if event.type == pg.QUIT:
        close_game()
    elif event.type == pg.KEYDOWN:
        if event.key == pg.K_ESCAPE:
            close_game()
                    
                    
def gameIntro():
    intro = True
    while intro == True:
        check_events()
            
##        screen.fill(bgcolor)
        screen.blit(images['bg']['intro'],images['bg']['intro'].get_rect())
        message_to_screen("Welcome to Tanks",black,y_displace = -180,size = large)
        message_to_screen("The objective of the game is to shoot destroy",black,y_displace = -100)
        message_to_screen("the enemy tank before they destroy you.",black,y_displace =-60)

        x = dWidth/2
        y = dHeight - 100
        play = button("Play",x-200,y,100,50, green, light_green, "chooseplayer")
        control = button("Controls",x,y,100,50, yellow, light_yellow, "controls")
        close = button("Quit",x+200,y,100,50, red, light_red, "quit")

        for response in (play,control,close):
            if response != None:
                return response
            
        pg.display.update()
        clock.tick(5)
        
   
def choosePlayer():
    global resp
    intro = True
    resp = ''
    
    def setplayerinf(ids,number):
        global totalplayers,resp,playersinfo
        try:
            if 1 < int(number) < 8:
                totalplayers = int(number)

                for i in range(totalplayers):
                    data = {'name':'Tank'+str(i+1),'color':pg.Color('green'),'human':True}
                    playersinfo.append(data)
                resp = 'prop'
        except:
            pass
        
    inputbox = TextBox((dWidth/2-150,dHeight/2-30,300,70),command = setplayerinf)
    
    while intro == True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                close_game()
            inputbox.get_event(event)
            
        screen.fill(bgcolor)
        message_to_screen("Choose no of player",green,y_displace = -150,size = large)
        
        
        inputbox.update()
        inputbox.draw(screen)
        
        if resp == 'prop':
            return resp
            
        pg.display.update()
        clock.tick(5)

def playerproperties():
    global pos,resp,scores
    controls = True
    pos = 0
    resp = ''
    color_buttons = []
    def setplayername(ids,name):
        global pos,resp
        playersinfo[pos]['name'] = name
        scores[name] = 0
        if pos == totalplayers-1:
            resp = "main"
        pos += 1

    def setplayercolor(color,active):
        playersinfo[pos]['color']=color

    def setplayermode(color,active):
        playersinfo[pos]['human'] = not active
        
    x = int(dWidth/2-60)
    y = int(dHeight/2-60)
    for color in colors:
        rad = Radio(x,y,color_buttons,main_color=pg.Color(color),command = setplayercolor,active = color=='gray')
        color_buttons.append(rad)
        x += 50
    modebutt = Radio(int(dWidth/2+200),int(dHeight/2),command = setplayermode,active = False,checkbox = True)
    
    inputbox = TextBox((dWidth/2-150,dHeight/2-30,300,60),command = setplayername)
    while controls == True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                close_game()
            inputbox.get_event(event)
            modebutt.get_event(event)
            for butt in color_buttons:
                butt.get_event(event)
        
        screen.fill(bgcolor)
        message_to_screen("Player:-"+str(pos+1),black,x_displace=-70,y_displace=-140,size=mid)
        message_to_screen("Name:- ",black,x_displace=-120,y_displace=-60)
        message_to_screen("Computer Mode",black,x=dWidth/2+220,y=dHeight/2-30,size = small)
        if resp == 'main':
            return resp
        inputbox.update()
        inputbox.draw(screen)
        modebutt.draw(screen)
        for butt in color_buttons:
                butt.draw(screen)


##        x = dWidth/2
##        y = dHeight/2
##        close = button("Quit",x+200,y,100,50, red, light_red, "quit")
        
            
        pg.display.update()
        clock.tick(5)
                
def game_controls():
    controls = True
    while controls == True:
        check_events()
               
        screen.fill(bgcolor)
##        msg = \
##        """
##                        Controls
##                        
##        Move Tank:    Left & Right Arrow / A & D Button
##        Change Angle: Up $ Down Arrows / W & S Button
##        Fire/Shoot:   Space / Left Ctrl
##        """
##        message_to_screen(msg,green,x = dWidth/2,y = dHeight/2)
        message_to_screen("Controls",green,y_displace = -200,size = large)
        message_to_screen("Player 1             Player 2",black,x = 350, y = 200)
        message_to_screen("Fire:                    Spacebar          Spacebar",black,x = 150, y = 250)
        message_to_screen("Change Angle:        W,S          Up & Down arrows",black,x = 150, y = 300)
        message_to_screen("Move Tank:             A,D         Left & Right arrows",black,x = 150, y = 350)
        message_to_screen("Change Power:        Q,E                Alt & Ctrl",black,x = 150, y = 400)
        
        x = dWidth/2
        y = dHeight - 100
        play = button("Play",x-200,y,100,50, green, light_green, "chooseplayer")
        intro = button("Back",x,y,100,50, yellow, light_yellow, "intro")
        close = button("Quit",x+200,y,100,50, green, light_yellow, "quit")

        for response in (play,intro,close):
            if response != None:
                return response
            
        pg.display.update()
        clock.tick(5)
        
def gameOver():
    
    try:
        winner = players[0].name
    except:
        winner = 'Noone'
        
    pg.mixer.Sound.play(gameover_sound)
    over = True
    while over == True:
        check_events()
            
        screen.fill(bgcolor)
        message_to_screen("%s wins"%winner,black,size = midFont)
        
        x = int(dWidth/2)
        play = button("Play Again",x-200,500,150,50, green, light_green, "main")
        intro = button("Home",     x,    500,150,50, yellow, light_yellow, "intro")
        close = button("Quit",     x+200,500,150,50, green, light_yellow, "quit")

        for response in (play,intro,close):
            if response != None:
                return response
            
        pg.display.update()
        clock.tick(5)
        
def text_to_button(msg, color, x, y, width, height, size = 25):
    font = pg.font.SysFont('comicsansms', size)
    screen_text = font.render(msg, True, color)
    text_rect = screen_text.get_rect()
    text_rect.center = (x+(width/2)), (y+(height/2))
    screen.blit(screen_text, text_rect)

def close_game():
    pg.quit()
    import sys
    sys.exit()
    return None

def message_to_screen(msg,color, x_displace = 0,y_displace=0, size = smallFont,x = None ,y = None):
    font = pg.font.SysFont('comicsansms', size)
    screen_text = font.render(msg, True, color)
    text_rect = screen_text.get_rect()
    if x == None and y == None:
        text_rect.center = (dWidth/2)+x_displace, (dHeight/2)+y_displace
    else:
        text_rect.topleft = x, y
    screen.blit(screen_text, text_rect)

def button(text, x, y, width, height,inactive_color,active_color, action=None):
    x = x - width/2
    y = y - height/2
    cur = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()
    global multiplayer
    if x < cur[0] < x+width and y < cur[1] < y+height:
        pg.draw.rect(screen, active_color, (x,y,width,height))
        
        if click[0] == 1 and action != None:
            return action
    else:
        pg.draw.rect(screen, inactive_color, (x,y,width,height))
        
    text_to_button(text, black, x, y, width, height)
    return None

        
def draw_objects(player):
    for tanker in players:
        tanker.draw_tank()

    for obj in objects:
        obj.draw()
        
    w = cloud.draw()
    show_power(player.power)
    healthbar(player.gethealth())
    show_name(player.name)
    show_score()
    message_to_screen('Wind:- '+str(w),black,x = dWidth/2,y=5,size = smallFont)

def healthbar(datas):
    health = datas[0]
    primary = datas[1]
    secondary = datas[2]
    pg.draw.rect(screen,secondary,(dWidth/2 - dWidth/4-50,50,maxPower,25))
    pg.draw.rect(screen,primary,(dWidth/2 - dWidth/4 -50,50,health,25))

def show_name(name):
    message_to_screen('Turn:',black,x = 5,y = 5 ,size = smallFont)
    message_to_screen(  name ,black,x = 5,y = 30,size = smallFont)
    
def show_power(power):
    message_to_screen("Power: "+ str(power)+"%",black,x_displace = -dWidth/4, y_displace = -dHeight/2 +20, size = smallFont)

def fire(player):
    xy = player.turEnd
    pos = list(player.turEnd)
    fire = True
    g = gravity
    wind = cloud.speed
    bombR = bombRadius
    x,y = 0,0
    damage = 0
    
    
    if player.human == False:
        time.sleep(1)
        player.calculateAngle(players)
        player.calculatePower(players,randomize = False)
        
    power = player.power
    t = 0
    while fire:
        check_events()
        screen.blit(images['bg']['main'],images['bg']['main'].get_rect())
        weapon = Missile(bombR,20,color=blue)
        weapon.draw(int(pos[0]),int(pos[1]))
        draw_objects(player)
        
        x = power * cos(player.ang) * t + wind*t/2        #Using formula from projectile motion
        y = power * sin(player.ang) * t - (g*(t**2))/2
            
        t += 0.2
        pos[0] = xy[0] + x
        pos[1] = xy[1] - y

        for obj in players+objects:
            if collided(weapon,obj):
                weapon.explode()
                fire = False
                break
            
        if weapon.rect.left <=0 or weapon.rect.right >= dWidth:
            fire = False
            
        pg.display.update()
        clock.tick(FPS)
        
    score = 0

    if weapon.exploded:
        for tank in players:
            score += setdamage(weapon.rect.center,tank)*100
        player.score += score
        
        for obj in objects[:-1]:
            setdamage(weapon.rect.center,tank)
    
    
def collided(sprite,target):
    collide = False
    if sprite != target:
        if sprite.rect.colliderect(target.rect):
            collide = True

    return collide

def setdamage(center,target):
    center2 = target.rect.center
    damage = 55 - ((center[0] - center2[0])**2 + (center[1] - center2[1])**2)**(1/2) * 0.7
    if damage < 0:
        damage = 0

    target.health -= damage
    return damage

def validatemotion(player):
    movable = True
    pos = player.rect
    move = player.moveX
    
    if pos.left<= 0 or pos.right >= dWidth:
        movable = False
        
    for obj in players+objects[:-1]:
        if collided(player,obj):
            movable = False
            
    if not movable:
        player.midX -= player.moveX
        
def show_score():
    global scores
    x = dWidth-200
    y = 40
    for player in players:
        scores[player.name] = [int(player.score),player.color]
        
    for name in scores.keys():
        message_to_screen(name+':- '+str(scores[name][0]),scores[name][1],size=30,x=x,y=y)
        y += 50
        
def makeBarrier(color):
    bar = Barrier(color=color)
    bar.draw()
    for player in players+objects:
        if collided(bar,player):
            bar = makeBarrier(color)
    return bar

def gameLoop():
    global totalplayers,cloud
    
    try: multiplayer
    except NameError: multiplayer = False
    
    x = tankWidth/2
    interval = (dWidth-tankWidth)/(totalplayers-1)
    for tanker,tanker in zip(range(totalplayers),playersinfo):
        player = Tank(tanker['name'],x,color = tanker['color'],human = tanker['human'])
        players.append(player)
        x += interval
        
    bar1 = makeBarrier(green)
    objects.append(bar1)
    bar2 = makeBarrier(blue)
    objects.append(bar2)

    terrain = Terrain(blue,groundHeight)
    cloud = Cloud()
    
    objects.append(terrain)
    turn = 0
    draw_objects(players[turn])
    game = True
    while game:

        if players[turn].human == False:
            time.sleep(1)
            fire(players[turn])
            turn = turn + 1 if turn < totalplayers -1 else 0
            
        for event in pg.event.get():
            check_quit_event(event)
            if event.type == pg.KEYDOWN:
                b = event.key
                if b == pg.K_ESCAPE:
                    close_game()
                    
                elif b == pg.K_a or b == pg.K_LEFT :
                    players[turn].moveX = -2
                elif b == pg.K_d or b == pg.K_RIGHT:
                    players[turn].moveX = 2
                elif b == pg.K_w or b == pg.K_UP:
                    players[turn].chgAng = 0.05
                elif b == pg.K_s or b == pg.K_DOWN:
                    players[turn].chgAng = -0.05
                elif b == pg.K_e or b == pg.K_PAGEUP:
                    players[turn].chgPow = 1
                elif b == pg.K_q or b == pg.K_PAGEDOWN:
                    players[turn].chgPow = -1
                elif b == pg.K_SPACE or b == pg.K_LCTRL:
                    fire(players[turn])
                    turn = turn + 1 if turn < totalplayers-1 else 0
                
                        
            if event.type == pg.KEYUP:
                if event.key in (pg.K_UP, pg.K_DOWN,pg.K_w, pg.K_s):
                    players[turn].chgAng = 0
                elif event.key in (pg.K_LEFT, pg.K_RIGHT,pg.K_a, pg.K_d):
                    players[turn].moveX = 0
                elif event.key in (pg.K_q, pg.K_e,pg.K_PAGEUP,pg.K_PAGEDOWN):
                    players[turn].chgPow = 0
            
                    
        screen.blit(images['bg']['main'],images['bg']['main'].get_rect())
        players[turn].change_values()
            
        for obj in players+objects[:-1]:
            if obj.health <= 0:
                if obj in players:
                    i = players.index(obj)
                    players.remove(obj)
                    totalplayers -= 1
                else:
                    objects.remove(obj)

                if i < turn:
                    turn -= 1
                elif i >= turn:
                    if turn+1 > totalplayers:turn=0

                
        draw_objects(players[turn])
        
        pg.display.update()
        validatemotion(players[turn]) 
        clock.tick(FPS)

        if len(players) == 1:
            return 'over'

        
        




##Main Program
        
currScreen = gameIntro

screens = {'intro':gameIntro,'controls':game_controls,'chooseplayer':choosePlayer,
           'main':gameLoop,'quit':close_game,'over':gameOver,'prop':playerproperties}
gameOn = True
while gameOn:
    resp = currScreen()
    if resp != None:
        currScreen = screens[resp]
    else:
        gameOn = False

gameLoop()
##choosePlayer()
##playerproperties()
