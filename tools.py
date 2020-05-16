import random
import pickle
import pygame
import os
from constants import *

pygame.init()

def set_random_coord():
    flag = True 
    while flag == True:
        coord = []
        for i in range(2):
            x = random.randrange(50, 450)
            y = random.randrange(-250, -50)
            coord.append((x,y))
        if abs(coord[0][0] - coord[1][0]) < 100:
            flag = True
        else: flag = False
        
    return coord


def open_score_list():
    # load the previous score if it exists
    try:
        with open('score.dat', 'rb') as file:
            score = pickle.load(file)
    except:
        score = [0]
    return score    


def score_to_list(result):
    scores = open_score_list()
    scores.append(result)
    # save the score
    with open('score.dat', 'wb') as file:
        pickle.dump(scores, file)
        
    return scores


def clear_score_list():
    with open('score.dat', "w"):
        pass

    
def record_res():
    score_list = open_score_list()
    return max(score_list)

def add_image(filename):
    image = pygame.image.load(os.path.join(image_path, filename))
    return image

def create_text(surf, text, location):
    myfont = pygame.font.SysFont('Comic Sans MS', 25)
    textsurface = myfont.render(text, False, (0, 0, 0))
    surf.blit(textsurface, location)

def create_background(background, size):
    background = pygame.Surface(size)
    background.set_alpha(50)

    
