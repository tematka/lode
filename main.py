import pygame
from tile import Tile
from computer import ComputerPlaying
import numpy as np
import random 

table_player = np.zeros((10, 10), dtype=np.int16) # tabulka do které hráč umisťuje lodě
table_computer = np.zeros((10, 10), dtype=np.int16) # tabulka do které počítač umisťuje lodě
table_shooting = np.zeros((10, 10), dtype=np.int16) # tabulka do které hráč střílí
table_computer_shooting = np.zeros((10, 10), dtype=np.int16) # tabulka do které počítač střílí
computer_placed = False # počítač nemá položené lodě

ships = [4, 3, 3, 2, 2, 2] # pole které udává délky lodí, v pořadí v jakém jsou umisťovány
active_ship = 0 # index kolikátá loď v poli ships je zrovna umisťována
good_tiles = [] # list koncových polí aktuálně stavěné lodi
x1, y1 = None, None  # počáteční souřadnice aktuálně stavěné lodi
ship_computer_count = 6
ship_player_count = 6

pygame.init() #spustí pygame
screen = pygame.display.set_mode((1100, 500)) # obrazovka
clock = pygame.time.Clock() # časovač
tiles_left = set() # levé hrací pole
tiles_right = set() # pravé hrací pole

#vygeneruje levou tabulku 10 x 10
for i in range(10):
    for j in range(10):
        tile = Tile(pygame.Rect(50 * i + 1, 50 * j + 1, 48, 48), i, j)
        tiles_left.add(tile)

computer = ComputerPlaying() #instance té třídy ComputerPlaying

def isShipSunk(x, y, ship_board, shot_board):
    """ kontroluje, jestli je loď potopená
        x, y - souřadnice střeleného políčka
        ship_board - tabulka ve které jsou umístěné lodě
        shot_board - tabulka do které střílí
        pokud je loď potopená vrací true a seznam polí na kterých leží, jinak vrací false a prázdný seznam
    """
    visited = set() # množina již zkontrolovaných políček
    to_visit = [(x, y)] #zásobník políček co jsou potřeba ještě navštívit
    
    while to_visit:
        current_x, current_y = to_visit.pop() # aktuálně zkoumané políčko smaže z těch co jsou potřeba prozkoumat
        visited.add((current_x, current_y)) # přidá aktuální políčko do navštívených

        #pokud aktuální políčko není trefené tak jsme našli nepotopenou část lodi a proto je loď nepotopená
        if shot_board[current_x][current_y] != 3:
            return False, []

        #pro dané políčko se vždy podívá na 4 okolní políčka, zkontroluje, zda jejich indexy stálel leží v tabulce
        # a poté pokud je na ěm loď a ještě nebylo zkontrolované tak ho přidá do seznamu na zkontrolování    
        for plus_x, plus_y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_x, next_y = current_x + plus_x, current_y + plus_y
            if 0 <= next_x < 10 and 0 <= next_y < 10:
                if ship_board[next_x][next_y] == 1 and (next_x, next_y) not in visited:
                    to_visit.append((next_x, next_y))

    #pokud se nenašlo nesestřelené pole lodi tak vrátí, že loď byla sestřelená a seznam jejich polí               
    return True, list(visited) 

def markSurroundingMisses(ship_tiles, shot_board):
    """ okolní políčka potopené lodi zaznačí jakože na nich neleží loď
        ship_tiles - seznam políček na kterých leží potopená loď
        shot_board - tabulka do které se provádí střeli a zaznamenávají se tam trefy  
    """
    # pro každé políčko zkontroluje jeho 4 sousedy jestli jejich idexy leží ještě v tabulce a pokud ano tak pokud
    # je v tabulce střel jejich hodnota 0 (čili neleží tam loď) tak hodnotu přepíše na 2 (neleží tam loď a nemůže
    # tam ležet)
    for tail_ship_x, tail_ship_y in ship_tiles:
        for plus_x, plus_y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_x, next_y = tail_ship_x + plus_x, tail_ship_y + plus_y
            if 0 <= next_x < 10 and 0 <= next_y < 10:
                if shot_board[next_x][next_y] == 0:
                    shot_board[next_x][next_y] = 2  # Voda

