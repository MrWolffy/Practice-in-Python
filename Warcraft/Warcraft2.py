warrior_name = ["dragon", "ninja", "iceman", "lion", "wolf"]
weapon_name = ["sword", "bomb", "arrow"]


class Weapon:
    def __init__(self, t):
        self.type = t
        self.typename = weapon_name[t]


class Sword (Weapon):
    def __init__(self, t):
        Weapon.__init__(self, t)


class Bomb (Weapon):
    def __init__(self, t):
        Weapon.__init__(self, t)


class Arrow (Weapon):
    def __init__(self, t):
        Weapon.__init__(self, t)


def makeWeapon(t):
    if t == 0: return Sword(0)
    elif t == 1: return Bomb(1)
    elif t == 2: return Arrow(2)


class Warrior:
    def __init__(self, t = 0, s = 0):
        self.type = t
        self.strength = s
        global warrior_name
        self.name = warrior_name[t]


class Dragon (Warrior):
    def __init__(self, t, s, e, n):
        Warrior.__init__(self, t, s)
        self.morale = (e - s) / s
        self.wp = makeWeapon((n + 1) % 3)

    def printInfo(self):
        print("It has a", self.wp.typename, ",and it's morale is", format(self.morale, ".2f"))


class Ninja (Warrior):
    def __init__(self, t, s, e, n):
        Warrior.__init__(self, t, s)
        self.wp1 = makeWeapon((n + 1) % 3)
        self.wp2 = makeWeapon((n + 2) % 3)

    def printInfo(self):
        print("It has a", self.wp1.typename, "and a", self.wp2.typename)


class Iceman (Warrior):
    def __init__(self, t, s, e, n):
        Warrior.__init__(self, t, s)
        self.wp = makeWeapon((n + 1) % 3)

    def printInfo(self):
        print("It has a", self.wp.typename);


class Lion (Warrior):
    def __init__(self, t, s, e, n):
        Warrior.__init__(self, t, s)
        self.loyalty = e - s

    def printInfo(self):
        print("It's loyalty is", self.loyalty)


class Wolf (Warrior):
    def __init__(self, t, s, e, n):
        Warrior.__init__(self, t, s)


class Headquarter:
    def __init__(self, m, order):
        self.type = 0
        self.element = m
        self.order = order
        self.count = [0] * 5
        self.stop = False
        self.now = 0
        self.warNum = 0
        self.warriors = [Warrior()] * 1000
        self.typename = ""

    def printWarInfo(self, time, tmp, elements):
        print(format(time, "03d"), self.typename, warrior_name[tmp], self.warNum + 1, "born with strength", self.warriors[self.warNum].strength, end=",")
        print(self.count[tmp], warrior_name[tmp], "in", self.typename, "headquarter")
        self.warNum = self.warNum + 1

    def makeWarrior(self, time, elements):
        if self.stop: return
        i = 0
        while i < 5:
            tmp = self.order[(self.now + i) % 5]
            if elements[tmp] <= self.element:
                self.count[tmp] = self.count[tmp] + 1
                if tmp == 0:
                    self.warriors[self.warNum] = Dragon(tmp, elements[tmp], self.element, self.warNum)
                    self.printWarInfo(time, tmp, elements)
                    self.warriors[self.warNum-1].printInfo()
                elif tmp == 1:
                    self.warriors[self.warNum] = Ninja(tmp, elements[tmp], self.element, self.warNum)
                    self.printWarInfo(time, tmp, elements)
                    self.warriors[self.warNum - 1].printInfo()
                elif tmp == 2:
                    self.warriors[self.warNum] = Iceman(tmp, elements[tmp], self.element, self.warNum)
                    self.printWarInfo(time, tmp, elements)
                    self.warriors[self.warNum - 1].printInfo()
                elif tmp == 3:
                    self.warriors[self.warNum] = Lion(tmp, elements[tmp], self.element, self.warNum)
                    self.printWarInfo(time, tmp, elements)
                    self.warriors[self.warNum - 1].printInfo()
                elif tmp == 4:
                    self.warriors[self.warNum] = Wolf(tmp, elements[tmp], self.element, self.warNum)
                    self.printWarInfo(time, tmp, elements)
                self.element = self.element - elements[tmp]
                self.now = (self.now + i + 1) % 5
                break
            i = i + 1
        if i == 5:
            self.stop = True
            print(format(time, "03d"), self.typename, "headquarter stops making warriors")


# 开始
t = int(input())
order_red = [2, 3, 4, 1, 0]; order_blue = [3, 0, 1, 2, 4]
for case in range(1, t + 1):
    print("Case:", case, sep="")
    m = int(input())
    elements = list(input().split(" "))
    time = 0
    for i in range(0, elements.__len__()):
        elements[i] = int(elements[i])
    red = Headquarter(m, order_red); blue = Headquarter(m, order_blue)
    red.type = 0; blue.type = 1
    red.typename = "red"; blue.typename = "blue"
    while not red.stop or not blue.stop:
        red.makeWarrior(time, elements)
        blue.makeWarrior(time, elements)
        time = time + 1
