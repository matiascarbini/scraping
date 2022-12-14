import pandas as pd

def importCSV(path_file):
  return pd.read_csv(path_file, sep=';', keep_default_na=False)  

def createDF():  
  pd.set_option('mode.chained_assignment', None)
  return pd.DataFrame()

def exportCSV(path_file, dataframe: pd.DataFrame):
  dataframe.to_csv(path_file, sep=';', index=False)