def placingFirstPart(x, y, table, ship_length):
    """funkce pro pokládání prvního políčka lodi
        x,y - souřadnice kam se hráč snaží umístit první pole lodi
        table - tabulka do které se umisťuje loď 
        ship_lenght - délka aktuálně umisťované lodi
        funkce vrací seznam polí kde může končit aktuálně umisťovaná loď 
    """
    # pokud není dané políčko volné (již je tam umístěna loď nebo to s lodí sousedí) loď nelze umístit a vrátí to 
    # prázdný seznam políček ke může končit loď
    if table[x][y] != 0:
        return []

    good_tiles = [] #seznam polí kde může končit loď

    # zkontroluje jestli jde loď umístit na pravo od prvního políčka (jestli se do tabulky vejde a jestli jsou 
    # všechna políčka kam by byla loď umístěná volná)
    if y + ship_length <= 10:
        volno = True
        for i in range(1, ship_length):
            if table[x][y + i] != 0:
                volno = False
                break
        if volno:
            good_tiles.append((x, y + ship_length - 1)) # pokud jde vloží koncové políčko v tomto smětu do možných polí

    # zkontroluje, zda jde loď umístit nalevo
    if y - ship_length + 1 >= 0:
        volno = True
        for i in range(1, ship_length):
            if table[x][y - i] != 0:
                volno = False
                break
        if volno:
            good_tiles.append((x, y - ship_length + 1))

    #zkontroluje zda jde loď umístit nahodu
    if x + ship_length <= 10:
        volno = True
        for i in range(1, ship_length):
            if table[x + i][y] != 0:
                volno = False
                break
        if volno:
            good_tiles.append((x + ship_length - 1, y))

    # zkontroluje zda jde loď umístit dolů
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
    """ funkce umisťujre loď 
        x1, y1 -  souřadnice počátečního políčka lodi
        X2, Y2 - souřadnice konečného políčka lodi
        active - aktuální loď kterou pokládáme
        table - tabulka do které se pokládá loď
    """
    ship_length = ships[active] #délka aktuálně pokládané lodi

    # pokud mají obě pole stejnou y souřadnici, tak zvolíme minimální a maximální x souřadnici
    # pak jedeme od min po max a pokládáme loď a zároveň okolní pole zaznačíme jakože na nich nesmí být položená loď
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

    # pokud mají obě stejnou x souřadnici, tak zvolíme minimální a maximální y souřadnici
    # pok jedeme od min po max a pokládáme loď a zároveň okolí pole zaznačíme jakože na nich nesmí být položená loď 
    else:
        min_y = min(y1, y2)
        max_y = max(y1, y2)
        for i in range(ship_length):
            table[x1][min_y + i] = 1
            if x1 > 0:
                table[x1 - 1][min_y + i] = 3
            if x1 < 9:
                table[x1 + 1][min_y + i] = 3
        if min_y > 0:
            table[x1][min_y - 1] = 3
        if max_y < 9:
            table[x1][max_y + 1] = 3

    return active + 1 #posuneme index aktivní lodi o 1

def computerPlacing():
    """ pokládání lodí počítačem
    """
    # položí takto každou loď ze seznamu lodí
    for ship_index in range(len(ships)):

        # dokud není loď uspěšně položená
        placed = False
        while not placed:
            #vygeneruje nahodně sořadnice prvního políčka
            rx = random.randint(0, 9)
            ry = random.randint(0, 9)

            # projde stejným pokládacím procesem jako hráč pomocí fcí placingFirstPart a placingSecondPart
            valid_ends = placingFirstPart(rx, ry, table_computer, ships[ship_index])
            if valid_ends:
                end_tile = random.choice(valid_ends)
                placingSecondPart(rx, ry, end_tile[0], end_tile[1], ship_index, table_computer)
                placed = True
    for i in range(10):
        for j in range(10):
            tile = Tile(pygame.Rect(600 + 50 * i+1, 50 * j+1, 48, 48), i, j)
            tiles_right.add(tile)
            if table_player[i][j] == 1:
                table_computer_shooting[i][j] = 1
            

