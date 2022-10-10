from unicodedata import decimal
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas
import string
import time 
import sys

import modules.webdriver.driver as chrome

from flask import Blueprint, request

carrefour_api = Blueprint('carrefour_api', __name__)

def getPriceLote(driver: webdriver, arrInput: pandas.DataFrame):      
  driver.get("https://www.carrefour.com.ar")

  if(len(sys.argv) == 2):    
    time.sleep(int(sys.argv[1]))  

  arrPrices = []
  for url in arrInput: 
    if url:
      arrPrices.append(getPrice(driver, url))
    else:
      arrPrices.append(0)
    
  return arrPrices

def getPrice(driver: webdriver, url: string):   
  driver.get(url)
  
  if(len(sys.argv) == 2):    
    time.sleep(int(sys.argv[1]))  
  
  html = driver.page_source      
  return parse(html)  

def parse(html: string):
  element = BeautifulSoup(html, 'lxml')  
  element = element.find('span', 'lyracons-carrefourarg-product-price-1-x-sellingPriceValue') 
  
  if element:
    arrPrecio = element.find_all('span', 'lyracons-carrefourarg-product-price-1-x-currencyInteger')                         
    
    precio = ""
    for p in arrPrecio: 
      precio = str(precio) + str(p.text)
      
    decimal = element.find('span', 'lyracons-carrefourarg-product-price-1-x-currencyFraction')  
            
    if precio and decimal.text:
      return precio + '.' + decimal.text
    else:
      return 0
  else:
    return 0
          
@carrefour_api.route('/carrefour/get_price', methods=["GET"])
def getPriceByURL():   
  url = request.args.get('url')
  
  if url is not None:
    driver = chrome.init()    
    driver.get("https://www.carrefour.com.ar")
    driver.get(url)    
    html = driver.page_source    
    chrome.quit(driver)
    
    return parse(html)    
  else: 
    return 'SD'