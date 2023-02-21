from bs4 import BeautifulSoup
from selenium import webdriver
import pandas
import string

import modules.data.sqlite as sqlite
from os.path import abspath

import modules.webdriver.driver as chrome

from flask import Blueprint, request

hiperlibertad_api = Blueprint('hiperlibertad_api', __name__)

def getPriceLote(driver: webdriver, arrInput, column):    
  val = None
  for indice, row in enumerate(arrInput): 
    url = row[6]
    if url:
      val = getPrice(driver, url)
    else:
      val = 'SD'
    
    sqlite.insert_output_price(int(indice) + 1, column, val)      
    val = None

def getPrice(driver: webdriver, url: string):     
  gradual = '0'
  posGradual = url.find('|http')    
  if posGradual > 0:
    gradual = url[0 : posGradual]
    url = url[posGradual + 1 : len(url)]
  
  driver.get(url)
  html = driver.page_source  
  val = parse(html)

  if val != 'ERR' and float(gradual) > 0:
    val = float(val.replace(',','.')) * float(gradual)      
    val = str(val).replace('.',',')        

  val = val.replace('.','')    
  return val
  
def parse(html: string):
  try:
    element = BeautifulSoup(html, 'lxml')

    element = element.find('div','styles__Container-sc-1ovmlws-1')
    isOferta = element.find('p', 'styles__ListPrice-sc-1ovmlws-11')    
    
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

  gradual = '0'
  posGradual = url.find('|http')    
  if posGradual > 0:
    gradual = url[0 : posGradual]
    url = url[posGradual + 1 : len(url)]
    
  if url is not None:
    driver = chrome.init()    
    driver.get("https://hiperlibertad.com.ar")
    driver.get(url)    
    html = driver.page_source    
    chrome.quit(driver)
    
    val = parse(html)    

    if val != 'ERR' and float(gradual) > 0:
      val = float(val.replace(',','.')) * float(gradual)      
      val = str(val).replace('.',',')      
    
    val = val.replace('.','')    
    sqlite.insert_output_price(int(pos) + 1,'hiperlibertad', val)
    return val   
  else: 
    sqlite.insert_output_price(int(pos) + 1,'hiperlibertad', 'SD')            
    return 'SD'