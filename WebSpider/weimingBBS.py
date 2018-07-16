from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


browser = webdriver.Chrome()
browser.get("http://bbs.pku.edu.cn")
username = browser.find_element_by_name("username")
username.send_keys("MrWolffy")
password = browser.find_element_by_name("password")
password.send_keys("BarrettM82A1")
login = browser.find_element_by_class_name("red")
login.click()
wait = WebDriverWait(browser, 10)
big_ten = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "big-ten")))
for each in big_ten.find_elements(By.TAG_NAME, "li"):
    print("rank:", each.find_element_by_class_name("rank-digit").text, end=" ")
    print("title:", each.find_element_by_class_name("post-link").text)
