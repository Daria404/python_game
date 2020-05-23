import pygame as pg
import random
from constants import FONT

class Button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win, font_size, outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pg.draw.rect(win, outline,
                             (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pg.draw.rect(win, self.color,
                         (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pg.font.SysFont(FONT, font_size)
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

    def waiting_in_new_position(self, new_location):
        self.x = new_location[0]
        self.y = new_location[1]
        

class Pic_Button(Button):
    def __init__(self, pic, location, active):
        self.image = pic
        self.location = location
        self.rect = self.image.get_rect(topleft = location)
        self.active = False

    def draw_pic_button(self, win):
        win.blit(self.image, self.location)

    def pic_isPressed(self, event):
        if self.active == True:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    if self.rect.collidepoint(event.pos): 
                        return True
        elif self.active == False: return None
        
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
        
    def draw(self, win, font_size, outline = None, only_value = None):
        if outline:
            pg.draw.rect(win, outline,
                             (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pg.draw.rect(win, self.color,
                         (self.x,self.y,self.width,self.height),0)

        font = pg.font.SysFont(FONT, font_size)
        if only_value == 1:
            text = font.render(f'{str(self.value)}', 1, (0,0,0))
        elif only_value == 2 :
            text = font.render(f'{self.text}:', 1, (0,0,0))
        else:
            text = font.render(f'{self.text}:{str(self.value)}', 1, (0,0,0))
        win.blit(text, (self.x + (self.width/2 - text.get_width()/2),
                            self.y + (self.height/2 - text.get_height()/2)))        
        
    def update(self,new_value):
        self.value = new_value

    
        
