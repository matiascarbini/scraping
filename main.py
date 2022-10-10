from cmath import nan
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
import os

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

def createOutput(input):  
  output = csv.createDF()

  colMicropackId = []
  colProductos = []
  colLagallega = []
  colLareinaonline  = []
  colCarrefour  = []
  colUnicosupermercados  = []
  colArcoirisencasa  = []
  colHiperlibertad  = []
  colCotodigital3  = []
  colJumbo  = []

  for row in input:        
    for cell in input[row]:  
      if row == "micropack_id":        
        colMicropackId.append(cell)

      if row == "productos":        
        colProductos.append(cell)

      if row == "lagallega":           
        if cell and cell.strip(): 
          colLagallega.append(0)
        else:
          colLagallega.append("SD")

      if row == "lareinaonline":       
        if cell and cell.strip(): 
          colLareinaonline.append(0)
        else:
          colLareinaonline.append("SD")

      if row == "carrefour":       
        if cell and cell.strip(): 
          colCarrefour.append(0)
        else:
          colCarrefour.append("SD")

      if row == "unicosupermercados":       
        if cell and cell.strip(): 
          colUnicosupermercados.append(0)
        else:
          colUnicosupermercados.append("SD")

      if row == "arcoirisencasa":       
        if cell and cell.strip(): 
          colArcoirisencasa.append(0)
        else:
          colArcoirisencasa.append("SD")

      if row == "hiperlibertad":       
        if cell and cell.strip(): 
          colHiperlibertad.append(0)
        else:
          colHiperlibertad.append("SD")

      if row == "cotodigital3":       
        if cell and cell.strip(): 
          colCotodigital3.append(0)
        else:
          colCotodigital3.append("SD")

      if row == "jumbo":       
        if cell and cell.strip(): 
          colJumbo.append(0)
        else:
          colJumbo.append("SD")

  output['micropack_id'] = colMicropackId
  output['productos'] = colProductos
  output['lagallega'] = colLagallega
  output['lareinaonline'] = colLareinaonline
  output['carrefour'] = colCarrefour
  output['unicosupermercados'] = colUnicosupermercados
  output['arcoirisencasa'] = colArcoirisencasa
  output['hiperlibertad'] = colHiperlibertad
  output['cotodigital3'] = colCotodigital3
  output['jumbo'] = colJumbo
  
  csv.exportCSV(abspath('result/output.csv'), output)  
  return csv.importCSV(abspath('result/output.csv'))

@app.route('/', methods=["GET"])
def getInit():  
  return 'RECOPILADOR PRECIOS'