# hlavní smyčka
while True:
    for event in pygame.event.get(): #zkoumá všechny události co se dějou
        # když se zavře okno, končí program
        if event.type == pygame.QUIT:
            raise SystemExit
        # kontroluje kliknutí myši
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for tile in tiles_left: # projde všechna políčka v levé tabulce
                if tile.rect.collidepoint(event.pos): # kontroluje jestli bylo kliknuto na tohle políčko
                    if not computer_placed: #kontroluje jestli se ještě pokládají lodě
                        if active_ship < len(ships):
                            if len(good_tiles) == 0: #pokud nemá žádná konečná políčka tak hráč pokládá první políčko aktuální lodi
                                if table_player[tile.x][tile.y] == 0:
                                    x1, y1 = tile.x, tile.y
                                    good_tiles = placingFirstPart(x1, y1, table_player, ships[active_ship])
                                    if len(good_tiles) != 0:
                                        tile.value(table_player, 1)
                                        for gt in good_tiles:
                                            table_player[gt[0]][gt[1]] = 2
                            else: # jinak pokládá konečné políčko lodě a vyprázdní seznam konečných políček
                                if (tile.x, tile.y) in good_tiles:
                                    for gt in good_tiles:
                                        table_player[gt[0]][gt[1]] = 0
                                    active_ship = placingSecondPart(x1, y1, tile.x, tile.y, active_ship, table_player)
                                    good_tiles = []

                                    # pokud hráč položil všechny lodě a ještě nepokládal počítač, položí lodě počítač
                                    if active_ship == len(ships) and not computer_placed:
                                        computerPlacing()
                                        computer_placed = True
                    else: #pokud jsou položeny všechny lodě tak následuje střílení
                        if table_shooting[tile.x][tile.y] == 0: #pouze pokud člověk střílí do políčka kam zatím nestřílel
                            if table_computer[tile.x][tile.y] == 1: #pokud trefená loď
                                table_shooting[tile.x][tile.y] = 3
                                # kontrola, zda hráč potopil loď
                                sunk, ship_tiles = isShipSunk(tile.x, tile.y, table_computer, table_shooting)
                                # pokud je loď potopená označíme okolí jako vodu
                                if sunk:
                                    markSurroundingMisses(ship_tiles, table_shooting)
                                    ship_computer_count -= 1
                                    if ship_computer_count == 0:
                                        print("Hráč vyhrál")
                                        raise SystemExit
                            else: # zaznamená že hráč minul
                                table_shooting[tile.x][tile.y] = 2  # Voda

                            #souřadnice kam počítač vystřelil
                            computer_x, computer_y = computer.shoting(table_computer_shooting)

                            # pokud se počítač trefil
                            if table_player[computer_x][computer_y] == 1:
                                table_computer_shooting[computer_x][computer_y] = 3
                                computer.processResult(computer_x, computer_y, True)

                                #pokud je potopená celá loď označí okolí jako vodu
                                sunk, ship_tiles = isShipSunk(computer_x, computer_y, table_player, table_computer_shooting)
                                if sunk:
                                    markSurroundingMisses(ship_tiles, table_computer_shooting)
                                    ship_player_count -= 1
                                    if ship_player_count == 0:
                                        print("Počítač vyhrál")
                                        raise SystemExit
                                    computer.resetToHunt()
                            else:
                                #pokud netrefil zaznačí vodu
                                table_computer_shooting[computer_x][computer_y] = 2
                                table_player[computer_x][computer_y] = 2
                                computer.processResult(computer_x, computer_y, False)

    # aktualizuje obraz na okně podle toho ve které fázi hry hráč je
    if computer_placed: #pokud hráč střílí
        for tile in tiles_left:
            tile.update(table_shooting)
            pygame.draw.rect(screen, tile.color, tile.rect)
        for tile in tiles_right:
            tile.update(table_computer_shooting)
            pygame.draw.rect(screen, tile.color, tile.rect)
        pygame.display.update() 
    else: # pokud hráč pokládá lodě
        for tile in tiles_left:
            tile.update(table_player)
            pygame.draw.rect(screen, tile.color, tile.rect)
            pygame.display.update()

    clock.tick(24)