from bs4 import BeautifulSoup
from selenium import webdriver
import pandas
import string

import modules.webdriver.driver as chrome

from flask import Blueprint, request

arcoirisencasa_api = Blueprint('arcoirisencasa_api', __name__)

def getPriceLote(driver: webdriver, arrInput: pandas.DataFrame):    
  driver.get("https://arcoirisencasa.com.ar")
  
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

@arcoirisencasa_api.route('/arcoirisencasa/get_price', methods=["GET"])
def getPriceByURL():       
  url = request.args.get('url')
  
  if url is not None:
    driver = chrome.init()    
    driver.get("https://arcoirisencasa.com.ar")
    driver.get(url)    
    html = driver.page_source    
    chrome.quit(driver)
    
    return parse(html)    
  else: 
    return '-- No se cargo la url << ARCOIRISENCASA >> --'