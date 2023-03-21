import modules.scan.lagallega as site1
import modules.scan.lareinaonline as site2
import modules.scan.carrefour as site3
import modules.scan.arcoirisencasa as site5
import modules.scan.hiperlibertad as site6
import modules.scan.cotodigital3 as site7

import modules.data.csvHelper as csv
import modules.data.sqlite as sqlite

from os.path import abspath
import os

import modules.webdriver.driver as chrome

from flask import Flask, request, send_file, redirect
from flask_cors import CORS

from modules.scan.arcoirisencasa import arcoirisencasa_api
from modules.scan.carrefour import carrefour_api
from modules.scan.cotodigital3 import cotodigital3_api
from modules.scan.hiperlibertad import hiperlibertad_api
from modules.scan.lagallega import lagallega_api
from modules.scan.lareinaonline import lareinaonline_api

app = Flask(__name__)
CORS(app)

app.register_blueprint(arcoirisencasa_api)
app.register_blueprint(carrefour_api)
app.register_blueprint(cotodigital3_api)
app.register_blueprint(hiperlibertad_api)
app.register_blueprint(lagallega_api)
app.register_blueprint(lareinaonline_api)

def createOutput(input):  
  sqlite.insert_input(input)
  input = sqlite.select_input()
  
  output = csv.createDF()

  colMicropackId = []
  colProductos = []
  colLagallega = []
  colLareinaonline  = []
  colCarrefour  = []
  colArcoirisencasa  = []
  colHiperlibertad  = []
  colCotodigital3  = []

  for row in input:
    for indice, cell in enumerate(row):  

      if indice == 0: #micropack_id        
        colMicropackId.append(cell)

      if indice == 1: #productos        
        colProductos.append(cell)

      if indice == 2: #lagallega
        if cell and cell.strip(): 
          colLagallega.append(0)
        else:
          colLagallega.append("SD")

      if indice == 3: #lareinaonline
        if cell and cell.strip(): 
          colLareinaonline.append(0)
        else:
          colLareinaonline.append("SD")

      if indice == 4: #carrefour
        if cell and cell.strip(): 
          colCarrefour.append(0)
        else:
          colCarrefour.append("SD")
      
      if indice == 5: #arcoirisencasa
        if cell and cell.strip(): 
          colArcoirisencasa.append(0)
        else:
          colArcoirisencasa.append("SD")

      if indice == 6: #hiperlibertad      
        if cell and cell.strip(): 
          colHiperlibertad.append(0)
        else:
          colHiperlibertad.append("SD")

      if indice == 7: #cotodigital3
        if cell and cell.strip(): 
          colCotodigital3.append(0)
        else:
          colCotodigital3.append("SD")

  output['micropack_id'] = colMicropackId
  output['productos'] = colProductos
  output['lagallega'] = colLagallega
  output['lareinaonline'] = colLareinaonline
  output['carrefour'] = colCarrefour  
  output['arcoirisencasa'] = colArcoirisencasa
  output['hiperlibertad'] = colHiperlibertad
  output['cotodigital3'] = colCotodigital3
  
  sqlite.insert_output(output)
  return sqlite.select_output()
  
@app.route('/', methods=["GET"])
def getInit():  
  if os.path.exists('result/input.csv') == True:
    return "SI"
  else: 
    return "NO"

@app.route('/force_generate_output', methods=["GET"])
def forceGenerateOutput():  
  input = csv.importCSV(abspath('result/input.csv'))    
  output = createOutput(input)      

  return output

@app.route('/upload', methods=["POST"])
def upload():  
  uploaded_file = request.files['file']
  if uploaded_file.filename != '':
    uploaded_file.filename = 'input.csv'
    uploaded_file.save('result/' + uploaded_file.filename)  
  
  forceGenerateOutput()
  
  return redirect(request.host + "/index.html", code=302)

@app.route('/download_output', methods=["GET"])
def downloadOutput():  
  path = "result/output.csv"
  return send_file(path, as_attachment=True)

@app.route('/select/input', methods=["GET"])
def selectInput():
  return sqlite.select_input()

@app.route('/select/output', methods=["GET"])
def selectOutput():
  return sqlite.select_output()

@app.route('/all/get_price', methods=["GET"])
def getPrice():    
  col = request.args.get('col')
  
  driver = chrome.init()    
  input = sqlite.select_input()
     
  if col is None:  
    site1.getPriceLote(driver, input, "lagallega")    
    site2.getPriceLote(driver, input, "lareinaonline")    
    site3.getPriceLote(driver, input, "carrefour")           
    site5.getPriceLote(driver, input, "arcoirisencasa")     
    site6.getPriceLote(driver, input, "hiperlibertad")     
    site7.getPriceLote(driver, input, "cotodigital3")          
  else: 
    if col == 'lagallega':     
      site1.getPriceLote(driver, input, "lagallega")  
  
    if col == 'lareinaonline':      
      site2.getPriceLote(driver, input, "lareinaonline")              
      
    if col == 'carrefour':
      site3.getPriceLote(driver, input, "carrefour") 
      
    if col == 'arcoirisencasa':      
      site5.getPriceLote(driver, input, "arcoirisencasa")       
      
    if col == 'hiperlibertad':      
      site6.getPriceLote(driver, input, "hiperlibertad")       
            
    if col == 'cotodigital3':
      site7.getPriceLote(driver, input, "cotodigital3")      
    
  chrome.quit(driver)

  return ''             

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True, port=5000)