@app.route('/all/get_price', methods=["GET"])
def getPrice():    
  col = request.args.get('col')
  top = request.args.get('top')
  
  driver = chrome.init()    
  input = csv.importCSV(abspath('result/input.csv'))
    
  if os.path.exists('result/output.csv') == True:
    output = csv.importCSV(abspath('result/output.csv'))
  else:
    output = createOutput(input)    

  result = csv.createDF()  
  result['micropack_id'] = output['micropack_id']
  result['productos'] = output['productos']
  result['lagallega'] = output['lagallega']
  result['lareinaonline'] = output['lareinaonline']
  result['carrefour'] = output['carrefour']
  result['unicosupermercados'] = output['unicosupermercados']
  result['arcoirisencasa'] = output['arcoirisencasa']
  result['hiperlibertad'] = output['hiperlibertad']
  result['cotodigital3'] = output['cotodigital3']
  result['jumbo'] = output['jumbo']
  
  if col is None:  
    if top is None:  
      result['lagallega'] = site1.getPriceLote(driver, input["lagallega"])  
      result['lareinaonline'] = site2.getPriceLote(driver, input["lareinaonline"])       
      result['carrefour'] = site3.getPriceLote(driver, input["carrefour"]) 
      result['unicosupermercados'] = site4.getPriceLote(driver, input["unicosupermercados"]) 
      result['arcoirisencasa'] = site5.getPriceLote(driver, input["arcoirisencasa"]) 
      result['hiperlibertad'] = site6.getPriceLote(driver, input["hiperlibertad"]) 
      result['cotodigital3'] = site7.getPriceLote(driver, input["cotodigital3"])
      result['jumbo'] = site8.getPriceLote(driver, input["jumbo"])
    else: 
      result['lagallega'][0:int(top)] = site1.getPriceLote(driver, input["lagallega"].head(int(top)))
      result['lareinaonline'][0:int(top)] = site2.getPriceLote(driver, input["lareinaonline"].head(int(top)))
      result['carrefour'][0:int(top)] = site3.getPriceLote(driver, input["carrefour"].head(int(top)))
      result['unicosupermercados'][0:int(top)] = site4.getPriceLote(driver, input["unicosupermercados"].head(int(top)))
      result['arcoirisencasa'][0:int(top)] = site5.getPriceLote(driver, input["arcoirisencasa"].head(int(top)))
      result['hiperlibertad'][0:int(top)] = site6.getPriceLote(driver, input["hiperlibertad"].head(int(top)))
      result['cotodigital3'][0:int(top)] = site7.getPriceLote(driver, input["cotodigital3"].head(int(top)))
      result['jumbo'][0:int(top)] = site8.getPriceLote(driver, input["jumbo"].head(int(top)))
  else: 
    if col == 'lagallega':
      if top is None:  
        result['lagallega'] = site1.getPriceLote(driver, input["lagallega"])  
      else:
        result['lagallega'][0:int(top)] = site1.getPriceLote(driver, input["lagallega"].head(int(top)))
  
    if col == 'lareinaonline':
      if top is None:  
        result['lareinaonline'] = site2.getPriceLote(driver, input["lareinaonline"])        
      else:
        result['lareinaonline'][0:int(top)] = site2.getPriceLote(driver, input["lareinaonline"].head(int(top))) 

    if col == 'carrefour':
      if top is None:  
        result['carrefour'] = site3.getPriceLote(driver, input["carrefour"]) 
      else:
        result['carrefour'][0:int(top)] = site3.getPriceLote(driver, input["carrefour"].head(int(top)))
      
    if col == 'unicosupermercados':
      if top is None:  
        result['unicosupermercados'] = site4.getPriceLote(driver, input["unicosupermercados"]) 
      else:
        result['unicosupermercados'][0:int(top)] = site4.getPriceLote(driver, input["unicosupermercados"].head(int(top)))
                  
    if col == 'arcoirisencasa':
      if top is None:  
        result['arcoirisencasa'] = site5.getPriceLote(driver, input["arcoirisencasa"]) 
      else:
        result['arcoirisencasa'][0:int(top)] = site5.getPriceLote(driver, input["arcoirisencasa"].head(int(top)))
      
    if col == 'hiperlibertad':
      if top is None:  
        result['hiperlibertad'] = site6.getPriceLote(driver, input["hiperlibertad"]) 
      else:
        result['hiperlibertad'][0:int(top)] = site6.getPriceLote(driver, input["hiperlibertad"].head(int(top)))
      
    if col == 'cotodigital3':
      if top is None:  
        result['cotodigital3'] = site7.getPriceLote(driver, input["cotodigital3"])
      else:
        result['cotodigital3'][0:int(top)] = site7.getPriceLote(driver, input["cotodigital3"].head(int(top)))
      
    if col == 'jumbo':
      if top is None:  
        result['jumbo'] = site8.getPriceLote(driver, input["jumbo"])
      else:
        result['jumbo'][0:int(top)] = site8.getPriceLote(driver, input["jumbo"].head(int(top)))
            
  csv.exportCSV(abspath('result/output.csv'), result)  
  chrome.quit(driver)
  
  return result.to_json()

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=False, port=5000)