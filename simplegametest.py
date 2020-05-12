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

U_LOSE_pic = pygame.image.load(os.path.join(image_path, 'lose.png'))
U_LOSE_rect = U_LOSE_pic.get_rect()
PAUSE_pic = pygame.image.load(os.path.join(image_path, 'pause.png'))
PAUSE_rect = PAUSE_pic.get_rect()
LIFE_pic = pygame.image.load(os.path.join(image_path, 'heart.png'))
LIFE_rect = LIFE_pic.get_rect()
GROUND_pic = pygame.image.load(os.path.join(image_path, 'ground.png'))

Left  = Eye("left_eye.png", 'left', START_EYE_POS)
Right = Eye("right_eye.png", 'right', START_EYE_POS)

Fire  = Flame("fire_50.png", fire_start_pos, START_ENEMY_SPEED)
Gold  = Coin("coin.png", gold_start_pos, START_ENEMY_SPEED)
Heart = Enemies("red_heart.png", gold_start_pos, START_ENEMY_SPEED)
Enemy = pygame.sprite.Group(Fire, Gold)

start_button = Button(GREEN, 0, 0, 100, 25, 'START')
exit_button  = Button(RED, 400, 0, 100, 25, 'EXIT')

time_panel = InfoPanel('TIME', DARK_GREY,  100, 0, 150, 25, 0, 'TIME')
score_panel = InfoPanel('SCORE', DARK_GREY,  250, 0, 150, 25, 0, 'SCORE')
total_score = InfoPanel('TOTAL_SCORE', RED, 250, 75, 200, 50, 0, 'TOTAL SCORE')
record = InfoPanel('RECORD_SCORE', RED, 250, 150, 200, 50, 0, 'RECORD')
new_record = InfoPanel('RECORD_SCORE', RED, 250, 100, 200, 50, 0, 'NEW RECORD')
level_info = InfoPanel('Level', RED,  200, 0, 100, 25, 0, 'LVL')
coin_panel = InfoPanel('COIN_CHECKER', GRAY, 395, 0, 100, 25, 0, 'COINS')
                                   
current_sprite  = Left.img()
sprite = Left
gameplay = False
TIMER = None
collide = None
GAME = True
LOSE = False
PAUSE = False
level = 1
LIFE_COUNTER = 3

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
            TIMER = pygame.time.get_ticks() #start a time counting
            Enemies.set_start_level(Gold, Fire, Heart) #refresh level to 1 for new start
            score_panel.value = 0
            coin_counter = 0
            level_info.value = 1
            coin_panel.value = 0
            LIFE_COUNTER = 3
            NEW_RECORD = False
            random_heart_int = random.choice(range(10,30))


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
    
    action_window.fill(GRAY)
    Enemy.draw(action_window)
    
    if LOSE == True:                                #draws only if U lose
        action_window.blit(U_LOSE_pic, U_LOSE_rect)
        if NEW_RECORD:
            new_record.update(new_record_score)
            InfoPanel.draw(new_record, action_window,  True)
        else:
            InfoPanel.draw(total_score, action_window,  True)
            record.update(prev_record)
            InfoPanel.draw(record, action_window,  True)
    if PAUSE == True:                               #draws only if game is on PAUSE
        action_window.blit(PAUSE_pic, (100, 180))

    if LIFE_COUNTER == 3:                           #draws life hearts
        action_window.blit(LIFE_pic, (4,3))
        action_window.blit(LIFE_pic, (33,3))
        action_window.blit(LIFE_pic, (62,3))
    elif LIFE_COUNTER == 2:
        action_window.blit(LIFE_pic, (4,3))
        action_window.blit(LIFE_pic, (33,3))
    elif LIFE_COUNTER == 1:
        action_window.blit(LIFE_pic, (4,3))
        
    InfoPanel.draw(coin_panel, action_window,  False)
    InfoPanel.draw(level_info, action_window,  True)
    action_window.blit(GROUND_pic, (0, 450))
    action_window.blit(current_sprite, sprite.locate())
    screen.blit(action_window, (0, 25))
    Button.draw(start_button, screen, True)
    Button.draw(exit_button, screen,  True)
    InfoPanel.draw(time_panel, screen,  True)
    InfoPanel.draw(score_panel, screen,  True)
    pygame.display.update()
