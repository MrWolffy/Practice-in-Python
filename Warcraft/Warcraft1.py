warrior_name = ["dragon", "ninja", "iceman", "lion", "wolf"]


class Warrior:
    def __init__(self, t = 0, s = 0):
        self.type = t
        self.strength = s
        global warrior_name
        self.name = warrior_name[t]


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
    def makeWarrior(self, time, elements):
        if self.stop: return
        print(format(time, "03d"), end=" ")
        print(self.typename, end=" ")
        i = 0
        while i < 5:
            tmp = self.order[(self. now +i) % 5]
            if elements[tmp] <= self.element:
                self.warriors[self.warNum] = Warrior(tmp, elements[tmp])
                self.element -= elements[tmp]
                self.count[tmp] = self.count[tmp] + 1
                print(self.warriors[self.warNum].name, self.warNum + 1, "born with strength", self.warriors[self.warNum].strength, sep=" ", end=",")
                print(self.count[tmp], self.warriors[self.warNum].name, "in", self.typename, "headquarter", sep=" ", end="\n")
                self.warNum = self.warNum + 1
                self.now = (self.now + i + 1) % 5
                return
            i = i + 1
        if i == 5:
            self.stop = True
            print("headquarter stops making warriors", end="\n")


# 开始
t = int(input())
order_red = [2, 3, 4, 1, 0]; order_blue = [3, 0, 1, 2, 4]
for case in range(1, t + 1):
    print("Case:", case, sep=" ")
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
