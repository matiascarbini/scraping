from selenium import webdriver
from bs4 import BeautifulSoup

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

DRIVER_PATH = '/usr/bin/chromedriver'
driver = webdriver.Chrome(DRIVER_PATH, chrome_options=chrome_options)

driver.get("https://www.lagallega.com.ar")
driver.get("https://www.lagallega.com.ar/Detalle.asp?Pr=779078710032")
html = driver.page_source

driver.quit()

soup = BeautifulSoup(html, 'lxml')

a = soup.find('div', 'izq') 
a = a.find('b') 
print(a.text.split('$')[1])