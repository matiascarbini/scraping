from selenium import webdriver
import os

def init():
  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')

  DRIVER_PATH = '/usr/bin/chromedriver'  
  if os.name == 'nt':
    DRIVER_PATH = 'C:\_RobotPrecios\scraping\modules\chromedriver.exe'

  return webdriver.Chrome(DRIVER_PATH, chrome_options=chrome_options)

def quit(driver):
  driver.quit()