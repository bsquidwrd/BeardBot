#!/bin/sh
#pull latest image and restart bot

docker pull bsquidwrd/beardbot:latest
docker-compose down --remove-orphans 
sleep 5
docker-compose up --build -d --remove-orphans
docker exec beardbot_bot_1 python manage.py migrate
docker-compose logs -f
