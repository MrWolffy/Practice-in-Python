import random


def getSymbol(r):
    if r < 0:
        return "-"
    else:
        return "+"


# 真随机
def realRandom():
    fakeRandom(0)


# 伪随机
def fakeRandom(rho):
    u = 0
    tmpSymbol = "/"
    countChange = 0
    countSymbol = [0, 0]
    for i in range(100):
        r = random.normalvariate(0, 1) + rho * u
        u = r
        if r < 0:
            countSymbol[0] += 1
        else:
            countSymbol[1] += 1
        c = getSymbol(r)
        if c != tmpSymbol:
            countChange += 1
            tmpSymbol = c
        print(c, end="")
    print("\nrun = ", countChange, sep="")
    print("[# of -, # of +] =", countSymbol)


if __name__ == '__main__':
    realRandom()
    fakeRandom(0.6)
    fakeRandom(-0.6)
