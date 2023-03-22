from unicodedata import decimal
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas
import string
import time 
import sys
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import modules.data.sqlite as sqlite
from os.path import abspath

import modules.webdriver.driver as chrome

from flask import Blueprint, request

carrefour_api = Blueprint('carrefour_api', __name__)

def getPriceLote(driver: webdriver, arrInput, column):      
  val = None
  for indice, row in enumerate(arrInput): 
    url = row[4]
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
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".lyracons-incompatible-cart-0-x-buttonContentText"))      
  )       
  WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".lyracons-carrefourarg-product-price-1-x-discountPercentage"))
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

    element = element.find('body')
    element = element.find('div','vtex-flex-layout-0-x-flexRowContent--product-view-product-main')       
    element = element.find('div','vtex-flex-layout-0-x-flexCol--product-view-details') 
    isOferta = element.find('span','lyracons-carrefourarg-product-price-1-x-listPrice')
    
    if isOferta == None:    
      isOferta = element.find('span','lyracons-carrefourarg-product-price-1-x-discountPercentage')
    
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
  
  gradual = '0'
  posGradual = url.find('|http')    
  if posGradual > 0:
    gradual = url[0 : posGradual]
    url = url[posGradual + 1 : len(url)]  

  if url is not None:
    driver = chrome.init()        
    driver.get(url)               

    WebDriverWait(driver, 10).until(
      EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".lyracons-incompatible-cart-0-x-buttonContentText"))      
    )       
    WebDriverWait(driver, 10).until(
      EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".lyracons-carrefourarg-product-price-1-x-discountPercentage"))
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
    sqlite.insert_output_price(int(pos) + 1,'carrefour', val)            
    return val 
  else: 
    sqlite.insert_output_price(int(pos) + 1,'carrefour', 'SD')            
    return 'SD'