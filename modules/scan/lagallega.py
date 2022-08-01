from bs4 import BeautifulSoup
from selenium import webdriver
import pandas
import string

def searchPriceLote(driver: webdriver, arrInput: pandas.DataFrame):    
  driver.get("https://www.lagallega.com.ar")
  
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

  element = element.find('div', 'izq') 
  precio = element.find('b') 
  
  if precio.text:
    return precio.text.split('$')[1]
  else:
    return 0
  