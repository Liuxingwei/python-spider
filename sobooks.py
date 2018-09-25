#!/usr/bin/env python
from selenium import webdriver
import re



# 创建chrome参数对象
opt = webdriver.ChromeOptions()

# 把chrome设置成无界面模式，不论windows还是linux都可以，自动适配对应参数
# opt.set_headless()

# 创建chrome无界面对象
driver = webdriver.Chrome(options=opt)

months = ['01', '02', '03', '04', '05', '06']

soBooks = []

soBookPre = 'https://sobooks.cc/'

for month in months:
    soBook = 'books/date/2018/' + month
    driver.get(soBookPre + soBook)
    print(soBookPre + soBook)
    pages = int(driver.find_element_by_xpath("//div[@class='pagination']//li[last()]").text.replace('共 ', '').replace(' 页', ''))
    page = 1
    while page <= pages:
        soBooks.insert(len(soBooks) + 1, soBook + "/page/" + str(page))
        print(soBook + "/page/" + str(page))
        page += 1

errorFile = open('sobooks_error.txt', 'a')

for soBook in soBooks:
    
    resultFile = open(soBook.replace('/', '_') + ".html", "a")

    soLink = soBookPre + soBook

    driver.get(soLink)

    if "404" == driver.title:
        print('出错啦')
        errorFile.write(driver.title + " " + soLink + "\n")
        continue

    books = driver.find_elements_by_xpath("//div[@id='cardslist']//h3/a")
    links = []
    for n, book in enumerate(books):
        links.insert(n + 1, book.get_attribute('href'))
    for link in links:
        try:
            driver.get(link)
            pan = driver.find_element_by_xpath("//i[@class='fa fa-download']/following-sibling::a[1]")
            if '百度网盘' != pan.text:
                errorFile.write(driver.title + ' ' + link + '\n')
                continue
            panLink = pan.get_attribute('href').replace('https://sobooks.cc/go.html?url=', '')
            panText = pan.text
            print(panLink)
            driver.find_element_by_xpath("//input[@name='e_secret_key']").send_keys('201818')
            driver.find_element_by_xpath("//input[@type='submit']").click()
            panSecret = driver.find_element_by_xpath("//div[@class='e-secret']/strong").text.replace('提取密码：', '')
            print(panSecret)
            resultFile.write("<a href='" + panLink + "' target='_blank'>" + driver.title + "</a>&nbsp;" + panSecret + "<br>\n")
        finally:
            errorFile.write(link + '\n')
    
    resultFile.close()
driver.quit()
errorFile.close()
