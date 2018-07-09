from math import floor

warrior_name = ["dragon", "ninja", "iceman", "lion", "wolf"]
weapon_name = ["sword", "bomb", "arrow"]
headquarter_name = ["red", "blue"]


class City:
    def __init__(self, n):
        self.id = n
        self.element = 0
        self.flag = -1
        self.red = None
        self.blue = None
        self.red2 = None
        self.blue2 = None
        self.now = -1
        self.count = 0

    def warGetElement(self, time):
        if self.red is not None and self.blue is None:
            self.red.hq.element += self.element
            print(str.format("{0:03d}:30", time), end=" ")
            printWarInfo(self.red)
            print(str.format("earned {0} elements for his headquarter", self.element))
            self.element = 0
            return
        if self.red is None and self.blue is not None:
            self.blue.hq.element += self.element
            print(str.format("{0:03d}:30", time), end=" ")
            printWarInfo(self.blue)
            print(str.format("earned {0} elements for his headquarter", self.element))
            self.element = 0

    def raiseFlag(self, time):
        if self.blue.strength > 0 and self.red.strength > 0 or self.blue.strength <= 0 and self.red.strength <= 0:
            self.now = -1
            self.count = 0
            return
        if self.blue.strength <= 0:
            if self.now != 0:
                self.now = 0
                self.count = 1
            if self.flag != 0:
                if self.count >= 2:
                    self.flag = 0
                    print(str.format("{0:03d}:40", time), "red flag raised in city", self.id)
                self.count += 1
        if self.red.strength <= 0:
            if self.now != 1:
                self.now = 1
                self.count = 1
            if self.flag != 1:
                if self.count >= 2:
                    self.flag = 1
                    print(str.format("{0:03d}:40", time), "blue flag raised in city", self.id)
                self.count += 1


cities = [None] * 30


class Weapon:
    def __init__(self, t):
        self.type = t
        self.typename = weapon_name[t]


class Sword(Weapon):
    def __init__(self, t, force):
        Weapon.__init__(self, t)
        self.force = floor(force * 2 / 10)


class Bomb(Weapon):
    def __init__(self, t):
        Weapon.__init__(self, t)


class Arrow(Weapon):
    def __init__(self, t):
        Weapon.__init__(self, t)
        self.use = 3


def makeWeapon(t, force):
    if t == 0:
        tmp = Sword(0, force)
        if tmp.force <= 0: tmp = None
        return tmp
    elif t == 1:
        return Bomb(1)
    elif t == 2:
        return Arrow(2)
    return None


