import datetime
import re
import time

import pymysql
import requests
from lxml import etree
from requests.exceptions import RequestException

from selenium import webdriver





def call_page(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome("/usr/bin/chromedriver", chrome_options=options)
    driver.get(url)
    html = driver.page_source
    driver.quit()
    return html




# 正则和lxml混用
def parse_html(html):  # 正则专门有反爬虫的布局设置，不适合爬取表格化数据！
    big_list = []
    try:


        selector = etree.HTML(html)
        # 小主题的解析　比如猪肉？ ３个数字
        # Theme = selector.xpath("/html/body/div[5]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/h1/text()")
        # names = selector.xpath("/html/body/div[5]/div/div/div[1]/div[1]/div/div[2]/div[2]/div[2]/ul/li/div/div/p[1]/a/text()")
        # name_l = []
        # for item in names:
        #     s_name = item.strip()
        #     name_l.append(s_name)
        #
        # links = selector.xpath("/html/body/div[5]/div/div/div[1]/div[1]/div/div[2]/div[2]/div[2]/ul/li/div/div/p[1]/a/@href")
        # stars = selector.xpath("/html/body/div[5]/div/div/div[1]/div[1]/div/div[2]/div[2]/div[2]/ul/li/div/div/p[3]/span[1]/text()")
        # perple_num = selector.xpath("/html/body/div[5]/div/div/div[1]/div[1]/div/div[2]/div[2]/div[2]/ul/li/div/div/p[3]/span[2]/text()")


        #  小主题的解析　比如 4个数字

        Theme = selector.xpath("/html/body/div[5]/div/div/div[1]/div[1]/div/div[2]/h1/text()")
        names = selector.xpath(
            "/html/body/div[5]/div/div/div[1]/div[1]/div/div[2]/div[2]/ul/li/div/div/p[1]/a/text()")
        name_l = []
        for item in names:
            s_name = item.strip()
            name_l.append(s_name)

        links = selector.xpath(
            "/html/body/div[5]/div/div/div[1]/div[1]/div/div[2]/div[2]/ul/li/div/div/p[1]/a/@href")
        stars = selector.xpath(
            "/html/body/div[5]/div/div/div[1]/div[1]/div/div[2]/div[2]/ul/li/div/div/p[3]/span[1]/text()")
        perple_num = selector.xpath(
            "/html/body/div[5]/div/div/div[1]/div[1]/div/div[2]/div[2]/ul/li/div/div/p[3]/span[2]/text()")


        f_Theme = Theme * len(names)

        for i1,i2,i3,i4,i5 in zip(f_Theme,name_l,stars,perple_num,links):
            big_list.append((i1,i2,i3,i4,"http://www.xiachufang.com"+i5))
    except:
        pass
    return big_list



def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='CookMenu_S',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    try:
        cursor.executemany('insert into CookMenu_ (Theme,cname,stars,PN,link) values (%s,%s,%s,%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except TypeError:
        pass

#
if __name__ == '__main__':
    #
    # Themes = ["40076","40077","40078","51848","20137","731","104","5391","718","178","206","4359","1105","918","211","787","1138","468","20132","20148","1025","20146","51091","52144","20145","40081","826","394","2316","947","1000426","1025"]
    # for i_theme  in Themes:

    for nu in range(1,51):
        url  = 'http://www.xiachufang.com/category/40077/pop/?page='+str(nu)
        html = call_page(url)
        content = parse_html(html)
        insertDB(content)
        print(datetime.datetime.now())
        time.sleep(0.2)

# http://www.xiachufang.com/category/51848/
# http://www.xiachufang.com/category/40078/
# http://www.xiachufang.com/category/40077/
# select Theme,count(cname) as 主题菜数 from CookMenu_ group by Theme;

# link name

''
#  Theme,cname,stars,PN,link
# create table CookMenu_(
# id int not null primary key auto_increment,
# Theme varchar(20),
# cname text,
# stars varchar(8),
#  PN   varchar(15),
# link varchar(88)
# ) engine=InnoDB  charset=utf8;
#
# drop table CookMenu_;
