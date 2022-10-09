import modules.scan.lagallega as site1
import modules.scan.lareinaonline as site2
import modules.scan.carrefour as site3
import modules.scan.unicosupermercados as site4
import modules.scan.arcoirisencasa as site5
import modules.scan.hiperlibertad as site6
import modules.scan.cotodigital3 as site7
import modules.scan.jumbo as site8

import modules.data.csv as csv
from os.path import abspath

import modules.webdriver.driver as chrome

from flask import Flask, request

from modules.scan.arcoirisencasa import arcoirisencasa_api
from modules.scan.carrefour import carrefour_api
from modules.scan.cotodigital3 import cotodigital3_api
from modules.scan.hiperlibertad import hiperlibertad_api
from modules.scan.jumbo import jumbo_api
from modules.scan.lagallega import lagallega_api
from modules.scan.lareinaonline import lareinaonline_api
from modules.scan.unicosupermercados import unicosupermercados_api

app = Flask(__name__)

app.register_blueprint(arcoirisencasa_api)
app.register_blueprint(carrefour_api)
app.register_blueprint(cotodigital3_api)
app.register_blueprint(hiperlibertad_api)
app.register_blueprint(jumbo_api)
app.register_blueprint(lagallega_api)
app.register_blueprint(lareinaonline_api)
app.register_blueprint(unicosupermercados_api)

@app.route('/', methods=["GET"])
def getInit():  
  return 'RECOPILADOR PRECIOS'

@app.route('/all/get_price', methods=["GET"])
def getPrice():  
  col = request.args.get('col')
  
  """
    me quede aca, voy a hacer un top, para actualizar algunos registros
    poner el excel que mando tomas
    
    y ver que otra logica copada puede servir    
  """
  
  top = request.args.get('top')
  
  driver = chrome.init()  
  input = csv.importCSV(abspath('result/input.csv'))
  
  arrProd = []
  for name in input["productos"]: 
    arrProd.append(name)
  
  result = csv.createDF()
  result['productos'] = arrProd  
  
  if col is None:  
    result['lagallega'] = site1.getPriceLote(driver, input["lagallega"])  
    result['lareinaonline'] = site2.getPriceLote(driver, input["lareinaonline"])       
    result['carrefour'] = site3.getPriceLote(driver, input["carrefour"]) 
    result['unicosupermercados'] = site4.getPriceLote(driver, input["unicosupermercados"]) 
    result['arcoirisencasa'] = site5.getPriceLote(driver, input["arcoirisencasa"]) 
    result['hiperlibertad'] = site6.getPriceLote(driver, input["hiperlibertad"]) 
    result['cotodigital3'] = site7.getPriceLote(driver, input["cotodigital3"])
    result['jumbo'] = site8.getPriceLote(driver, input["jumbo"])
  else: 
    if col == 'lagallega':
      result['lagallega'] = site1.getPriceLote(driver, input["lagallega"])  
  
    if col == 'lareinaonline':
      result['lareinaonline'] = site2.getPriceLote(driver, input["lareinaonline"])        
      
    if col == 'carrefour':
      result['carrefour'] = site3.getPriceLote(driver, input["carrefour"]) 
      
    if col == 'unicosupermercados':
      result['unicosupermercados'] = site4.getPriceLote(driver, input["unicosupermercados"]) 
                  
    if col == 'arcoirisencasa':
      result['arcoirisencasa'] = site5.getPriceLote(driver, input["arcoirisencasa"]) 
      
    if col == 'hiperlibertad':
      result['hiperlibertad'] = site6.getPriceLote(driver, input["hiperlibertad"]) 
      
    if col == 'cotodigital3':
      result['cotodigital3'] = site7.getPriceLote(driver, input["cotodigital3"])
      
    if col == 'jumbo':
      result['jumbo'] = site8.getPriceLote(driver, input["jumbo"])                               
            
  csv.exportCSV(abspath('result/result.csv'), result)  
  chrome.quit(driver)
  
  return result

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=False, port=5000)