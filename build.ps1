Clear-Host
docker build --rm -f "Dockerfile" -t bsquidwrd/beardbot:latest .
docker-compose up --build -d --remove-orphans
docker exec beardbot_streamlabs_1 python manage.py migrate
Clear-Host
docker-compose logs -f