class Warrior:
    def __init__(self, t, s, hq, force):
        self.type = t
        self.strength = s
        global warrior_name, cities
        self.name = warrior_name[t]
        self.id = hq.warNum + 1
        self.force = force
        self.hq = hq
        self.city = hq.location
        self.kill = False
        if hq.type == 0:
            cities[0].red = self
        else:
            cities[hq.location].blue = self
        self.wp = [None, None, None]

    def march(self, time, n):
        global cities
        if self.strength <= 0: return
        if self.hq.type == 0:
            if self.city == n + 1: return
            cities[self.city].red = None
            self.city += 1
            cities[self.city].red2 = self
            if self.type == 2:
                self.step += 1
                if self.step != 0 and self.step % 2 == 0:
                    if self.strength <= 9:
                        self.strength = 1
                        self.force += 20
                    else:
                        self.strength -= 9
                        self.force += 20
        elif self.hq.type == 1:
            if self.city == 0: return
            cities[self.city].blue = None
            self.city -= 1
            cities[self.city].blue2 = self
            if self.type == 2:
                self.step += 1
                if self.step != 0 and self.step % 2 == 0:
                    if self.strength <= 9:
                        self.strength = 1
                        self.force += 20
                    else:
                        self.strength -= 9
                        self.force += 20
        print(str.format("{0:03d}:10", time), end=" ")
        printWarInfo(self)
        if self.city != n + 1 and self.city != 0:
            print("marched to city", self.city, end=" ")
        else:
            print("reached", headquarter_name[not self.hq.type], "headquarter", end=" ")
        print(str.format("with {0} elements and force {1}", self.strength, self.force))

    def warUseArrow(self):
        self.wp[2].use -= 1
        if self.wp[2].use <= 0: self.wp[2] = None

    def shot(self, time, r):
        global cities
        if self.hq.type == 0:
            cities[self.city + 1].blue.strength -= r
            print(str.format("{0:03d}:35", time), end=" ")
            printWarInfo(self)
            print("shot", end=" ")
            if cities[self.city + 1].blue.strength <= 0:
                print("and killed", end=" ")
                printWarInfo(cities[self.city + 1].blue)
            print()
            self.warUseArrow()
        elif self.hq.type == 1:
            cities[self.city - 1].red.strength -= r
            print(str.format("{0:03d}:35", time), end=" ")
            printWarInfo(self)
            print("shot", end=" ")
            if cities[self.city - 1].red.strength <= 0:
                print("and killed", end=" ")
                printWarInfo(cities[self.city - 1].red)
            print()
            self.warUseArrow()

    def willUseBomb(self, enemy):
        if self.strength <= 0 or enemy.strength <= 0: return False
        if priorToAttack(self.city, enemy.hq.type):
            return self.strength <= (enemy.force + enemy.forceOfSword())
        else:
            return (enemy.strength > (self.force + self.forceOfSword())
                    and enemy.type != 1 and self.strength <= (enemy.force / 2 + enemy.forceOfSword()))

    def useBomb(self, enemy, time):
        global cities
        print(str.format("{0:03d}:38", time), end=" ")
        printWarInfo(self)
        print("used a bomb and killed", end=" ")
        printWarInfo(enemy)
        print()
        cities[self.city].red.strength = cities[self.city].blue.strength = 0
        cities[self.city].red = cities[self.city].blue = None

    def forceOfSword(self):
        tmp = 0
        if self.wp[0] is not None:
            tmp = floor(self.wp[0].force)
        return tmp

    def earnElement(self, time):
        global cities
        print(str.format("{0:03d}:40", time), end=" ")
        printWarInfo(self)
        print("earned", cities[self.city].element, "elements for his headquarter")
        self.hq.element += cities[self.city].element
        cities[self.city].element = 0

    def warUseSword(self):
        if self.wp[0] is not None:
            self.wp[0].force = floor(self.wp[0].force * 0.8)
            if self.wp[0].force <= 0: self.wp[0] = None

    def warWin(self, enemy, time):
        if self.type == 4: self.getWeapon(enemy)
        self.earnElement(time)

    def attack(self, enemy, time):
        print(str.format("{0:03d}:40", time), end=" ")
        printWarInfo(self)
        print("attacked", end=" ")
        printWarInfo(enemy)
        print("in city", self.city, "with", self.strength, "elements and force", self.force)
        aggforce = self.force + self.forceOfSword()
        if enemy.type == 3 and enemy.strength <= aggforce:
            self.strength += enemy.strength
        enemy.strength -= aggforce
        self.warUseSword()
        if enemy.strength <= 0:
            print(str.format("{0:03d}:40", time), end=" ")
            printWarInfo(enemy)
            print("was killed in city", self.city)
            self.kill = True

    def fightBack(self, enemy, time):
        if self.strength <= 0 or self.type == 1: return
        if enemy.strength <= 0: return
        print(str.format("{0:03d}:40", time), end=" ")
        printWarInfo(self)
        print("fought back against", end=" ")
        printWarInfo(enemy)
        print("in city", self.city)
        aggforce = self.force // 2 + self.forceOfSword()
        if enemy.type == 3 and enemy.strength <= aggforce:
            self.strength += enemy.strength
        enemy.strength -= aggforce
        self.warUseSword()
        if enemy.strength <= 0:
            print(str.format("{0:03d}:40", time), end=" ")
            printWarInfo(enemy)
            print("was killed in city", self.city)
            self.kill = True

    def reportWp(self, time):
        print(str.format("{0:03d}:55", time), end=" ")
        printWarInfo(self)
        print("has", end=" ")
        sum = int(self.wp[0] is not None) + int(self.wp[1] is not None) + int(self.wp[2] is not None)
        if sum == 3:
            printWp(self.wp[2])
            print(",", end="")
            printWp(self.wp[1])
            print(",", end="")
            printWp(self.wp[0])
        elif sum == 2:
            if printWp(self.wp[2]):
                print(",", end="")
                printWp(self.wp[1])
                printWp(self.wp[0])
            else:
                printWp(self.wp[1])
                print(",", end="")
                printWp(self.wp[0])
        elif sum == 1:
            printWp(self.wp[2])
            printWp(self.wp[1])
            printWp(self.wp[0])
        else:
            print("no weapon", end="")
        print()


