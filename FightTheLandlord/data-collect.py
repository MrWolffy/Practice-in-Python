import json
import csv
import time


# 原始json的结构：
# _id, 应该是对局id
# initdata
#   publiccard, 地主被公开的三张牌
#   allocation, 分牌情况
#   seed
# scores, 最终得分情况
# players, 玩家情况
# log
# 偶数：
#   keep_running
#   memory
#   output
#   time
#   verdict
# 奇数：
#   '0'或'1'或'2', 玩家身份
#       keep_running
#       memory
#       time
#       verdict
#       response, 出牌情况


# 需要的数据：
#   我是谁
#   我赢了吗
#   三家现在手里有多少牌（与我是谁的交叉项）
#   我手里有什么牌
#   我出了什么牌
#   我管了什么牌


# 具体一些：
#   我是谁：三个参数，分别代表地主、农民甲和农民乙，从玩家身份可以知道
#   我赢了吗：一个参数，从scores和我是谁可以知道，排除崩溃的局面
#   三家现在手里有多少牌（与我是谁的交叉项）：18个参数，分别为我是谁和三家现在手里有多少牌相乘，以及它们的平方项
#   我手里有什么牌：54个参数，52个参数代表从3到2共13种牌每种牌的个数（从1到4共4种可能），2个参数代表有没有两种王
#   我出了什么牌：许多个参数，分别代表每一种牌型
#   我管了什么牌：许多个参数，分别代表每一种牌型


def card2level(card):
    return card // 4 + card // 53


def cardAnalysis(cards):
    levels = [0] * 15
    para4 = [0] * 54
    for each in cards:
        levels[card2level(each)] += 1
    for i in range(0, 14):
        if levels[i] != 0:
            para4[i * 4 + levels[i]] = 1
    if levels[13] == 1:
        para4[52] = 1
    if levels[14] == 1:
        para4[53] = 1
    return para4


def findMaxSeq(packs):
    for c in range(1, len(packs)):
        if packs[c].count != packs[0].count or packs[c].level != packs[c - 1].level - 1:
            return c
    return len(packs)


class cardPack:
    def __init__(self, level, count):
        self.level = level
        self.count = count

    def __lt__(self, other):
        if self.count == other.count:
            return self.level > other.level
        return self.count > other.count


class cardCombo:
    def __init__(self, cards):
        self.combotype = ""
        self.combolevel = 0
        self.cards = cards
        self.packs = []
        if len(cards) == 0:
            self.combotype = "pass"
            return
        counts = [0] * 15
        countOfCount = [0] * 5
        for each in cards:
            counts[card2level(each)] += 1
        for l in range(0, 15):
            if counts[l] != 0:
                self.packs.append(cardPack(l, counts[l]))
                countOfCount[counts[l]] += 1
        self.packs.sort()
        self.combolevel = self.packs[0].level
        kindOfCountOfCount = []
        for i in range(0, 5):
            if countOfCount[i] != 0:
                kindOfCountOfCount.append(i)
        kindOfCountOfCount.sort()

        if len(kindOfCountOfCount) == 1:  # 只有一类牌
            curr = countOfCount[kindOfCountOfCount[0]]
            if kindOfCountOfCount[0] == 1:  # 只有若干单张
                if curr == 1:
                    self.combotype = "single"
                elif curr == 2 and self.packs[1].level == 13:
                    self.combotype = "rocket"
                elif 5 <= curr == findMaxSeq(self.packs) and self.packs[0].level <= 11:
                    self.combotype = "straight"
            elif kindOfCountOfCount[0] == 2:  # 只有若干对子
                if curr == 1:
                    self.combotype = "pair"
                if 3 <= curr == findMaxSeq(self.packs) and self.packs[0].level <= 11:
                    self.combotype = "straight2"
            elif kindOfCountOfCount[0] == 3:  # 只有若干三条
                if curr == 1:
                    self.combotype = "triplet"
                elif curr == findMaxSeq(self.packs) and self.packs[0].level <= 11:
                    self.combotype = "plane"
            elif kindOfCountOfCount[0] == 4:  # 只有若干四条
                if curr == 1:
                    self.combotype = "bomb"
                elif curr == findMaxSeq(self.packs) and self.packs[0].level <= 11:
                    self.combotype = "sshuttle"
        elif len(kindOfCountOfCount) == 2:  # 有两类牌
            curr = countOfCount[kindOfCountOfCount[1]]
            lesser = countOfCount[kindOfCountOfCount[0]]
            if kindOfCountOfCount[1] == 3:  # 三条带？
                if curr == 1 and lesser == 1:
                    self.combotype = "triplet1"
                elif findMaxSeq(self.packs) == curr == lesser and self.packs[0].level <= 11:
                    self.combotype = "plane1"
            if kindOfCountOfCount[1] == 4:  # 四条带？
                if kindOfCountOfCount[0] == 1:
                    if curr == 1 and lesser == 2:
                        self.combotype = "quardruple2"
                    if findMaxSeq(self.packs) == curr and lesser == curr * 2 and self.packs[0].level <= 11:
                        self.combotype = "sshuttle2"
                if kindOfCountOfCount[0] == 2:
                    if curr == 1 and lesser == 2:
                        self.combotype = "quardruple4"
                    if findMaxSeq(self.packs) == curr and lesser == curr * 2 and self.packs[0].level <= 11:
                        self.combotype = "sshuttle4"
        if self.combotype == "":
            raise ValueError


