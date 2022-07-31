import pandas as pd

def importCSV(path_file):
  return pd.read_csv(path_file)  

def createDF():
  return pd.DataFrame()

def exportCSV(path_file, dataframe: pd.DataFrame):
  dataframe.to_csv(path_file)