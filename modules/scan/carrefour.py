from unicodedata import decimal
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas
import string
import time 
import sys

def searchPriceLote(driver: webdriver, arrInput: pandas.DataFrame):      
  driver.get("https://www.carrefour.com.ar")

  if(len(sys.argv) > 2):    
    time.sleep(sys.argv[1])  

  arrPrices = []
  for url in arrInput: 
    if url:
      arrPrices.append(getPrice(driver, url))
    else:
      arrPrices.append(0)
    
  return arrPrices

def getPrice(driver: webdriver, url: string): 
  driver.get(url)

  if(len(sys.argv) > 2):    
    time.sleep(sys.argv[1])  
  
  html = driver.page_source    
  element = BeautifulSoup(html, 'lxml')
  
  element = element.find('span', 'lyracons-carrefourarg-product-price-1-x-sellingPriceValue') 
  precio = element.find('span', 'lyracons-carrefourarg-product-price-1-x-currencyInteger') 
  decimal = element.find('span', 'lyracons-carrefourarg-product-price-1-x-currencyFraction')  
  
  if precio.text and decimal.text:
    return precio.text + '.' + decimal.text
  else:
    return 0