def myAction(cards):
    para5 = [0] * 32
    myaction = cardCombo(cards)

    # 过
    if myaction.combotype == "pass":
        para5[0] = 1

    # 单张
    # 使用level的一次、两次和三次项
    if myaction.combotype == "single":
        para5[1] = myaction.combolevel
        para5[2] = myaction.combolevel ** 2
        para5[3] = myaction.combolevel ** 3

    # 对子
    # 使用level的一次、两次和三次项
    if myaction.combotype == "pair":
        para5[4] = myaction.combolevel
        para5[5] = myaction.combolevel ** 2
        para5[6] = myaction.combolevel ** 3

    # 顺子
    # 使用顺子起点的level、长度以及交叉项
    if myaction.combotype == "straight":
        para5[7] = myaction.combolevel
        para5[8] = findMaxSeq(myaction.packs)
        para5[9] = myaction.combolevel * findMaxSeq(myaction.packs)

    # 双顺
    # 双顺和单顺作同样处理
    if myaction.combotype == "straight2":
        para5[10] = myaction.combolevel
        para5[11] = findMaxSeq(myaction.packs)
        para5[12] = myaction.combolevel * findMaxSeq(myaction.packs)

    # 三条
    # 因为纯三条比较少见，所以采用一次项和二次项
    if myaction.combotype == "triplet":
        para5[13] = myaction.combolevel
        para5[14] = myaction.combolevel

    # 三带一
    # 采用三条和单张的一次项以及它们的交叉项
    if myaction.combotype == "triplet1":
        para5[15] = myaction.packs[0].level
        para5[16] = myaction.packs[1].level
        para5[17] = myaction.packs[0].level * myaction.packs[1].level

    # 三带二
    # 与三带一类似
    if myaction.combotype == "triplet2":
        para5[18] = myaction.packs[0].level
        para5[19] = myaction.packs[1].level
        para5[20] = myaction.packs[0].level * myaction.packs[1].level

    # 炸弹
    # 采用炸弹的一次项和二次项
    if myaction.combotype == "bomb":
        para5[21] = myaction.combolevel
        para5[22] = myaction.combolevel ** 2

    # 四带二（只）
    # 以下都比较稀少，只采用一个有或没有
    if myaction.combotype == "quadruple2":
        para5[23] = 1

    # 四带二（对）
    if myaction.combotype == "quadruple4":
        para5[24] = 1

    # 飞机
    if myaction.combotype == "plane":
        para5[25] = 1

    # 飞机带小翼
    if myaction.combotype == "plane1":
        para5[26] = 1

    # 飞机带大翼
    if myaction.combotype == "plane2":
        para5[27] = 1

    # 航天飞机
    if myaction.combotype == "sshuttle":
        para5[28] = 1

    # 航天飞机带小翼
    if myaction.combotype == "sshuttle2":
        para5[29] = 1

    # 航天飞机带大翼
    if myaction.combotype == "sshuttle4":
        para5[30] = 1

    # 火箭
    if myaction.combotype == "rocket":
        para5[31] = 1

    return para5


def main(month, match):
    path = "FightTheLandlord-2018-" + str(month) + "/" \
           + str(match * 100 + 1) + "-" + str((match + 1) * 100) + ".matches"
    result = open("data.txt", "ab")
    with open(path) as f:
        for line in f:
            s = json.loads(line)
            length = len(s["log"])

            if s["scores"] == [3, -1, -1] or s["scores"] == [-1, 3, 3] \
                    or s["scores"] == [2.5, -1, -1] or s["scores"] == [-1, 2.5, 2.5]:
                continue

            player = 0
            cards = json.loads(s["initdata"])["allocation"]
            for i in range(1, length, 2):
                para1, para2, para3 = [0] * 3, [0], [0] * 18

                para1[player] = 1

                if s["scores"][player] > 2:
                    para2[0] = 1

                try:
                    for each in s["log"][i][str(player)]["response"]:
                        cards[player].remove(each)
                except KeyError:
                    player = (player + 1) % 3
                    continue

                for j in range(0, 3):
                    for k in range(0, 3):
                        para3[j * 3 + k] = len(cards[j]) * para1[k]
                for j in range(0, 9):
                    para3[9 + j] = para3[j] ** 2

                para4 = cardAnalysis(cards[player])

                try:
                    para5 = myAction(s["log"][i][str(player)]["response"])
                except ValueError:
                    player = (player + 1) % 3
                    continue

                try:
                    para6 = myAction(s["log"][i - 1]["output"]["content"][str(player)]["history"][0])
                except ValueError:
                    player = (player + 1) % 3
                    continue

                for each in para2 + para1 + para3 + para4 + para5 + para6:
                    result.write(bytes(str(each) + ",", encoding="utf8"))
                result.write(bytes("\46\n", encoding="utf8"))
                player = (player + 1) % 3


if __name__ == '__main__':
    t0 = time.monotonic()
    for i in range(0, 961):
        t1 = time.monotonic()
        print("正在读取 6 月的第", i, "个文件，用时", t1 - t0, "秒")
        main(6, i)
    for i in range(0, 640):
        t1 = time.monotonic()
        print("正在读取 7 月的第", i, "个文件，用时", t1 - t0, "秒")
        main(7, i)
