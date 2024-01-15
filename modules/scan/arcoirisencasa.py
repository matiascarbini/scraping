from bs4 import BeautifulSoup
from selenium import webdriver
import pandas
import string
import time

import modules.data.sqlite as sqlite
from os.path import abspath

import modules.webdriver.driver as chrome

from flask import Blueprint, request

arcoirisencasa_api = Blueprint('arcoirisencasa_api', __name__)

def getPriceLote(driver: webdriver, arrInput, column):    
  driver.get("https://arcoirisencasa.com.ar")
  
  val = None
  for indice, row in enumerate(arrInput): 
    url = row[5]
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
    isOferta = False
    if '*' in val:
      val = val[1:]
      isOferta = True

    val = float(val.replace('.','').replace(',','.')) * float(gradual)        
    val = round(val,2) 
    val = str(val).replace('.',',')        

    if isOferta:
      val = '* ' + val

  val = val.replace('.','')    
  return val 
  
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

@arcoirisencasa_api.route('/arcoirisencasa/get_price', methods=["GET"])
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
    driver.get("https://arcoirisencasa.com.ar")
    driver.get(url)    
    time.sleep(1)
    html = driver.page_source    
    chrome.quit(driver)
    
    val = parse(html)    
    
    if val != 'ERR' and float(gradual) > 0:
      isOferta = False
      if '*' in val:
        val = val[1:]
        isOferta = True
              
      val = float(val.replace('.','').replace(',','.')) * float(gradual)        
      val = round(val,2)  
      val = str(val).replace('.',',')  
    
      if isOferta:
        val = '* ' + val

    val = val.replace('.','')    
    sqlite.insert_output_price(int(pos) + 1,'arcoirisencasa', val)      
    return val 
  else: 
    sqlite.insert_output_price(int(pos) + 1,'arcoirisencasa', 'SD')      
    return 'SD'