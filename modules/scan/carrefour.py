from unicodedata import decimal
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas
import string
import time 
import sys

import modules.data.csv as csv
from os.path import abspath

import modules.webdriver.driver as chrome

from flask import Blueprint, request

carrefour_api = Blueprint('carrefour_api', __name__)

def getPriceLote(driver: webdriver, arrInput: pandas.DataFrame):      
  driver.get("https://www.carrefour.com.ar")

  arrPrices = []
  for url in arrInput: 
    if url:
      arrPrices.append(getPrice(driver, url))
    else:
      arrPrices.append('SD')
    
  return arrPrices

def getPrice(driver: webdriver, url: string):   
  driver.get(url)
  html = driver.page_source      
  return parse(html)  

def parse(html: string):
  try:
    element = BeautifulSoup(html, 'lxml')  

    isOferta = element.find('span', 'lyracons-carrefourarg-product-price-1-x-listPrice')    
    
    if isOferta == None:    
      element = element.find('span', 'lyracons-carrefourarg-product-price-1-x-sellingPriceValue') 
    
      if element:
        arrPrecio = element.find_all('span', 'lyracons-carrefourarg-product-price-1-x-currencyInteger')                         
      
        precio = ""
        for p in arrPrecio: 
          precio = str(precio) + str(p.text)
        
        decimal = element.find('span', 'lyracons-carrefourarg-product-price-1-x-currencyFraction')  
              
        if precio and decimal.text:
          return precio + ',' + decimal.text
        else:
          return 'ERR'
    else:
      element = element.find('span', 'lyracons-carrefourarg-product-price-1-x-sellingPriceValue') 
    
      if element:
        arrPrecio = element.find_all('span', 'lyracons-carrefourarg-product-price-1-x-currencyInteger')                         
      
        precio = ""
        for p in arrPrecio: 
          precio = str(precio) + str(p.text)
        
        decimal = element.find('span', 'lyracons-carrefourarg-product-price-1-x-currencyFraction')  
              
        if precio and decimal.text:
          return '* ' + precio + ',' + decimal.text
        else:
          return 'ERR'

    return 'ERR'
  except:
    return 'ERR'
          
@carrefour_api.route('/carrefour/get_price', methods=["GET"])
def getPriceByURL():   
  url = request.args.get('url')
  pos = request.args.get('pos')
  
  if url is not None:
    driver = chrome.init()    
    driver.get("https://www.carrefour.com.ar")
    driver.get(url)    
    html = driver.page_source    
    chrome.quit(driver)
    
    val = parse(html)    
    
    if pos is not None:            
      output = csv.importCSV(abspath('result/output.csv'))
      output.at[int(pos),'carrefour'] = val
      csv.exportCSV(abspath('result/output.csv'), output)  

    return val 
  else: 
    return 'SD'