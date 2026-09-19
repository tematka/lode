import pygame


class Tile():
    def __init__(self,rect:pygame.Rect,x=None,y=None,color=(255,255,255)):
        self.color = color
        self.rect = rect
        self.x = x
        self.y = y
    def update(self,table):
        if table[self.x][self.y] == 0:
            self.color = "white"
        elif table[self.x][self.y] == 1:
            self.color = "green"
        elif table[self.x][self.y] == 2:
            self.color = "blue"
        elif table[self.x][self.y] == 3:
            self.color = "red"
    def value(self,table,value:int):
        table[self.x][self.y] = value
