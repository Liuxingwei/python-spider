from selenium import webdriver
import re

# 创建chrome参数对象
opt = webdriver.ChromeOptions()

# 把chrome设置成无界面模式，不论windows还是linux都可以，自动适配对应参数
opt.set_headless()

# 创建chrome无界面对象
driver = webdriver.Chrome(options=opt)

# 访问百度
driver.get('http://www.mca.gov.cn/article/sj/xzqh/2018/201804-12/201804-06041553.html')

#打印内容
codes = driver.find_elements_by_xpath("//td[@class='xl7016293'][1]")
names = driver.find_elements_by_xpath("//td[@class='xl7016293'][2]")
result = []
level = ''

for n, e in enumerate(codes):
    if re.match('.*0000$', codes[n].text):
        level = '0'
    elif re.match('.*00$', codes[n].text):
        level = '1'
    else:
        level = '2'
    result.insert(n + 1, '{"code": "' + codes[n].text + '", "name": "' + names[n].text + '", "level":' + level + '}')
string = '[' + ','.join(result) + ']'

file = open("area.json", "w")
file.write(string)
file.close()
