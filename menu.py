import pygame as pg
import random

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
        
    def draw(self,win,outline = None):
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
        
    def update(self,new_value):
        self.value = new_value

        
