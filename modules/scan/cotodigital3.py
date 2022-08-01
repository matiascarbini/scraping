from bs4 import BeautifulSoup
from selenium import webdriver
import pandas
import string

def searchPriceLote(driver: webdriver, arrInput: pandas.DataFrame):      
  arrPrices = []
  for url in arrInput: 
    if url:
      arrPrices.append(getPrice(driver, url))
    else:
      arrPrices.append(0)
    
  return arrPrices

def getPrice(driver: webdriver, url: string): 
  driver.get(url)
  
  html = driver.page_source  
  element = BeautifulSoup(html, 'lxml')

  element = element.find('span', 'atg_store_newPrice') 
  
  if element.text.find('$') >= 0:
    pos = element.text.find('$') + 1
    count = len(element.text)
    precio = element.text[pos:count].strip()
    
    return precio
  else:
    return 0