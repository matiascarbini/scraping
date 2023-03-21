# -------------
# BUILD
# -------------
build-back:
		docker build -t precios_back -f ./docker/python/Dockerfile .		

build-front:
		docker build -t precios_front -f ./docker/nginx/Dockerfile .

# -------------
# UP
# -------------
up:
	docker-compose -f docker-compose.yml up -d

# -------------
# DOWN
# -------------
down:
	docker-compose -f docker-compose.yml down

# -------------
# DEPLOY
# -------------
deploy: build-back build-front up