class Dragon(Warrior):
    def __init__(self, t, s, hq, force):
        Warrior.__init__(self, t, s, hq, force)
        self.morale = (hq.element - s) / s
        self.wp[(self.hq.warNum + 1) % 3] = makeWeapon((self.hq.warNum + 1) % 3, force)

    def printInfo(self):
        print("Its morale is", format(self.morale, ".2f"))

    def yell(self, time):
        if self.kill:
            self.morale += 0.2
        else:
            self.morale -= 0.2
        if self.morale > 0.8:
            print(str.format("{0:03d}:40", time), end=" ")
            printWarInfo(self)
            print("yelled in city", self.city)


class Ninja(Warrior):
    def __init__(self, t, s, hq, force):
        Warrior.__init__(self, t, s, hq, force)
        self.wp[(self.hq.warNum + 1) % 3] = makeWeapon((self.hq.warNum + 1) % 3, force)
        self.wp[(self.hq.warNum + 2) % 3] = makeWeapon((self.hq.warNum + 2) % 3, force)


class Iceman(Warrior):
    def __init__(self, t, s, hq, force):
        Warrior.__init__(self, t, s, hq, force)
        self.wp[(self.hq.warNum + 1) % 3] = makeWeapon((self.hq.warNum + 1) % 3, force)
        self.step = 0


class Lion(Warrior):
    def __init__(self, t, s, hq, force):
        Warrior.__init__(self, t, s, hq, force)
        self.loyalty = hq.element - s

    def printInfo(self):
        print("Its loyalty is", self.loyalty)

    def runAway(self, time):
        print(str.format("{0:03d}:05", time), self.hq.typename, self.name, self.id, "ran away")
        if self.hq.type == 0:
            cities[self.city].red = None
        elif self.hq.type == 1:
            cities[self.city].blue = None


class Wolf(Warrior):
    def __init__(self, t, s, hq, force):
        Warrior.__init__(self, t, s, hq, force)

    def getWeapon(self, enemy):
        if self.wp[0] is None and enemy.wp[0] is not None: self.wp[0] = enemy.wp[0]
        if self.wp[1] is None and enemy.wp[1] is not None: self.wp[1] = enemy.wp[1]
        if self.wp[2] is None and enemy.wp[2] is not None: self.wp[2] = enemy.wp[2]


class Headquarter:
    def __init__(self, m, order):
        self.type = 0
        self.element = m
        self.order = order
        self.now = 0
        self.warNum = 0
        self.warriors = [None] * 1000
        self.typename = ""
        self.taken = False
        self.location = -1

    def printMakeWar(self, time, tmp):
        print(str.format("{0:03d}:00", time), self.typename, warrior_name[tmp], self.warNum + 1, "born")
        self.warNum += 1

    def makeWarrior(self, time, elements, force):
        tmp = self.order[self.now]
        if elements[tmp] <= self.element:
            if tmp == 0:
                self.warriors[self.warNum] = Dragon(tmp, elements[tmp], self, force[tmp])
                self.printMakeWar(time, tmp)
                self.warriors[self.warNum - 1].printInfo()
            elif tmp == 1:
                self.warriors[self.warNum] = Ninja(tmp, elements[tmp], self, force[tmp])
                self.printMakeWar(time, tmp)
            elif tmp == 2:
                self.warriors[self.warNum] = Iceman(tmp, elements[tmp], self, force[tmp])
                self.printMakeWar(time, tmp)
            elif tmp == 3:
                self.warriors[self.warNum] = Lion(tmp, elements[tmp], self, force[tmp])
                self.printMakeWar(time, tmp)
                self.warriors[self.warNum - 1].printInfo()
            elif tmp == 4:
                self.warriors[self.warNum] = Wolf(tmp, elements[tmp], self, force[tmp])
                self.printMakeWar(time, tmp)
            self.element -= elements[tmp]
            self.now = (self.now + 1) % 5

    def takeHq(self, dst, time):
        count = 0
        for i in range(0, self.warNum):
            if self.warriors[i].city == dst.location: count += 1
        if count >= 2:
            dst.taken = True
            print(str.format("{0:03d}:10", time), dst.typename, "headquarter was taken")

    def reportElement(self, time):
        print(str.format("{0:03d}:50", time), self.element, "elements in", self.typename, "headquarter")


