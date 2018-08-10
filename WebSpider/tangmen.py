from bs4 import BeautifulSoup
import requests
import time

url = "http://www.shushu8.com/jueshitangmen/"
time0 = time.monotonic()


def parse(i):
    time1 = time.monotonic()
    print("正在爬取第", i, "页，已用时", time1 - time0, "秒")
    request = requests.get(url + str(i))
    html = request.content
    soup = BeautifulSoup(html)
    with open("tangmen.txt", "a") as f:
        f.write(soup.find("div", {"class": "page-content"}).text)


if __name__ == '__main__':
    for i in range(1, 1789):
        parse(i)