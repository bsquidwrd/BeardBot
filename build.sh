docker-compose up --build -d --remove-orphans

docker exec beardbot_bot_1 python manage.py migrate

docker-compose logs -f
