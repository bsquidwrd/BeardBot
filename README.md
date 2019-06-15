# BeardBot

### Requirements
* Linux (any kernel should be fine)
* [Docker](https://docker.com/)
* [Docker Compose](https://docs.docker.com/compose/)


### Install Docker
Go to the official [Docker Install documentationn](https://docs.docker.com/install/#server) and follow the steps for your operating system
Ubuntu Xenial 16.04 (LTS) x_86_64/amd64 example:
```bash
sudo apt-get remove docker docker-engine docker.io containerd runc
sudo apt-get update
sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
```


### Install Docker Compose
According to the official [Docker Compose documentation](https://docs.docker.com/compose/install/), install Docker as follows:
```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
docker-compose --version
```


### Setup
1. Copy the `docker-compose.yml` to the machine/server you will be running the bot from
1. Make a file named `.env` in the same directory as `docker-compose.yml` and copy the contents of `example.env` into the file
1. Modify the `.env` contents accordingly (Only modify what has `CHANGEME` as the value)


### Running
Run the following to start everything, including the database.
```bash
docker-compose up --build -d --remove-orphans
docker exec beardbot_bot_1 python manage.py migrate
docker-compose logs -f
```
* **NOTE:** If you do not run the `docker exec beardbot_bot_1 python manage.py migrate` command, everything will fail as there will be no tables in the MySQL Database


### Stopping
Run the following to stop everything, including the database.
```bash
docker-compose down --remove-orphans
```


### Re-setup
There are multiple ways to "Reset" the database
* Delete everything in the database (make it a fresh slate for next startup): `docker volume rm beardbot_db`
* Delete just the records associated in the `bearddb_beardlog` table (assuming the containers are still running): `docker exec beardbot_bot_1 python reset_database.py`


### Modifications
If you have made modifications to the `docker-compose.yml` file after starting the containers, simply run the following to update the containers (they will restart only if they were affected by the changes made)
```bash
docker-compose up --build -d --remove-orphans
```


### Database Notes
* The database generates a one-time root password, if you need it look into configuring the `.env` file based off of the MySQL Docker documentation here: https://hub.docker.com/_/mysql 
* By default, it is unaccessible from anything other than a container within the Compose file
* If you'd like to make it accessible via the outside, change the `db` section of the `docker-compose.yml` file:
```yml
  db:
    image: mysql:5.7.26
    ports:
      - "3306:3306"
    restart: unless-stopped
    env_file:
      - .env
    volumes:
      - db:/var/lib/mysql
    networks:
      backend:
        aliases:
          - beardbot_db
```
* If you'd rather manage it via **phpmyadmin** add the following in the `docker-compose.yml` file underneath the `db` section, but before the `networks` section
  * **THIS IS NOT RECOMMENDED, UNLESS YOU HAVE CHANGED THE PASSWORD FOR THE DATABASE IN THE ENVIRONMENT FILE AS IT'S NOT A SECURE PASSWORD**
```yml
  phpmyadmin:
    image: phpmyadmin/phpmyadmin:4.8
    container_name: phpmyadmin
    ports:
      - "8080:80"
    restart: unless-stopped
    environment:
      - PMA_HOST=beardbot_db
      - PMA_PORT=3306
    volumes:
      - /sessions
    networks:
      - backend
      - default
    depends_on:
      - db
```
