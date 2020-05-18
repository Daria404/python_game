import sys, pygame, time, random, os,  pickle
from constants import *
from menu import *
from game_objects import *
from tools import *

pygame.init()    # initialize all pygame modules
pygame.display.set_caption("Lancelot's eye")

fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode(SCREEN_SIZE)  #create a new Surface object
## pygame.FULLSCREEN can add to set_mode
coin_menu = pygame.Surface((100, 30))
potion_menu = pygame.Surface((100, 30))
selled_potion_menu = pygame.Surface((210, 60))

(fire_start_pos, gold_start_pos) = set_random_coord()

##group of downloaded surfaces:
U_LOSE_pic = add_image('lose.png')
PAUSE_pic = add_image('pause.png')
LIFE_pic = add_image('heart.png')
GROUND_pic = add_image('ground.png')
COIN_pic = add_image('coin_30.png')
BIG_COIN_pic = add_image('coin.png')
POTION_pic = add_image('water_potion.png')
BIG_POTION_pic = add_image('water_potion_55.png')
BOX_pic = add_image('box.png')
INSIDEbox_pic = add_image('box_window.png')
BUY_pic = add_image('buy_menu.png')
WATER_pic = add_image('water.png')
L_tower_pic = add_image('L_tower.png')
BACKGROUND_pic = add_image('game_background.png')

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
box_button = Pic_Button(BOX_pic, (230, 470))
buy_button = Pic_Button(BUY_pic, (100, 180))

time_panel = InfoPanel('TIME', GRAY,  390, 475, 70, 17, 0, 'TIME')
score_panel = InfoPanel('SCORE', GRAY,  12, 475, 70, 17, 0, 'SCORE')
total_score = InfoPanel('TOTAL_SCORE', RED, 260, 75, 200, 50, 0, 'TOTAL SCORE')
record = InfoPanel('RECORD_SCORE', RED, 260, 150, 200, 50, 0, 'RECORD')
new_record = InfoPanel('RECORD_SCORE', RED, 260, 100, 200, 50, 0, 'NEW RECORD')
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
BUY_POTION = False
TRY_TO_BUY = False
APPLY_WATER_POTION = False
start_water = None
end_water = None

#initial variables:
level = 1
potion_counter = 0
current_time = pygame.time.get_ticks()

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

            if event.key == pygame.K_w and potion_counter>0:
                potion_counter -=1
                potion_panel.update(potion_counter)
                APPLY_WATER_POTION = True
                start_water = pygame.time.get_ticks()//1000
                end_water = start_water + 10
                
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
            BOX = not BOX
            TRY_TO_BUY = False
        elif buy_button.pic_isPressed(event):
            TRY_TO_BUY = True
            if coin_counter >= 50:
                coin_counter -=50
                potion_counter +=1
                coin_panel.update(coin_counter)
                potion_panel.update(potion_counter)
                BUY_POTION = True
            else:
                BUY_POTION = False


    if TIMER:
        result_time = (pygame.time.get_ticks() - TIMER)//1000
        time_panel.update(result_time)  #set new value on the button text


    if gameplay == True and not PAUSE:        #if game process started, every obj can move
        if APPLY_WATER_POTION == True:
            Flame.water_update(Fire)
            Gold.update()
            sprite.update()
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
    screen.blit(BACKGROUND_pic, (0, 0))
    screen.blit(current_sprite, sprite.locate())
    Enemy.draw(screen)
    
    if WAITING == True and LOSE == False:
        Button.draw(start_button, screen, 30, True)
        Button.draw(exit_button, screen,  30, True)
        
    if gameplay == True:            
        InfoPanel.draw(coin_panel, screen, 25)
        InfoPanel.draw(potion_panel, screen, 25)
        InfoPanel.draw(level_info, screen, 25,  False)
        screen.blit(COIN_pic, (225, 2))
        screen.blit(POTION_pic, (359, 0))
        InfoPanel.draw(time_panel, screen, 15, False)
        InfoPanel.draw(score_panel, screen, 15,  False)

        if APPLY_WATER_POTION == True:
            if time_panel.value != end_water:
                create_text(screen, f'0:{end_water - time_panel.value}', (0, 25), 20)
                screen.blit(WATER_pic, (0, 20))
            else:
                APPLY_WATER_POTION = False
                current_time = 0

        #draw only if game is on PAUSE
        if PAUSE == True:
            create_text(screen, 'Press "SPACE" to continue', (55, 100), 25)
            screen.blit(PAUSE_pic, (100, 180))
            start_button.waiting_in_new_position(30, 260)
            exit_button.waiting_in_new_position(260, 260)
            Button.draw(start_button, screen, 30, True)
            Button.draw(exit_button, screen,  30, True)
            
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

        if BOX == True:
            PAUSE = True
            coin_menu.fill(BEIGE)
            potion_menu.fill(LIGHT_BEIGE)
            selled_potion_menu.fill(LIGHT_BEIGE)
            create_text(coin_menu, f'x {coin_counter}', (0, 0), 25)
            create_text(potion_menu, f'x {potion_counter}', (0, 0), 25)
            if TRY_TO_BUY == True:
                if BUY_POTION == True:
                    create_text(selled_potion_menu,
                                f'+1 Water Potion', (10, 0), 20)
                    create_text(selled_potion_menu,
                                f'in Box!', (60, 30), 20)
                else:
                    create_text(selled_potion_menu,
                                f'Need more coins!', (2, 0), 20)
            INSIDEbox_pic.blit(coin_menu,(120, 60))
            INSIDEbox_pic.blit(potion_menu,(120, 120))
            INSIDEbox_pic.blit(selled_potion_menu,(45, 230))
            Pic_Button.draw_pic_button(buy_button, INSIDEbox_pic)
            INSIDEbox_pic.blit(BIG_COIN_pic, (70, 50))
            INSIDEbox_pic.blit(BIG_POTION_pic, (70, 110))
            screen.blit(INSIDEbox_pic, (0, 0))
        else :
            create_background(coin_menu, (100, 30))
            create_background(potion_menu, (100, 30))
            create_background(selled_potion_menu, (210, 60))

    #draw only if U lose        
    if LOSE == True:                                
        start_button.waiting_in_new_position(30, 260)
        exit_button.waiting_in_new_position(260, 260)
        Button.draw(start_button, screen, 30, True)
        Button.draw(exit_button, screen,  30, True)
        screen.blit(U_LOSE_pic, (25, 65))
        if NEW_RECORD:
            new_record.update(new_record_score)
            InfoPanel.draw(new_record, screen, 20, True)
        else:
            InfoPanel.draw(total_score, screen, 20, True)
            record.update(prev_record)
            InfoPanel.draw(record, screen, 20, True)
    pygame.display.update()
