from unicodedata import decimal
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas
import string
import time 

def searchPriceLote(driver: webdriver, arrInput: pandas.DataFrame, sleep: int):      
  driver.get("https://www.carrefour.com.ar")
  time.sleep(sleep)

  arrPrices = []
  for url in arrInput: 
    if url:
      arrPrices.append(getPrice(driver, url, sleep))
    else:
      arrPrices.append(0)
    
  return arrPrices

def getPrice(driver: webdriver, url: string, sleep: int): 
  driver.get(url)
  time.sleep(sleep)
  
  html = driver.page_source    
  element = BeautifulSoup(html, 'lxml')
  
  element = element.find('span', 'lyracons-carrefourarg-product-price-1-x-sellingPriceValue') 
  precio = element.find('span', 'lyracons-carrefourarg-product-price-1-x-currencyInteger') 
  decimal = element.find('span', 'lyracons-carrefourarg-product-price-1-x-currencyFraction')  
  
  if precio.text and decimal.text:
    return precio.text + '.' + decimal.text
  else:
    return 0