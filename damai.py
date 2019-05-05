#!/usr/bin/env python


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


opt = webdriver.ChromeOptions()

opt.add_argument(r"user-data-dir=/home/liuxingwei/chrome-config")
prefs = {"profile.managed_default_content_settings": {"images": 1}}
opt.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=opt)

driver.get('https://passport.damai.cn/login?ru=https%3A%2F%2Fwww.damai.cn%2F')

iframe = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//iframe[@id='alibaba-login-box']")))

driver.switch_to.frame('alibaba-login-box')

nameInput = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//input[@id='fm-login-id']")))

nameInput.send_keys('hello')

time.sleep(30)

driver.close()