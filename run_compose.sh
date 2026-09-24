docker compose down -v
docker compose up -d --build

sleep 3

docker compose ps
docker compose exec api python manage.py makemigrations

sleep 3

docker compose exec api python manage.py migrate