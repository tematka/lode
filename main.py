import pygame
from testy import Tile
import numpy as np
import random

table_possible = np.zeros((10,10),dtype=np.int16)
table_computer = np.zeros((10,10),dtype=np.int16)

ships = [4,3,3,2,2,2]
active_ship = 0
good_tiles=[]
x = None
y = None

pygame.init()
screen=pygame.display.set_mode((500,500))
clock = pygame.time.Clock()
tiles = set()
for i in range(10):
    for j in range(10):
        x = Tile(pygame.Rect(50*i,50*j,50,50),i,j)
        tiles.add(x)

def placingFirstPart(x,y,table):
        not_placed = True
        ship_lenght = ships[active_ship]
        good_tiles = []
        while not_placed:
            if table[x][y] == 0:
                not_placed = False
        ok = True
        try:
            for i in range(1,ship_lenght):
                if table[x][y+i] != 0:
                    ok = False
            if ok:
                good_tiles.append((x,y+ship_lenght-1))
        except LookupError:
            pass
        ok = True
        for i in range(1,ship_lenght):
            if table[x][y-i] != 0:
                ok = False
            if y-i<0:
                ok = False
        if ok:
            good_tiles.append((x,y-ship_lenght+1))
        ok = True
        try:
            for i in range(1,ship_lenght):
                if table[x+i][y] != 0:
                    ok = False
            if ok:
                good_tiles.append((x+ship_lenght-1,y))
        except LookupError:
            pass
        ok = True
        for i in range(1,ship_lenght):
            if table[x-i][y] != 0:
                ok = False
            if x-i<0:
                ok = False
        if ok:
            good_tiles.append((x-ship_lenght+1,y))
        return good_tiles

def placingSecondPart(x2,y2,active,table):
    ship_lenght = ships[active]
    if y2 == y:
        if x > x2:
            for i in range(ship_lenght):
                table[x-i][y] = 1
                if y != 0:
                    table[x-i][y-1] = 3
                if y != 9:
                    table[x-i][y+1] = 3
            if x != 9:
                table[x+1][y] = 3
            if x-ship_lenght+1 != 0:
                table[x-ship_lenght][y] = 3
                
        else:
            for i in range(ship_lenght):
                table[x+i][y] = 1
                if y != 0:
                    table[x+i][y-1] = 3
                if y != 9:
                    table[x+i][y+1] = 3
            if x != 0:
                table[x-1][y] = 3
            if x+ship_lenght-1 != 9:
                table[x+ship_lenght][y] = 3
    else:
        if y > y2:
            for i in range(ship_lenght):
                table[x][y-i] = 1
                if x != 0:
                    table[x-1][y-i] = 3
                if x != 9:
                    table[x+1][y-i] = 3
            if y != 9:
                table[x][y+1] = 3
            if y-ship_lenght+1 != 0:
                table[x][y-ship_lenght] = 3

        else:
            for i in range(ship_lenght):
                table[x][y+i] = 1
                if x != 0:
                    table[x-1][y+i] = 3
                if x != 9:
                    table[x+1][y+i] = 3
            if y != 0:
                table[x][y-1] = 3
            if y+ship_lenght-1 != 9:
                table[x][y+ship_lenght] = 3
    if active < 5:
        return active + 1
    else:
        return active

def computerPlacing():
    active_comp = 0
    good_comp = []
    for i in range(3):
        x_comp = random.randint(0,9)
        y_comp = random.randint(0,9)
        if len(good_comp) == 0:
            good_comp = placingFirstPart(x_comp,y_comp,table_computer)
        else:
            r = random.randint(0, len(good_comp)-1)
            end_of_ship = good_comp[r]
            placingSecondPart(end_of_ship[0],end_of_ship[1],active_comp,table_computer)
            del good_comp[:]

    print(table_computer)



while True:
    for tile in tiles:
        tile.update(table_possible)
        pygame.draw.rect(screen, tile.color, tile.rect)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for tile in tiles:
                if tile.rect.collidepoint(event.pos):
                    if table_possible[tile.x][tile.y] == 0 or table_possible[tile.x][tile.y] == 2:
                        if len(good_tiles) == 0:
                            x, y = tile.x,tile.y
                            good_tiles = placingFirstPart(x,y,table_possible)
                            if len(good_tiles) != 0:
                                tile.value(table_possible,1)

                                for good_tile in good_tiles:
                                    table_possible[good_tile[0]][good_tile[1]] = 2
                        else:
                            if (x2 := tile.x,y2 :=tile.y) in good_tiles:
                                for good_tile in good_tiles:
                                    table_possible[good_tile[0]][good_tile[1]] = 0
                                active_ship = placingSecondPart(x2,y2,active_ship,table_possible)
                                good_tiles= []
                                if active_ship >= 1:
                                    computerPlacing()
                                    print("hura")

    clock.tick(24)


