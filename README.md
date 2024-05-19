Comandos:

docker-compose down --rmi all
docker-compose up --build

Em outro console:

docker cp initialize_databases.py api_1:/app/initialize_databases.py
docker exec -it api_1 python /app/initialize_databases.py 
