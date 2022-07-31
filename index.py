import modules.driver as chrome

import modules.data.csv as csv
from os.path import abspath

import modules.scan.lagallega as site1
import modules.scan.lareinaonline as site2
import modules.scan.carrefour as site3
import modules.scan.unicosupermercados as site4
import modules.scan.arcoirisencasa as site5
import modules.scan.hiperlibertad as site6
import modules.scan.cotodigital3 as site7
import modules.scan.jumbo as site8

driver = chrome.init()
print("inicio browser driver")

result = csv.createDF()
input = csv.importCSV(abspath('result/input.csv'))
print("importacion csv")

arrProd = []
for name in input["productos"]: 
  arrProd.append(name)
  
result['productos'] = arrProd
print("agrego columnas productos")

result['lagallega'] = site1.searchPriceLote(driver, input["lagallega"])  
print("agrego columnas <lagallega>")

result['lareinaonline'] = site2.searchPriceLote(driver, input["lareinaonline"]) 
print("agrego columnas <lareinaonline>")

result['carrefour'] = site3.searchPriceLote(driver, input["carrefour"]) #chequear precios
print("agrego columnas <carrefour>")

result['unicosupermercados'] = site4.searchPriceLote(driver, input["unicosupermercados"]) 
print("agrego columnas <unicosupermercados>")

result['arcoirisencasa'] = site5.searchPriceLote(driver, input["arcoirisencasa"]) 
print("agrego columnas <arcoirisencasa>")

result['hiperlibertad'] = site6.searchPriceLote(driver, input["hiperlibertad"]) 
print("agrego columnas <hiperlibertad>")

result['cotodigital3'] = site7.searchPriceLote(driver, input["cotodigital3"])
print("agrego columnas <cotodigital3>")

result['jumbo'] = site8.searchPriceLote(driver, input["jumbo"])
print("agrego columnas <jumbo>")

csv.exportCSV(abspath('result/result.csv'), result)
print("resultados exportados a CSV en carpeta <result>")

chrome.quit(driver)
print("finalizo browser driver")