def printWarInfo(war):
    print(war.hq.typename, war.name, war.id, end=" ")


def priorToAttack(i, type):
    if type == 0:
        return cities[i].flag == 0 or (cities[i].flag == -1 and i % 2 == 1)
    elif type == 1:
        return cities[i].flag == 1 or (cities[i].flag == -1 and i % 2 == 0)
    return False


def printWp(wp):
    if wp is None: return False
    print(wp.typename, end="")
    if wp.type == 0:
        print(str.format("({0})", wp.force), end="")
    elif wp.type == 2:
        print(str.format("({0})", wp.use), end="")
    return True


# 开始
t = int(input())
order_red = [2, 3, 4, 1, 0];
order_blue = [3, 0, 1, 2, 4]
for case in range(1, t + 1):
    print(str.format("Case {0}:", case))
    time = 0
    tmp = input().split(" ")
    m = int(tmp[0]); n = int(tmp[1]); r = int(tmp[2]); k = int(tmp[3]); t = int(tmp[4])
    elements = list(input().split(" "))
    for i in range(0, elements.__len__()):
        elements[i] = int(elements[i])
    force = list(input().split(" "))
    for i in range(0, force.__len__()):
        force[i] = int(force[i])
    for i in range(0, 30):
        cities[i] = City(i)
    red = Headquarter(m, order_red); blue = Headquarter(m, order_blue)
    red.type = 0; blue.type = 1
    red.typename = "red"; blue.typename = "blue"
    red.location = 0; blue.location = n + 1
    while 1:
        # time:00 武士降生
        if time * 60 > t: break
        red.makeWarrior(time, elements, force)
        blue.makeWarrior(time, elements, force)

        # time:05 Lion逃跑
        if time * 60 + 5 > t: break
        for i in range(0, n + 2):
            if i != n + 1 and cities[i].red is not None and cities[i].red.type == 3:
                if cities[i].red.loyalty <= 0:
                    cities[i].red.runAway(time)
            if i != 0 and cities[i].blue is not None and cities[i].blue.type == 3:
                if cities[i].blue.loyalty <= 0:
                    cities[i].blue.runAway(time)

        # time:10 武士前进、武士抵达敌军司令部、司令部被占领
        if time * 60 + 10 > t: break
        for i in range(0, n + 2):
            if i >= 1 and cities[i - 1].red is not None: cities[i - 1].red.march(time, n)
            if i == n + 1 and not blue.taken: red.takeHq(blue, time)
            if i <= n and cities[i + 1].blue is not None: cities[i + 1].blue.march(time, n)
            if i == 0 and not red.taken: blue.takeHq(red, time)
        cities[0].red = cities[blue.location].blue = None
        if cities[0].blue2 is not None:
            cities[0].blue = cities[0].blue2
            cities[0].blue2 = None
        if cities[blue.location].red2 is not None:
            cities[blue.location].red = cities[blue.location].red2
            cities[blue.location].red2 = None
        for i in range(1, n + 1):
            cities[i].red = cities[i].red2
            cities[i].blue = cities[i].blue2
            cities[i].red2 = cities[i].blue2 = None
        if red.taken or blue.taken: break

        # time:20 城市生产生命值
        if time * 60 + 20 > t: break
        for i in range(1, n + 1): cities[i].element += 10

        # time:30 武士从城市获取生命值
        if time * 60 + 30 > t: break
        for i in range(1, n + 1): cities[i].warGetElement(time)

        # time:35 武士放箭
        if time * 60 + 35 > t: break
        for i in range(0, n + 2):
            if i != n + 1 and cities[i].red is not None and cities[i].red.wp[2] is not None and cities[
                        i + 1].blue is not None:
                cities[i].red.shot(time, r)
            if i != 0 and cities[i].blue is not None and cities[i].blue.wp[2] is not None and cities[
                        i - 1].red is not None:
                cities[i].blue.shot(time, r)

        # time:38 武士使用bomb
        if time * 60 + 38 > t: break
        for i in range(0, n + 2):
            if cities[i].red is not None and cities[i].blue is not None:
                if cities[i].red.wp[1] is not None and cities[i].red.willUseBomb(cities[i].blue):
                    cities[i].red.useBomb(cities[i].blue, time)
                elif cities[i].blue.wp[1] is not None and cities[i].blue.willUseBomb(cities[i].red):
                    cities[i].blue.useBomb(cities[i].red, time)

        # time:40 武士主动进攻、武士反击、武士战死、武士欢呼、武士获取生命元
        if time * 60 + 40 > t: break
        for i in range(0, n + 2):
            if cities[i].red is not None and cities[i].blue is not None:
                if cities[i].red.strength <= 0 and cities[i].blue.strength <= 0: continue
                if cities[i].red.strength > 0 and cities[i].blue.strength <= 0:
                    cities[i].red.kill = True
                    if cities[i].red.type == 4:
                        cities[i].red.getWeapon(cities[i].blue)
                    if cities[i].red.type == 0 and cities[i].red.strength > 0 and priorToAttack(i, 0):
                        cities[i].red.yell(time)
                    cities[i].red.earnElement(time)
                elif cities[i].blue.strength > 0 and cities[i].red.strength <= 0:
                    cities[i].blue.kill = True
                    if cities[i].blue.type == 4:
                        cities[i].blue.getWeapon(cities[i].red)
                    if cities[i].blue.type == 0 and cities[i].blue.strength > 0 and priorToAttack(i, 1):
                        cities[i].blue.yell(time)
                    cities[i].blue.earnElement(time)
                elif priorToAttack(i, 0):
                    cities[i].red.attack(cities[i].blue, time)
                    cities[i].blue.fightBack(cities[i].red, time)
                    if cities[i].red.type == 0 and cities[i].red.strength > 0:
                        cities[i].red.yell(time)
                    if cities[i].red.strength > 0 and cities[i].blue.strength <= 0:
                        cities[i].red.warWin(cities[i].blue, time)
                    if cities[i].red.strength <= 0 and cities[i].blue.strength > 0:
                        cities[i].blue.warWin(cities[i].red, time)
                else:
                    cities[i].blue.attack(cities[i].red, time)
                    cities[i].red.fightBack(cities[i].blue, time)
                    if cities[i].blue.type == 0 and cities[i].blue.strength > 0:
                        cities[i].blue.yell(time)
                    if cities[i].blue.strength > 0 and cities[i].red.strength <= 0:
                        cities[i].blue.warWin(cities[i].red, time)
                    if cities[i].blue.strength <= 0 and cities[i].red.strength > 0:
                        cities[i].red.warWin(cities[i].blue, time)
                cities[i].raiseFlag(time)
                if not cities[i].red.kill and not cities[i].blue.kill:
                    if cities[i].red.type == 3:
                        cities[i].red.loyalty -= k
                    if cities[i].blue.type == 3:
                        cities[i].blue.loyalty -= k
        # 为死掉的武士收尸
        for i in range(0, n + 2):
            if cities[i].red is not None and cities[i].red.strength <= 0:
                cities[i].red = None
            if cities[i].blue is not None and cities[i].blue.strength <= 0:
                cities[i].blue = None
        # time:40 司令部奖励武士生命值
        for i in range(n + 1, -1, -1):
            if cities[i].red is not None and cities[i].red.kill:
                if red.element >= 8:
                    cities[i].red.strength += 8
                    red.element -= 8
                cities[i].red.kill = False
        for i in range(0, n + 2):
            if cities[i].blue is not None and cities[i].blue.kill:
                if blue.element >= 8:
                    cities[i].blue.strength += 8
                    blue.element -= 8
                cities[i].blue.kill = False

        # time:50 司令部报告生命元数量
        if time * 60 + 50 > t: break
        red.reportElement(time)
        blue.reportElement(time)

        # time:55 武士报告武器情况
        if time * 60 + 55 > t: break
        for i in range(0, n + 2):
            if cities[i].red is not None: cities[i].red.reportWp(time)
        for i in range(0, n + 2):
            if cities[i].blue is not None: cities[i].blue.reportWp(time)

        time += 1
