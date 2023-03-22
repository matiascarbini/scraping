from bs4 import BeautifulSoup
from selenium import webdriver
import pandas
import string
import time
import modules.data.sqlite as sqlite
from os.path import abspath

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import modules.webdriver.driver as chrome

from flask import Blueprint, request

cotodigital3_api = Blueprint('cotodigital3_api', __name__)

def getPriceLote(driver: webdriver, arrInput, column):    
  val = None
  for indice, row in enumerate(arrInput): 
    url = row[7]
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

  WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located(
      (By.CSS_SELECTOR, ".atg_store_newPrice"),        
    )      
  )           

  html = driver.page_source  
  val = parse(html)

  if val != 'ERR' and float(gradual) > 0:
    isOferta = False
    if '*' in val:
      val = val[1:]
      isOferta = True

    val = float(val.replace(',','.')) * float(gradual)      
    val = round(val,2)
    val = str(val).replace('.',',')  

    if isOferta:
      val = '* ' + val

  val = val.replace('.','')    
  return val  
  
def parse(html: string):
  try:
    element = BeautifulSoup(html, 'lxml')

    element = element.find('div','info_productPrice')
    isOferta = element.find('span', 'price_discount')    
    
    if isOferta == None:
      element = element.find('span', 'atg_store_newPrice') 
    
      if element.text.find('$') >= 0:
        pos = element.text.find('$') + 1
        count = len(element.text)
        precio = element.text[pos:count].strip()

        if precio.find(',') >= 0:
          pos1 = precio.find(',') + 1
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

  gradual = '0'
  posGradual = url.find('|http')    
  if posGradual > 0:
    gradual = url[0 : posGradual]
    url = url[posGradual + 1 : len(url)]
  
  if url is not None:
    driver = chrome.init()         
    driver.get(url)    
    
    WebDriverWait(driver, 10).until(
      EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, ".atg_store_newPrice"),        
      )      
    )           

    html = driver.page_source    
    chrome.quit(driver)
    
    val = parse(html)        
    
    if val != 'ERR' and float(gradual) > 0:
      isOferta = False
      if '*' in val:
        val = val[1:]
        isOferta = True
           
      val = float(val.replace(',','.')) * float(gradual)      
      val = round(val,2)
      val = str(val).replace('.',',')

      if isOferta:
        val = '* ' + val
    
    val = val.replace('.','')    
    sqlite.insert_output_price(int(pos) + 1,'cotodigital3', val)      
    return val  
  else: 
    sqlite.insert_output_price(int(pos) + 1,'cotodigital3', 'SD')            
    return 'SD'