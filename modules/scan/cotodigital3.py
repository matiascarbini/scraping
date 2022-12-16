from bs4 import BeautifulSoup
from selenium import webdriver
import pandas
import string

import modules.data.csv as csv
from os.path import abspath

import modules.webdriver.driver as chrome

from flask import Blueprint, request

cotodigital3_api = Blueprint('cotodigital3_api', __name__)

def getPriceLote(driver: webdriver, arrInput: pandas.DataFrame):      
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

    isOferta = element.find('span', 'price_discount')    
    
    if isOferta == None:
      element = element.find('span', 'atg_store_newPrice') 
    
      if element.text.find('$') >= 0:
        pos = element.text.find('$') + 1
        count = len(element.text)
        precio = element.text[pos:count].strip()

        if precio.find('.') >= 0:
          pos1 = precio.find('.') + 1
          decimal = precio[pos1:pos1 + 2].strip()
          precio = precio[0:pos1-1] + ',' + decimal               

        return precio
      
      return 'ERR'
    else:
      element = isOferta

      if element.text.find('$') >= 0:
        pos = element.text.find('$') + 1
        count = len(element.text)
        precio = element.text[pos:count].strip()
        
        if precio.find('.') >= 0:
          pos1 = precio.find('.') + 1
          decimal = precio[pos1:pos1 + 2].strip()
          precio = precio[0:pos1-1] + ',' + decimal                      

        return '* ' + precio
      
      return 'ERR'
  except:
    return 'ERR'
  
@cotodigital3_api.route('/cotodigital3/get_price', methods=["GET"])
def getPriceByURL():       
  url = request.args.get('url')
  pos = request.args.get('pos')
  
  if url is not None:
    driver = chrome.init()    
    driver.get("https://cotodigital3.com.ar")
    driver.get(url)    
    html = driver.page_source    
    chrome.quit(driver)
    
    val = parse(html)    
    
    if pos is not None:            
      output = csv.importCSV(abspath('result/output.csv'))
      output.at[int(pos),'cotodigital3'] = val
      csv.exportCSV(abspath('result/output.csv'), output)  

    return val  
  else: 
    return 'SD'