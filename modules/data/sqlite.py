import sqlite3
import modules.data.csvHelper as csv

def connect():
  return sqlite3.connect('scraping.sqlite3')

def insert_input(data):
  conexion = connect()
  cursor = conexion.cursor()

  cursor.execute("DELETE FROM input")
  
  for index, row in data.iterrows():              
    cursor.execute("INSERT INTO input (id,micropack_id,productos,lagallega,lareinaonline,carrefour,arcoirisencasa,hiperlibertad,cotodigital3) VALUES ('" +
                    str(int(index) + 1) + "', '" +
                    str(row[0]).replace("'","''") + "', '" +
                    str(row[1]).replace("'","''") + "', '" +
                    str(row[2]).replace("'","''") + "', '" +
                    str(row[3]).replace("'","''") + "', '" +
                    str(row[4]).replace("'","''") + "', '" +
                    str(row[5]).replace("'","''") + "', '" +
                    str(row[6]).replace("'","''") + "', '" +
                    str(row[7]).replace("'","''") + "')")

  conexion.commit()
  conexion.close()

def select_input():
  conexion = connect()
  cursor = conexion.cursor()
  cursor.execute("SELECT micropack_id,productos,lagallega,lareinaonline,carrefour,arcoirisencasa,hiperlibertad,cotodigital3 FROM input")
  filas = cursor.fetchall()
  conexion.close()

  return filas

def insert_output(data):
  conexion = connect()
  cursor = conexion.cursor()

  cursor.execute("DELETE FROM output")

  for index, row in data.iterrows():        
    cursor.execute("INSERT INTO output (id,micropack_id,productos,lagallega,lareinaonline,carrefour,arcoirisencasa,hiperlibertad,cotodigital3) VALUES ('" +
                    str(int(index) + 1) + "', '" +
                    str(row[0]).replace("'","''") + "', '" +
                    str(row[1]).replace("'","''") + "', '" +
                    str(row[2]).replace("'","''") + "', '" +
                    str(row[3]).replace("'","''") + "', '" +
                    str(row[4]).replace("'","''") + "', '" +
                    str(row[5]).replace("'","''") + "', '" +
                    str(row[6]).replace("'","''") + "', '" +
                    str(row[7]).replace("'","''") + "')")

  conexion.commit()
  conexion.close()

  select_output()

def select_output():
  conexion = connect()
  cursor = conexion.cursor()
  cursor.execute("SELECT micropack_id,productos,lagallega,lareinaonline,carrefour,arcoirisencasa,hiperlibertad,cotodigital3 FROM output")
  csv.exportCSVFromDatabase('result/output.csv', cursor)
  conexion.close()  

  conexion = connect()
  cursor = conexion.cursor()
  cursor.execute("SELECT micropack_id,productos,lagallega,lareinaonline,carrefour,arcoirisencasa,hiperlibertad,cotodigital3 FROM output")  
  filas = cursor.fetchall()  
  conexion.close()  

  return filas

def insert_output_price(id, field, value):    
  conexion = connect()
  cursor = conexion.cursor()
  
  cursor.execute("UPDATE output SET " + str(field) + " = '" + str(value).replace("'","''") + "' WHERE id=" + str(id))
                 
  conexion.commit()
  conexion.close()

  select_output()