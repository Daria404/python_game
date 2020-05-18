import os

FONT = 'castellar'

SCREEN_HEIGHT = 500
SCREEN_WIDTH = 500

EYE_X_POSITION = 200
EYE_Y_POSITION = 375

START_EYE_POS = (EYE_X_POSITION, EYE_Y_POSITION)
START_ENEMY_SPEED = 5

FPS = 60

SCREEN_SIZE = (SCREEN_WIDTH,SCREEN_HEIGHT)
ACTION_SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT - 50)
MENU_SCREEN_SIZE = (SCREEN_WIDTH, 25)

## COLORS ##

#            R    G    B
GRAY        = (128, 128, 128)
WHITE       = (255, 255, 255)
GREEN       = (63,  122,  77)
RED         = (178,  34,  34)
DARK_GREY   = (100, 100, 100)
BEIGE       = (225, 199, 154)
LIGHT_BEIGE = (225, 202, 160)

current_path = os.path.dirname(__file__) # Where your .py file is located
image_path = os.path.join(current_path, 'images') # The image folder path
