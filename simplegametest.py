import sys, pygame, time, random, os,  pickle
from constants import *
from menu import *
from game_objects import *
from tools import *

pygame.init()    # initialize all pygame modules

fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode(SCREEN_SIZE)  #create a new Surface object
action_window = pygame.Surface(ACTION_SCREEN_SIZE)

## pygame.FULLSCREEN can add to set_mode
(fire_start_pos, gold_start_pos) = set_random_coord()

##group of downloaded surfaces:
U_LOSE_pic = add_image('lose.png')
PAUSE_pic = add_image('pause.png')
LIFE_pic = add_image('heart.png')
GROUND_pic = add_image('ground.png')
COIN_pic = add_image('coin_30.png')
POTION_pic = add_image('water_potion.png')
BOX_pic = add_image('box.png')
INSIDEbox_pic = add_image('box_window.png')

##player's sprite initializing:
Left  = Eye("left_eye.png", 'left', START_EYE_POS)
Right = Eye("right_eye.png", 'right', START_EYE_POS)
current_sprite  = Left.img()
sprite = Left

##other moving objects:
(fire_start_pos, gold_start_pos) = set_random_coord()
Fire  = Flame("fire_50.png", fire_start_pos, START_ENEMY_SPEED)
Gold  = Coin("coin.png", gold_start_pos, START_ENEMY_SPEED)
Heart = Enemies("red_heart.png", gold_start_pos, START_ENEMY_SPEED)
Enemy = pygame.sprite.Group(Fire, Gold)

##all buttons and info panels:
start_button = Button(GREEN, 160, 100, 200, 50, 'START')
exit_button  = Button(RED, 160, 180, 200, 50, 'EXIT')
box_button = Pic_Button(BOX_pic, (240, 470))

time_panel = InfoPanel('TIME', DARK_GREY,  390, 477, 100, 20, 0, 'TIME')
score_panel = InfoPanel('SCORE', DARK_GREY,  10, 477, 110, 20, 0, 'SCORE')
total_score = InfoPanel('TOTAL_SCORE', RED, 250, 75, 200, 50, 0, 'TOTAL SCORE')
record = InfoPanel('RECORD_SCORE', RED, 250, 150, 200, 50, 0, 'RECORD')
new_record = InfoPanel('RECORD_SCORE', RED, 250, 100, 200, 50, 0, 'NEW RECORD')
level_info = InfoPanel('Level', GRAY,  100, 2, 100, 25, 0, 'LVL')
coin_panel = InfoPanel('COIN_CHECKER', GRAY, 250, 2, 30, 25, 0, '')
potion_panel = InfoPanel('POTION_CHECKER', GRAY, 380, 2, 30, 25, 0, '')
                                   
##set of flags: 
gameplay = False
TIMER = None
collide = None
WAITING = True
LOSE = False
PAUSE = False
BOX = False

#initial variables:
level = 1

##main loop:

