from bs4 import BeautifulSoup
from selenium import webdriver
import pandas
import string

import modules.data.csv as csv
from os.path import abspath

import modules.webdriver.driver as chrome

from flask import Blueprint, request

lagallega_api = Blueprint('lagallega_api', __name__)

def getPriceLote(driver: webdriver, arrInput: pandas.DataFrame):    
  driver.get("https://www.lagallega.com.ar")
  
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

    isOferta = element.find('div', 'OferProd')    
    
    if isOferta == None:    
      element = element.find('div', 'DetallPrec')
      element = element.find('div', 'izq') 
      precio = element.find('b') 
      
      if precio.text:
        return precio.text.split('$')[1]
    else:
      element = element.find('div', 'DetallPrec')
      element = element.find('div', 'izq') 
      precio = element.find('b') 
      
      if precio.text:
        return '* ' + precio.text.split('$')[1]

    return 'ERR'
  except:
    return 'ERR'

@lagallega_api.route('/lagallega/get_price', methods=["GET"])
def getPriceByURL():
  url = request.args.get('url')
  pos = request.args.get('pos')

  if url is not None:
    driver = chrome.init()    
    driver.get("https://www.lagallega.com.ar")
    driver.get(url)    
    html = driver.page_source    
    chrome.quit(driver)

    val = parse(html)    
    
    if pos is not None:            
      output = csv.importCSV(abspath('result/output.csv'))
      output.at[int(pos),'lagallega'] = val
      csv.exportCSV(abspath('result/output.csv'), output) 

    return val
  else: 
    return 'SD'