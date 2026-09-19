import pygame
from testy import Tile
import numpy as np
import random

table_possible = np.zeros((10, 10), dtype=np.int16)
table_computer = np.zeros((10, 10), dtype=np.int16)
table_shooting = np.zeros((10, 10), dtype=np.int16)

ships = [4, 3, 3, 2, 2, 2]
active_ship = 0
good_tiles = []
x1, y1 = None, None  # Počáteční souřadnice aktuálně stavěné lodi

pygame.init()
screen = pygame.display.set_mode((1100, 500))
clock = pygame.time.Clock()
tiles = set()
tiles2 = set()

for i in range(10):
    for j in range(10):
        t = Tile(pygame.Rect(50 * i+1, 50 * j+1, 48, 48), i, j)
        tiles.add(t)

def placingFirstPart(x, y, table, ship_length):
    if table[x][y] != 0:
        return []

    good_tiles = []

    # Směr dolů (+y)
    if y + ship_length <= 10:
        volno = True
        for i in range(1, ship_length):
            if table[x][y + i] != 0:
                volno = False
                break
        if volno:
            good_tiles.append((x, y + ship_length - 1))

    # Směr nahoru (-y)
    if y - ship_length + 1 >= 0:
        volno = True
        for i in range(1, ship_length):
            if table[x][y - i] != 0:
                volno = False
                break
        if volno:
            good_tiles.append((x, y - ship_length + 1))

    # Směr doprava (+x)
    if x + ship_length <= 10:
        volno = True
        for i in range(1, ship_length):
            if table[x + i][y] != 0:
                volno = False
                break
        if volno:
            good_tiles.append((x + ship_length - 1, y))

    # Směr doleva (-x)
    if x - ship_length + 1 >= 0:
        volno = True
        for i in range(1, ship_length):
            if table[x - i][y] != 0:
                volno = False
                break
        if volno:
            good_tiles.append((x - ship_length + 1, y))

    return good_tiles

def placingSecondPart(x1, y1, x2, y2, active, table):
    ship_length = ships[active]

    if y2 == y1:
        min_x = min(x1, x2)
        max_x = max(x1, x2)
        for i in range(ship_length):
            table[min_x + i][y1] = 1
            if y1 > 0:
                table[min_x + i][y1 - 1] = 3
            if y1 < 9:
                table[min_x + i][y1 + 1] = 3
        if min_x > 0:
            table[min_x - 1][y1] = 3
        if max_x < 9:
            table[max_x + 1][y1] = 3
    else:
        min_y = min(y1, y2)
        max_y = max(y1, y2)
        for i in range(ship_length):
            table[x1][min_y+ i] = 1
            if x1 > 0:
                table[x1 - 1][min_y + i] = 3
            if x1 < 9:
                table[x1 + 1][min_y + i] = 3
        if min_y > 0:
            table[x1][min_y - 1] = 3
        if max_y < 9:
            table[x1][max_y + 1] = 3

    return active + 1

def computerPlacing():
    for ship_idx in range(len(ships)):
        placed = False
        while not placed:
            rx = random.randint(0, 9)
            ry = random.randint(0, 9)
            
            valid_ends = placingFirstPart(rx, ry, table_computer, ships[ship_idx])
            if valid_ends:
                end_tile = random.choice(valid_ends)
                placingSecondPart(rx, ry, end_tile[0], end_tile[1], ship_idx, table_computer)
                placed = True

    print("Počítač úspěšně položil všechny lodě:")
    print(table_computer)
    for i in range(10):
        for j in range(10):
            t = Tile(pygame.Rect(600 + 50 * i+1, 50 * j+1, 48, 48), i, j)
            tiles2.add(t)


# Hlavní smyčka
computer_placed = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for tile in tiles:
                if tile.rect.collidepoint(event.pos):
                    if not computer_placed:
                        if active_ship < len(ships):
                            if len(good_tiles) == 0:
                                if table_possible[tile.x][tile.y] == 0:
                                    x1, y1 = tile.x, tile.y
                                    good_tiles = placingFirstPart(x1, y1, table_possible, ships[active_ship])
                                    if len(good_tiles) != 0:
                                        tile.value(table_possible, 1)
                                        for gt in good_tiles:
                                            table_possible[gt[0]][gt[1]] = 2
                            else:
                                if (tile.x, tile.y) in good_tiles:
                                    for gt in good_tiles:
                                        table_possible[gt[0]][gt[1]] = 0
                                    active_ship = placingSecondPart(x1, y1, tile.x, tile.y, active_ship, table_possible)
                                    good_tiles = []

                                    # Když hráč dokončí pokládání všech lodí, položí lodě počítač
                                    if active_ship == len(ships) and not computer_placed:
                                        computerPlacing()
                                        computer_placed = True
                    else:
                        if table_computer[tile.x][tile.y] == 1:
                            table_shooting[tile.x][tile.y] = 3
                        else: table_shooting[tile.x][tile.y] = 2
    if computer_placed:
            for tile in tiles2:
                if table_possible[tile.x][tile.y]== 3:
                    table_possible[tile.x][tile.y] = 0
                tile.update(table_possible)
                pygame.draw.rect(screen, tile.color, tile.rect)
                pygame.display.update()
            for tile in tiles:
                tile.update(table_shooting)
                pygame.draw.rect(screen, tile.color, tile.rect)
                pygame.display.update() 
    else:
        for tile in tiles:
            tile.update(table_possible)
            pygame.draw.rect(screen, tile.color, tile.rect)
            pygame.display.update()

    clock.tick(24)