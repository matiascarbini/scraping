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

  precio = element.find('p', 'styles__BestPrice-sc-1ovmlws-12') 
  
  return precio.text.split('$')[1]