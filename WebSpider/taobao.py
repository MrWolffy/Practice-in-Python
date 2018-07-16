from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote
from pyquery import PyQuery as pq
import csv


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
browser = webdriver.Chrome(chrome_options=chrome_options)
wait = WebDriverWait(browser, 10)
KEYWORD = "iPad"
MAX_PAGE = 100
fieldnames = ["image", "price", "deal", "title", "shop", "location"]


def index_page(page):
    print("正在爬取第", page, "页")
    try:
        url = 'https://s.taobao.com/search?q=' + quote(KEYWORD)
        browser.get(url)
        if page > 1:
            input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))
            submit = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit')))
            input.clear()
            input.send_keys(page)
            submit.click()
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), str(page)))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
        get_products()
    except TimeoutException:
        index_page(page)


def get_products():
    html = browser.page_source
    doc = pq(html)
    items = doc("#mainsrp-itemlist .items .item").items()
    for item in items:
        product = {
            "image": item.find(".pic .img").attr("data-src"),
            "price": item.find(".price").text(),
            "deal": item.find(".deal-cnt").text(),
            "title": item.find(".title").text(),
            "shop": item.find(".shop").text(),
            "location": item.find(".location").text()
        }
        print(product)
        write_to_csv(product)


def write_to_csv(result):
    with open("data.csv", "a") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(result)


def main():
    for i in range(1, MAX_PAGE + 1):
        index_page(i)


if __name__ == "__main__":
    with open("data.csv", "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
    main()
