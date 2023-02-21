import pandas as pd
import csv

def importCSV(path_file):
  return pd.read_csv(path_file, sep=';', keep_default_na=False)  

def createDF():  
  pd.set_option('mode.chained_assignment', None)
  return pd.DataFrame()

def exportCSV(path_file, dataframe: pd.DataFrame):
  dataframe.to_csv(path_file, sep=';', index=False)

def exportCSVFromDatabase(path_file, data):
  nombre_archivo = path_file
  encabezado = [i[0] for i in data.description]
  
  with open(nombre_archivo, 'w', newline='') as archivo:
      escritor_csv = csv.writer(archivo, delimiter=';')
      escritor_csv.writerow(encabezado)
      escritor_csv.writerows(data.fetchall())