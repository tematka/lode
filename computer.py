import random

class ComputerPlaying:
    def __init__(self):
        self.mode = "HUNT" # ukládá stav hry, jestli počitač střílí náhodně a enbo už trefil loď a teď ji chce vystřílet
        self.first_hit = None # souřadnice prvního trefeného pole té lodi
        self.last_hit = None # souřadnice posledního zásahu
        self.direction = None # určuje kterým směrem od prvního trefeného pole loď leží
        self.visited_directions = [] # seznam směrů které již byli vyzkoušené a loď v nich neleží
        self.current_direction = None # aktuálně zkoušený směr lodi

    def shoting(self, table_shots):
        """ funkce rozhoduje zda bude počítač střílet náhodně a nebo už trefil loď a má ji vystřílet
            table_shots - tabulka kde jsou uchované střelia zásahy
        """
        # pokud je aktuální mod hry HUNT tak počítač generuje nahodné souřadnice a pokud do nich zatím nebylo
        #  stříleno, vystřelí tam
        if self.mode == "HUNT":
            while True:
                rx = random.randint(0, 9)
                ry = random.randint(0, 9)
                if table_shots[rx][ry] == 0 or table_shots[rx][ry] == 1:
                    return rx, ry

        # pokud je aktuální mod TARGET jde počítač vystřílet nalezenou loď
        elif self.mode == "TARGET":
            # pokud neznáme jsakým směrem leží loď počítač to zjistí
            if self.direction is None:
                # dáme jako možné směry všechny
                possible_directions = ["UP", "DOWN", "LEFT", "RIGHT"]
                # pro každý směr z těch možných se podívám zda není ještě prozkoumaný a poikud ne a existuje soused 
                # v daném směru do kterého jsme ještě nestříleli tak jako souřadnice políčka do kterého budeme 
                # střílet příšté souřadnice aktuálně najitého políčka
                for direction in possible_directions:
                    if direction not in self.visited_directions:
                        next_x, next_y = self.getNeighbor(self.first_hit[0], self.first_hit[1], direction)
                        if next_x is not None and (table_shots[next_x][next_y] == 0 or table_shots[next_x][next_y] == 1):
                            self.current_direction = direction
                            return next_x, next_y
                        else:
                            self.visited_directions.append(direction)

            # jinak hledáme políčko do kterého budeme střílet jako další pomocí směru ve kterém leží loď
            else:
                # pokud ve směru ve kterém aktuálně hledáme loď leží políčko, do kterého jsme ještě nestříleli 
                # vrátíme jeho souřadnice jako souřadnice políčka do kterého budeme střílet příště
                next_x, next_y = self.getNeighbor(self.last_hit[0], self.last_hit[1], self.direction)
                if next_x is not None and (table_shots[next_x][next_y] == 0 or table_shots[next_x][next_y] == 1):
                    return next_x, next_y
                # pokud v aktuálně prohledávaném směru takové políčko není zkusíme jit na opačný směr od 
                # prvního sestřeleného políčka této lodi
                else:
                    self.direction = self.oppositeDirection(self.direction)
                    next_x, next_y = self.getNeighbor(self.first_hit[0], self.first_hit[1], self.direction)
                    if next_x is not None and (table_shots[next_x][next_y] == 0 or table_shots[next_x][next_y] == 1):
                        self.last_hit = self.first_hit
                        return next_x, next_y
                    # pokud aniu na druhé straně ndeni taové políčko, vyresetujeme směr a souřadnice prvního
                    # políčka lodi a pokračujeme ve střílení
                    else:
                        self.resetToHunt()
                        return self.shoting(table_shots)

    def processResult(self, x, y, hit):
        """ vyhodnocuje střelu
        """
        #pokud je aktuální stav hry HUNT a byla trefená loď je přepnutý režim na TARGET a nastavený první a 
        # poslední zásah na aktuální pole
        if self.mode == "HUNT":
            if hit:
                self.mode = "TARGET"
                self.first_hit = (x, y)
                self.last_hit = (x, y)
                self.direction = None
                self.visited_directions = []

        elif self.mode == "TARGET":
            # pokud byl zásah a zatím nebyl nastavený směr kterým loď vede tak ho podle aktuálně trefeného políčka
            # nastavíme a vrátíme jako poslední trefené to aktuálně trefené
            if hit:
                if self.direction is None:
                    self.direction = self.current_direction
                self.last_hit = (x, y)
            # pokud nebyl zásah a nemáme směr, přidáme aktuální směr do již prohledaných. jinak nastavíme na aktuální
            # směr opačný směr a pokračujeme v hledání na druhou stranu od prvního nalezeného pole
            else:
                if self.direction is None:
                    self.visited_directions.append(self.current_direction)
                else:
                    self.direction = self.oppositeDirection(self.direction)
                    self.last_hit = self.first_hit

    def getNeighbor(self, x, y, direction):
        """ vrací souřadnice sousedního políčka v daném směru pokud existuje
            x, y - souřadnice políčka pro něž hledáme souseda
            direction - směr ve kterém hledáme souseda
        """
        if direction == "UP" and y > 0: return x, y - 1
        if direction == "DOWN" and y < 9: return x, y + 1
        if direction == "LEFT" and x > 0: return x - 1, y
        if direction == "RIGHT" and x < 9: return x + 1, y
        return None, None

    def oppositeDirection(self, direction):
        """ funkce která vrací opačný směr k zadanému směru
        """
        opposites = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
        return opposites.get(direction)

    def resetToHunt(self):
        """ vrátí původní nastavení promenných třídy ComputerPlaying
        """
        self.mode = "HUNT"
        self.first_hit = None
        self.last_hit = None
        self.direction = None
        self.visited_directions = []