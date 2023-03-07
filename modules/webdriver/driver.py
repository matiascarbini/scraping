from selenium import webdriver
import os

def init():
  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')

  #https://chromedriver.chromium.org/downloads
  DRIVER_PATH = '/app/modules/webdriver/chromedriver'  
    
  return webdriver.Chrome(DRIVER_PATH, chrome_options=chrome_options)

def quit(driver):
  driver.quit()