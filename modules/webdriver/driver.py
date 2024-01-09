from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import os

#https://chromedriver.chromium.org/downloads
#https://googlechromelabs.github.io/chrome-for-testing/

def init():
  options = Options()
  options.browser_version = "120"
  options.executable_path = '/app/modules/webdriver/chromedriver'  
  options.add_argument('--headless')
  options.add_argument('--no-sandbox')
  options.add_argument('--disable-dev-shm-usage')

  return webdriver.Chrome(options=options)

def quit(driver):
  driver.quit()