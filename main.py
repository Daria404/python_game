import pygame as pg
import random

class Eye(pg.sprite.Sprite):
    def __init__(self, filename, direction, location):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(filename)
        self.rect = self.image.get_rect(topleft = location)
        self.direction = direction

    def update(self):
        keys =  pg.key.get_pressed()
        if keys[pg.K_LEFT] and self.rect.left >= 0 :
            self.rect.left -= 4
            self.direction = 'left'
        elif keys[pg.K_RIGHT] and self.rect.right <= 500:
            self.rect.right += 4
            self.direction = 'right'
        
    def get_w(self):
        return self.image.get_width()
    
    def get_h(self):
        return self.image.get_height()

    def img(self):
        return self.image

    def locate(self):
        return self.rect

class Flame(pg.sprite.Sprite):
    def __init__(self, filename, location):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(filename)
        self.rect = self.image.get_rect(topleft = location)

    def update(self):
        if self.rect.top < 500:
            self.rect.bottom +=2
        else: self.kill()

    def locate(self):
        return self.rect

    def img(self):
        return self.image

class Coin(pg.sprite.Sprite):
    def __init__(self, filename, location):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(filename)
        self.rect = self.image.get_rect(topleft = location)

    def update(self):
        if self.rect.top < 500:
            self.rect.bottom +=2
        else: self.kill()

    def locate(self):
        return self.rect

    def img(self):
        return self.image    


class Button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pg.draw.rect(win, outline,
                             (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pg.draw.rect(win, self.color,
                         (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pg.font.SysFont('comicsans', 30)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2),
                            self.y + (self.height/2 - text.get_height()/2)))

    def isPressed(self, pos):
        pressed = pg.mouse.get_pressed()
        flag = False
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                flag = True    
        else: flag = False
        if flag and pressed[0]: return True

class InfoPanel():
    def __init__(self, name, color, x, y, width, height, value, text=''):
        self.name = name
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.value = value
        
    def draw(self,win,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pg.draw.rect(win, outline,
                             (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pg.draw.rect(win, self.color,
                         (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pg.font.SysFont('comicsans', 30)
            text = font.render(f'{self.text}:{str(self.value)}', 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2),
                            self.y + (self.height/2 - text.get_height()/2)))        
        
    def update(self,TIME):
        self.value = TIME
