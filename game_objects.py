import pygame as pg
import random
from constants import *
import os

class Eye(pg.sprite.Sprite):
    def __init__(self, filename, direction, location):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(image_path, filename))
        self.rect = self.image.get_rect(topleft = location)
        self.direction = direction

    def update(self):
        keys =  pg.key.get_pressed()
        if keys[pg.K_LEFT] and self.rect.left >= 0 :
            self.rect.left -= 8
            self.direction = 'left'
        elif keys[pg.K_RIGHT] and self.rect.right <= 500:
            self.rect.right += 8
            self.direction = 'right'

    def img(self):
        return self.image

    def locate(self):
        return self.rect

class Enemies(pg.sprite.Sprite):
    def __init__(self, filename, location, speed, alive = None):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(image_path, filename))
        self.rect = self.image.get_rect(topleft = location)
        self.speed = speed
        self.alive = True

    def update(self):
        if self.rect.top < 500:
            self.rect.bottom +=self.speed 
        else:
            self.alive = False
            self.kill()

    def is_killed(self):
        if self.alive == False:
            return True

    def level_up(*args):
        for self in args:
            self.speed +=2
        
    def set_start_level(*args):
        for self in args:
            self.speed = START_ENEMY_SPEED
            

class Flame(Enemies):
    def __init__(self, filename, location, speed):
        super().__init__(filename, location, speed)

    def water_update(self):
        if self.rect.top < 100:
            self.rect.bottom +=self.speed 
        else:
            self.alive = False
            self.kill()


class Coin(Enemies):
    def __init__(self, filename, location, speed):
        super().__init__(filename, location, speed)
