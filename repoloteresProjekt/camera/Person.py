from random import randint

class MyPerson:
    tracks = []

    def __init__(self, i, xi, yi, max_age):
        # Szemely azonositoja
        self.i = i
        # Kezdeti koordináták
        self.x = xi
        self.y = yi
        # Nyomvonalak
        self.tracks = []
        # Véletlenszerű szín
        self.R = randint(0, 255)
        self.G = randint(0, 255)
        self.B = randint(0, 255)
        # Állapotok
        self.done = False
        self.state = '0'
        # Életkor és maximális életkor
        self.age = 0
        self.max_age = max_age
        # Irány
        self.dir = None

    def getRGB(self):
        return (self.R, self.G, self.B)

    def getTracks(self):
        return self.tracks

    def getId(self):
        return self.i

    def getState(self):
        return self.state

    def getDir(self):
        return self.dir

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def updateCoords(self, xn, yn):
        # Életkor nullázása
        self.age = 0
        # Nyomvonalak frissítése
        self.tracks.append([self.x, self.y])
        # Új koordináták beállítása
        self.x = xn
        self.y = yn

    def setDone(self):
        self.done = True

    def timedOut(self):
        return self.done

    def going_UP(self, mid_start, mid_end):
        if len(self.tracks) >= 2:
            if self.state == '0':
                if (
                    self.tracks[-1][1] < mid_end
                    and self.tracks[-2][1] >= mid_end
                ):  # Áthalad a felső vonalon
                    self.state = '1'
                    self.dir = 'up'
                    return True
            else:
                return False
        else:
            return False

    def going_DOWN(self, mid_start, mid_end):
        if len(self.tracks) >= 2:
            if self.state == '0':
                if (
                    self.tracks[-1][1] > mid_start
                    and self.tracks[-2][1] <= mid_start
                ):  # Áthalad az alsó vonalon
                    self.state = '1'
                    self.dir = 'down'
                    return True
            else:
                return False
        else:
            return False

    def age_one(self):
        # Életkor növelése
        self.age += 1
        # Ha a maximális életkor elérve, befejezettnek jelölés
        if self.age > self.max_age:
            self.done = True
        return True

class MultiPerson:
    def __init__(self, persons, xi, yi):
        # Személyek listája
        self.persons = persons
        # Kezdeti koordináták
        self.x = xi
        self.y = yi
        # Nyomvonal
        self.tracks = []
        # Véletlenszerű szín
        self.R = randint(0, 255)
        self.G = randint(0, 255)
        self.B = randint(0, 255)
        # Befejezettség állapota
        self.done = False