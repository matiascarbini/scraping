from bs4 import BeautifulSoup
from selenium import webdriver
import pandas
import string

import modules.data.csv as csv
from os.path import abspath

import modules.webdriver.driver as chrome

from flask import Blueprint, request

hiperlibertad_api = Blueprint('hiperlibertad_api', __name__)

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

    isOferta = element.find('p', 'styles__ListPrice-prs94d-0 hBDooZ styles__ListPrice-sc-1ovmlws-11 bWTvgS')    
    
    if isOferta == None:
      precio = element.find('p', 'styles__BestPrice-sc-1ovmlws-12') 
    
      if precio.text: 
        return precio.text.split('$')[1]
    else:
      precio = element.find('p', 'styles__BestPrice-sc-1ovmlws-12') 
    
      if precio.text: 
        return '* ' + precio.text.split('$')[1]

    return 'ERR'
  except:
    return 'ERR'
  
@hiperlibertad_api.route('/hiperlibertad/get_price', methods=["GET"])
def getPriceByURL():       
  url = request.args.get('url')
  pos = request.args.get('pos')

  if url is not None:
    driver = chrome.init()    
    driver.get("https://hiperlibertad.com.ar")
    driver.get(url)    
    html = driver.page_source    
    chrome.quit(driver)
    
    val = parse(html)    
    
    if pos is not None:            
      output = csv.importCSV(abspath('result/output.csv'))
      output.at[int(pos),'hiperlibertad'] = val
      csv.exportCSV(abspath('result/output.csv'), output)  

    return val   
  else: 
    return 'SD'