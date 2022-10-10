from bs4 import BeautifulSoup
from selenium import webdriver
import pandas
import string

import modules.data.csv as csv
from os.path import abspath

import modules.webdriver.driver as chrome

from flask import Blueprint, request

unicosupermercados_api = Blueprint('unicosupermercados_api', __name__)

def getPriceLote(driver: webdriver, arrInput: pandas.DataFrame):      
  driver.get("https://www.unicosupermercados.com.ar")
  
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
  return parse(html)    

def parse(html: string):
  element = BeautifulSoup(html, 'lxml')

  element = element.find('div', 'DetallPrec')

  element = element.find('div', 'izq') 
  precio = element.find('b') 
  
  if precio.text:
    return precio.text.split('$')[1]
  else:
    return 0

@unicosupermercados_api.route('/unicosupermercados/get_price', methods=["GET"])
def getPriceByURL():
  url = request.args.get('url')
  pos = request.args.get('pos')

  if url is not None:
    driver = chrome.init()    
    driver.get("https://www.unicosupermercados.com.ar")
    driver.get(url)    
    html = driver.page_source    
    chrome.quit(driver)
    
    val = parse(html)    
    
    if pos is not None:            
      output = csv.importCSV(abspath('result/output.csv'))
      output[int(pos),'unicosupermercados'] = val
      csv.exportCSV(abspath('result/output.csv'), output)  

    return val   
  else: 
    return 'SD'