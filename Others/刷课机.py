from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
from pyquery import PyQuery as pq


stu_id = ""
password = ""
time_break = 10
target_course = []
course_names = []
course_stu_no = []
count_target_course = 0
count_use_times = 0
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)


def get_info():
    global stu_id, password, target_course, count_target_course, count_use_times
    # 获取学号和密码
    stu_id = input("请输入你的学号")
    password = input("请输入你的密码")

    # elective页面
    browser.get('http://elective.pku.edu.cn')

    # 等待iaaa页面加载
    wait.until(EC.presence_of_element_located((By.ID, 'user_name')))
    # iaaa页面填写信息
    input_id = browser.find_element_by_id('user_name')
    input_id.send_keys(stu_id)
    input_pw = browser.find_element_by_id('password')
    input_pw.send_keys(password)
    input_pw.send_keys(Keys.ENTER)

    # 等待选课系统欢迎页加载
    div1 = wait.until(EC.presence_of_element_located((By.ID, 'div1')))

    # 进入主修页面
    div1.click()
    # 等待主修页面加载
    supply_cancel = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                               'body > table:nth-child(2) > tbody > tr > td > '
                                                               'table > tbody > tr:nth-child(2) > td:nth-child(8) '
                                                               '> span > a')))
    supply_cancel.click()

    # 等待补退选页面加载
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > table:nth-child(3) > tbody > '
                                                                'tr:nth-child(6) > td > table > tbody')))
    # 捕获选课计划中可选列表
    doc = pq(browser.page_source)
    course_list = doc('body > table:nth-child(3) > tbody > tr:nth-child(6) > td > table > tbody > tr')
    course_list = course_list[1:-2]
    for each in course_list:
        info = pq(each).children('td')
        info = list(info)
        name = pq(info[0]).find('a > span').text()
        course_names.append(name)
        stu_no = pq(info[9]).find('span')
        course_stu_no.append(stu_no.text().split(' / '))

    # 打印可选列表
    maxlen = 0
    for each in course_names:
        t = len(each)
        if t > maxlen:
            maxlen = t
    print("目前你的备选课程有：")
    print('-------' + '-' * maxlen * 2 + '--', sep='')
    for i in range(len(course_names)):
        print('| ' + str(i).ljust(2, ' ') + ' | ' + course_names[i]
                + ' ' * (maxlen - len(str(course_names[i]))) * 2 + " |", sep='')
    print('-------' + '-' * maxlen * 2 + '--', sep='')

    # 获取目标课程
    target_course = input("请列出你希望刷的课程编号，以空格分隔（如0 2 3），按回车结束：").split(' ')
    count_target_course = len(target_course)
    for i in range(count_target_course):
        target_course[i] = int(target_course[i])

    # 填写验证码
    input("请在chrome中填写验证码，按回车继续")


def main():
    global target_course, count_target_course, count_use_times, course_names, course_stu_no
    # 循环尝试刷课
    while True:
        # 进行一次尝试
        print("刷新于" + time.strftime("%Y-%m-%d %H:%M:%S") + "，正在尝试：" + course_names[target_course[count_use_times]])
        refresh = browser.find_element_by_css_selector('body > table:nth-child(3) > tbody > tr:nth-child(6) > '
                                                       'td > table > tbody > tr:nth-child('
                                                       + str(target_course[count_use_times] + 2)
                                                       + ') > td:nth-child(11) > a > span')
        refresh.click()

        # 处理弹窗
        alert = wait.until(EC.alert_is_present())
        text = alert.text
        alert.accept()
        if "您确定要选" in text:
            print("选课" + course_names[target_course[count_use_times]] + "成功！")
            break

        # 重新获得选课计划中可选列表
        doc = pq(browser.page_source)
        course_list = doc('body > table:nth-child(3) > tbody > tr:nth-child(6) > td > table > tbody > tr')
        course_list = course_list[1:-2]
        course_names = []
        course_stu_no = []
        for each in course_list:
            info = pq(each).children('td')
            info = list(info)

            name = pq(info[0]).find('a > span').text()
            course_names.append(name)
            stu_no = pq(info[9]).find('span')
            course_stu_no.append(stu_no.text().split(' / '))

        # 打印可选列表
        maxlen = 0
        for each in course_names:
            t = len(each)
            if t > maxlen:
                maxlen = t
        print('--' + '-' * maxlen * 2 + '---' + '-' * 7 + '--', sep='')
        for i in range(len(course_names)):
            print('| ' + course_names[i] + ' ' * (maxlen - len(str(course_names[i]))) * 2 + " | "
                  + str(course_stu_no[i][0]).ljust(3, ' ') + '/' + str(course_stu_no[i][1]).ljust(3, ' ') + ' |', sep='')
        print('--' + '-' * maxlen * 2 + '---' + '-' * 7 + '--', sep='')

        # 刷新结束
        count_use_times = (count_use_times + 1) % count_target_course
        time.sleep(time_break)

    browser.close()


if __name__ == '__main__':
    get_info()
    main()
