from selenium import webdriver
import os

def init():
  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')

  DRIVER_PATH = '/home/matias/DESARROLLO/PYTHON/scraping/modules/webdriver/chromedriver108'  
  if os.name == 'nt':
    DRIVER_PATH = 'C:\\xampp\\htdocs\\scraping\\modules\\webdriver\\chromedriver.exe'

  return webdriver.Chrome(DRIVER_PATH, chrome_options=chrome_options)

def quit(driver):
  driver.quit()