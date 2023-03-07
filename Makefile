include .env

build:
		sudo docker build -t micropack-precios .

run:
		sudo docker run -p 5000:5000 -v $(PATH_APP):/app micropack-precios python /app/main.py

stop:
		sudo docker stop micropack-precios

clean:
		sudo docker rm micropack-precios