while 1:
    fpsClock.tick(FPS)

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        
        if event.type == pygame.QUIT or exit_button.isPressed(pos):
            pygame.quit()
            sys.exit()
            
        elif event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_ESCAPE:    
                pygame.quit()
                sys.exit()
                
            if event.key == pygame.K_SPACE:
                PAUSE = not PAUSE
                
        elif start_button.isPressed(pos): #press the button for start
            gameplay = True             #game process is started
            LOSE = False                #lose pic isnt drawn
            PAUSE = False
            WAITING = False
            TIMER = pygame.time.get_ticks() #start a time counting
            Enemies.set_start_level(Gold, Fire, Heart) #refresh level to 1 for new start
            score_panel.value = 0
            coin_counter = 0
            potion_counter = 0
            level_info.value = 1
            coin_panel.value = 0
            LIFE_COUNTER = 3
            NEW_RECORD = False
            random_heart_int = random.choice(range(10,30))
        
        if box_button.pic_isPressed(event):
            BOX = True 

    if TIMER:
        result_time = (pygame.time.get_ticks() - TIMER)//1000
        time_panel.update(result_time)  #set new value on the button text


    if gameplay == True and not PAUSE:        #if game process started, every obj can move
        Enemy.update()
        sprite.update()
        
        if sprite.direction == 'right':
            current_sprite = Right.image
        elif sprite.direction == 'left':
            current_sprite = Left.image

        collide = pygame.sprite.spritecollide(sprite, Enemy, True)
        #trying to detect collide with any of Enemies obj
                  

    if collide:
        if collide[0] == Gold:  #if U catch the coin, plus score
            coin_counter += 1
            coin_panel.update(coin_counter)
            score = score_panel.value + 5
            score_panel.update(score)
            
            if coin_counter == level * 10 * (level + 1):
                #every N coins level UP:
                level +=1
                level_info.update(level)
                Enemies.level_up(Gold, Fire)
            Gold.alive = False
        elif collide[0] == Fire:
            LIFE_COUNTER -= 1
            Fire.alive = False
            Gold.alive = False
            
            if LIFE_COUNTER == 0:
            #if U catch the fire, U lose & stop gameplay & timer stop
                
                TIMER = False
                LOSE = True
                gameplay = False
                WAITING = True
                total_res = score_panel.value
                prev_record = record_res()
                scores = score_to_list(score_panel.value)
                total_score.update(total_res)
                
                if total_res > prev_record:
                    new_record_score = record_res()
                    NEW_RECORD = True
                
        elif collide[0] == Heart:
            LIFE_COUNTER = 3
               
    if  Gold.is_killed() and Fire.is_killed() and gameplay == True and not PAUSE:
        #everything after enemies free falling (without collide!)
        score = score_panel.value + 2
        score_panel.update(score)
        (fire_start_pos, gold_start_pos) = set_random_coord()
        Fire  = Flame("fire_50.png", fire_start_pos, Fire.speed)
        Gold  = Coin("coin.png", gold_start_pos, Gold.speed)
        Enemy.add(Fire, Gold)
        
        #checking extra life heart condition: 
        if score >= random_heart_int and score % random_heart_int == 0:
            Heart = Enemies("red_heart.png", set_random_coord()[0], Gold.speed)
            Enemy.add(Heart)
                   
    #DRAW everything we have:    
    screen.fill(GRAY)
    action_window.fill(GRAY)
    Enemy.draw(action_window)
    action_window.blit(current_sprite, sprite.locate())
    screen.blit(GROUND_pic, (0, 475))
    Pic_Button.draw_pic_button(box_button, screen)
    
    if WAITING == True and LOSE == False:
        Button.draw(start_button, action_window, True)
        Button.draw(exit_button, action_window,  True)
        
    if gameplay == True:
        InfoPanel.draw(coin_panel, screen)
        InfoPanel.draw(potion_panel, screen)
        InfoPanel.draw(level_info, screen,  False)
        screen.blit(COIN_pic, (229, 2))
        screen.blit(POTION_pic, (359, 0))
        InfoPanel.draw(time_panel, screen,  True)
        InfoPanel.draw(score_panel, screen,  True)


        #draw only if game is on PAUSE
        if PAUSE == True:
            action_window.blit(PAUSE_pic, (100, 180))
            start_button.waiting_in_new_position(30, 260)
            exit_button.waiting_in_new_position(260, 260)
            Button.draw(start_button, action_window, True)
            Button.draw(exit_button, action_window,  True)
            
        #draw life hearts
        if LIFE_COUNTER == 3:
            screen.blit(LIFE_pic, (4, 0))
            screen.blit(LIFE_pic, (33, 0))
            screen.blit(LIFE_pic, (62, 0))
        elif LIFE_COUNTER == 2:
            screen.blit(LIFE_pic, (4, 0))
            screen.blit(LIFE_pic, (33, 0))
        elif LIFE_COUNTER == 1:
            screen.blit(LIFE_pic, (4, 0))
            
    #draw only if U lose        
    if LOSE == True:                                
        action_window.blit(U_LOSE_pic, (0, 0))
        start_button.waiting_in_new_position(30, 260)
        exit_button.waiting_in_new_position(260, 260)
        Button.draw(start_button, action_window, True)
        Button.draw(exit_button, action_window,  True)
        if NEW_RECORD:
            new_record.update(new_record_score)
            InfoPanel.draw(new_record, action_window,  True)
        else:
            InfoPanel.draw(total_score, action_window,  True)
            record.update(prev_record)
            InfoPanel.draw(record, action_window,  True)
            
    screen.blit(action_window, (0, 25))
    pygame.display.update()
