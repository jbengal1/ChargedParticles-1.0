import pygame, sys
pygame.font.init()

if __name__=='__main__':
    sys.path.insert(0, "../")

from Engine.Settings import Settings as SETT
from Visualization.Colors import *

FONT_SIZE = 24

class Text:
    def __init__(self, 
        text='', 
        x=SETT.WIN_WIDTH/2, y=SETT.WIN_HEIGHT/2, 
        color=WHITE, 
        font_settings=('freesansbold.ttf', FONT_SIZE)
        ):
        self.text = text
        self.font = pygame.font.Font(font_settings[0], font_settings[1])
        self.x = x
        self.y = y
        self.color = color
        self.textImg = self.font.render(str(self.text), True, self.color, None)
        self.rectangular = self.textImg.get_rect()
        self.moveIfTouchBoarders()

    def setText(self, text=''):
        self.text = text
    
    def setPosition(self, x, y):
        self.x, self.y = x, y
    
    def moveIfTouchBoarders(self):
        x, y = self.rectangular.x, self.rectangular.y
        weight, height = self.rectangular.w, self.rectangular.h
        if x <= 0:
            self.x += weight/2
        elif x >= SETT.WIN_WIDTH:
            self.x -= weight/2
        if y <= 0:
            self.y += height/2
        elif y > SETT.WIN_HEIGHT:
            self.y -= height/2

    def draw(self, screen):
        self.textImg = self.font.render(str(self.text), True, self.color, None)
        self.rectangular = self.textImg.get_rect()
        self.rectangular.center = (self.x, self.y)
        self.moveIfTouchBoarders()
        screen.blit(self.textImg, self.rectangular)


class TimeText(Text):
    def __init__(self, 
        time=0.0, 
        x=SETT.WIN_WIDTH/2, y=SETT.WIN_HEIGHT/2, 
        color=BRIGHT_BLUE, font_settings=('freesansbold.ttf', FONT_SIZE)
        ):
        super().__init__('', x, y, color, font_settings)
        self.convertTime(time)

    def update(self, time):
        self.convertTime(time)

    def convertTime(self, time):
        time = int(time)
        self.days = time//(3600*24)
        self.hours = (time - self.days*3600*24)//3600
        self.minutes = (time - self.days*3600*24 - self.hours*3600)//60
        self.sec = time - self.days*3600*24 - self.hours*3600 - self.minutes*60
        text_array = [str(self.sec), str(self.minutes), str(self.hours), str(self.days)]
        N = len(text_array)
        for i, t in enumerate(text_array):
            if len(t)==1:
                text_array[i] = "0" + t
        for i in range(N):
            if float(text_array[N-1-i]) == 0:
                text_array.pop()
            else:
                break
        self.text = ":".join(text_array[::-1])
        self.text = "Simulated time: " + self.text

    

class Coordinates(Text):
    def __init__(self, 
        x=SETT.WIN_WIDTH/2, y=SETT.WIN_HEIGHT/2, 
        color=BRIGHT_BLUE, font_settings=('freesansbold.ttf', FONT_SIZE)
        ):
        super().__init__('', x, y, color, font_settings)
        self.text = '({:.2f},  '.format(self.x) + '{:.2f})'.format(self.y)

    def update(self, x, y):
        self.x = x
        self.y = y
        self.text = f'{self.x}, {self.y}'