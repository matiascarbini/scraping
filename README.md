# scraping

## Instalar librerias
- `sudo apt-get update -y`
- `sudo apt-get install -y chromium-chromedriver`

## Crear entorno virtual
- `pip install virtualenv`
- `mkdir <YOURPROJECT>` Crear una nueva carpeta contenedora del proyecto
- `virtualenv <YOURPROJECT>` Crear el entorno virtual
- `cd <YOURPROJECT>` Moverse a la carpeta
- `source bin/activate` Activar el entorno virtual
- `deactivate`

## Instalar requirements.txt
- `pip install -r requirements.txt`

## Entrada de Datos
- En la carpeta result, cambiar nombre al archivo `input-example.csv` a `input.csv`
- Cargar datos segun la estructura del archivo
- El script devuelve un archivo `result.csv` con la misma estructura mostrando los precios obtenidos por cada item
## Iniciar proyecto
- `python3 index.py`