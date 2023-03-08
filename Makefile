include .env

build:
		docker build -t micropack-precios .

run:
		docker run --name scraping -p 5000:5000 -v $(PATH_APP):/app micropack-precios python /app/main.py

stop:
		docker stop micropack-precios

clean:
		docker rm micropack-precios
