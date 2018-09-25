#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from threading import Thread
import re

# 创建chrome参数对象
opt = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings": {"images":2}}
opt.add_experimental_option("prefs", prefs)
# 把chrome设置成无界面模式，不论windows还是linux都可以，自动适配对应参数
# opt.set_headless()

# 创建chrome无界面对象
driver = webdriver.Chrome(options=opt)
#driver.maximize_window()

address = 'https://sobooks.cc/books/date/2018/06/page/2'

driver.get(address)

master = driver.current_window_handle

books = driver.find_elements_by_xpath("//div[@id='cardslist']//h3/a")
links = []
for n, book in enumerate(books):
  links.append(book.get_attribute('href'))
for link in links:
    js='window.open("' + link +'");'
    driver.execute_script(js)
handles = driver.window_handles
for handle in handles:
  try:
    if handle == master:
        continue
    driver.switch_to_window(handle)
    pan = driver.find_element_by_xpath("//i[@class='fa fa-download']/following-sibling::a[1]")
    if '百度网盘' != pan.text:
      errorFile.write(driver.title + ' ' + link + '\n')
      continue
    panLink = pan.get_attribute('href').replace('https://sobooks.cc/go.html?url=', '')
    panText = pan.text
    print(panLink)
    driver.find_element_by_xpath("//input[@name='e_secret_key']").send_keys('201818')
    driver.find_element_by_xpath("//input[@type='submit']").click()
    print(panLink)
    panSecret = driver.find_element_by_xpath("//div[@class='e-secret']/strong").text.replace('提取密码：', '')
    print(panSecret)
    ActionChains(driver).key_down(Keys.CONTROL).send_keys("t").key_up(Keys.CONTROL).perform()
    driver.get(panLink)
    driver.find_element_by_xpath("//dl[@class='pickpw clearfix']//input[1]").send_keys(panSecret)
  except:
    continue
Thread.sleep()
