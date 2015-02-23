#coding=utf8
import requests
from bs4 import BeautifulSoup
import sqlite3
import datetime

# 设置要抓取的总页数
ALL_PAGE_NUMBER = 21

# 保存到本地Sqlite
def saveToSqlite(lesson_info):
    # 获取lesson_info字典中的信息
    name = lesson_info['name']
    link = lesson_info['link']
    des = lesson_info['des']
    number = lesson_info['number']
    time = lesson_info['time']
    degree = lesson_info['degree']

    # 连接数据库并插入相应数据
    con = sqlite3.connect("lesson.db")
    cur = con.cursor()
    sql = "insert into lesson_info values ('%s', '%s','%s','%s','%s','%s')" % (name, link, des, number, time, degree)
    cur.execute(sql)
    con.commit()

# 抓取主函数
def startGrab():
    # 所有课程页面的BaseURL
    base_url = 'http://www.jikexueyuan.com/course/?pageNum='
    # 当前页码
    page_number = 1

    while page_number <= ALL_PAGE_NUMBER:
        url = base_url + str(page_number)
        print ">>>>>>>>>>>将要抓取", url

        # 可能因为超时等网络问题造成异常，需要捕获并重新抓取
        try:
            page = requests.get(url)
        except:
            print "重新抓取 ", url
            continue

        # 使用BeautifulSoup规范化网页并生成对象
        soup = BeautifulSoup(page.content)

        lesson_data = soup.find_all("li")
        for item in lesson_data:
            try:
                if (item.contents[1].find("a").text):
                    name = item.contents[1].find("a").text
                    link = item.contents[1].find("a").get("href")
                    des = item.contents[1].find("p").text
                    number = item.contents[1].find("em", {"class": "learn-number"}).text
                    time = item.contents[1].find("dd", {"class": "mar-b8"}).contents[1].text
                    degree = item.contents[1].find("dd", {"class": "zhongji"}).contents[1].text
                    lesson_info = {"name": name, "link": link, "des": des, "number": number, "time": time, "degree": degree}
                    saveToSqlite(lesson_info)
                    # print "课程名称: ", item.contents[1].find("a").text
                    # print "课程链接: ", item.contents[1].find("a").get("href")
                    # print "课程简介: ", item.contents[1].find("p").text
                    # print "学习人数: ", item.contents[1].find("em", {"class": "learn-number"}).text
                    # print "课程时间: ", item.contents[1].find("dd", {"class": "mar-b8"}).contents[1].text
                    # print "课程难度: ", item.contents[1].find("dd", {"class": "zhongji"}).contents[1].text
                    # print "-----------------------------------------------"
            except:
                pass
        page_number = page_number + 1


if __name__ == '__main__':
    starttime = datetime.datetime.now()
    startGrab()
    endtime = datetime.datetime.now()
    print "执行时间: ", (endtime - starttime).seconds, "s"