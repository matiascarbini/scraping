from bs4 import BeautifulSoup
from selenium import webdriver
import pandas
import string

import modules.webdriver.driver as chrome

from flask import Blueprint, request

cotodigital3_api = Blueprint('cotodigital3_api', __name__)

def getPriceLote(driver: webdriver, arrInput: pandas.DataFrame):      
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
    
  element = element.find('span', 'atg_store_newPrice') 
  
  if element.text.find('$') >= 0:
    pos = element.text.find('$') + 1
    count = len(element.text)
    precio = element.text[pos:count].strip()
    
    return precio
  else:
    return 0
  
@cotodigital3_api.route('/cotodigital3/get_price', methods=["GET"])
def getPriceByURL():       
  url = request.args.get('url')
  
  if url is not None:
    driver = chrome.init()    
    driver.get("https://cotodigital3.com.ar")
    driver.get(url)    
    html = driver.page_source    
    chrome.quit(driver)
    
    return parse(html)    
  else: 
    return 'SD'