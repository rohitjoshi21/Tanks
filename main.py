import pygame as pg
from defs import *
from sprites import *
from math import *
from random import *
import time

players = []
playersinfo = [['Rohit',red,False],['Susmita',blue,True],['Alex',green,False]]
totalplayers = len(playersinfo)
objects = []

clock = pg.time.Clock()


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

        play = button("Play",150,500,100,50, green, light_green, "chooseplayer")
        control = button("Controls",350,500,100,50, yellow, light_yellow, "controls")
        close = button("Quit",550,500,100,50, red, light_red, "quit")

        for response in (play,control,close):
            if response != None:
                return response
            
        pg.display.update()
        clock.tick(5)

def choosePlayer():
    intro = True
    while intro == True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                close_game()
            
        screen.fill(bgcolor)
        message_to_screen("Choose player mode",green,y_displace = -150,size = large)

        sing = button("Single Player",330,400,200,50, green, light_green, "single")
        mult = button("Two Player",330,500,200,50, yellow, light_yellow, "multi")
        
        for response in (sing,mult):
            if response != None:
                multiplayer = True if response == 'multi' else False
                return 'main'
            
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
        
        
        play = button("Play",150,500,100,50, green, light_green, "main")
        intro = button("Back",0,0,100,50, yellow, light_yellow, "intro")
        close = button("Quit",550,500,100,50, green, light_yellow, "quit")

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
        for event in pg.event.get():
            if event.type == pg.QUIT:
                close_game()
            
        screen.fill(bgcolor)
        message_to_screen("%s wins"%winner,black,size = midFont)
        

        play = button("Play Again",150,500,150,50, green, light_green, "main")
        intro = button("Home",350,500,100,50, yellow, light_yellow, "intro")
        close = button("Quit",550,500,100,50, green, light_yellow, "quit")

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
    show_power(player.power)
    healthbar(player.gethealth())
    show_name(player.name)

def healthbar(datas):
    health = datas[0]
    primary = datas[1]
    secondary = datas[2]
    pg.draw.rect(screen,secondary,(dWidth/2 - dWidth/4-50,50,maxPower,25))
    pg.draw.rect(screen,primary,(dWidth/2 - dWidth/4 -50,50,health,25))

def show_name(name):
    message_to_screen('Turn:',black,x = 5,y = 5 ,size = smallFont)
    message_to_screen(  name ,blue,x = 5,y = 30,size = smallFont)
    
def show_power(power):
    message_to_screen("Power: "+ str(power)+"%",black,x_displace = -dWidth/4, y_displace = -dHeight/2 +20, size = smallFont)

def fire(player):
    xy = player.turEnd
    pos = list(player.turEnd)
    fire = True
    g = gravity
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
        for event in pg.event.get():
            if event.type == pg.QUIT:
                close_game()
        screen.fill(bgcolor)
        weapon = Missile(bombR,20,color=blue)
        weapon.draw(int(pos[0]),int(pos[1]))
        draw_objects(player)
        
        x = power * cos(player.ang) * t
        try:
            y = x * tan(player.ang) - g/(2*(player.power*cos(player.ang))**2) * x**2
        except ZeroDivisionError:
            print(player.ang*180/pi,player.power,cos(player.ang),tan(player.ang))
            fire = False
            
        t += 0.2
        pos[0] = xy[0] + x
        pos[1] = xy[1] - y

        for obj in players+objects:
            if collided(weapon,obj):
                weapon.explode()
                fire = False
        if weapon.rect.left <=0 or weapon.rect.right >= dWidth:
            fire = False
            
        pg.display.update()
        clock.tick(100)

    for tank in players+objects[:-1]:
        setdamage(weapon.rect.center,tank)

def collided(sprite,target):
    collide = False
    if sprite != target:
        if sprite.rect.colliderect(target.rect):
            collide = True

    return collide

def setdamage(center,target):
    center2 = target.rect.center
    damage = 55 - ((center[0] - center2[0])**2 + (center[1] - center2[1])**2)**(1/2) * 0.5
    if damage < 0:
        damage = 0

    target.health -= damage

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
def makeBarrier(color):
    bar = Barrier(color=color)
    bar.draw()
    for player in players+objects:
        if collided(bar,player):
            bar = makeBarrier(color)
    return bar

def gameLoop():
    global totalplayers
    
    try: multiplayer
    except NameError: multiplayer = False
    
    x = 50
    for tanker in playersinfo:
        player = Tank(tanker[0],x,color = tanker[1],human = tanker[2])
        players.append(player)
        x += 350
        
    bar1 = makeBarrier(green)
    objects.append(bar1)
    bar2 = makeBarrier(blue)
    objects.append(bar2)

    terrain = Terrain(gray,groundHeight)
    
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
            if event.type == pg.QUIT:
                close_game()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_a :
                    players[turn].moveX = -5
                elif event.key == pg.K_d:
                    players[turn].moveX = 5
                elif event.key == pg.K_w:
                    players[turn].chgAng = 0.05
                elif event.key == pg.K_s:
                    players[turn].chgAng = -0.05
                elif event.key == pg.K_e:
                    players[turn].chgPow = 1
                elif event.key == pg.K_q:
                    players[turn].chgPow = -1
                elif event.key == pg.K_SPACE:
                    fire(players[turn])
                    turn = turn + 1 if turn < totalplayers-1 else 0
                
                        
            if event.type == pg.KEYUP:
                if event.key in (pg.K_UP, pg.K_DOWN,pg.K_w, pg.K_s):
                    players[turn].chgAng = 0
                elif event.key in (pg.K_LEFT, pg.K_RIGHT,pg.K_a, pg.K_d):
                    players[turn].moveX = 0
                elif event.key in (pg.K_q, pg.K_e):
                    players[turn].chgPow = 0
            
                    
        screen.fill(bgcolor)

        players[turn].change_values()
            
        for obj in players+objects[:-1]:
            if obj.health <= 0:
                if obj in players:
                    players.remove(obj)
                    totalplayers -= 1
                else:
                    objects.remove(obj)
                
                if turn >= totalplayers:
                    turn = 0
                
        draw_objects(players[turn])
        
        pg.display.update()
        validatemotion(players[turn]) 
        clock.tick(FPS)

        if len(players) == 1:
            return 'over'

        
        





currScreen = gameIntro

screens = {'intro':gameIntro,'controls':game_controls,'chooseplayer':choosePlayer,
           'main':gameLoop,'quit':close_game,'over':gameOver}
gameOn = True
while gameOn:
    resp = currScreen()
    if resp != None:
        currScreen = screens[resp]
    else:
        gameOn = False

#gameLoop()
