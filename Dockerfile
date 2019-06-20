FROM python:3.7.3-stretch


# Copy your application code to the container (make sure you create a .dockerignore file if any large files or directories should be excluded)
RUN mkdir /code/
WORKDIR /code/

# Copy in your requirements file
ADD requirements.txt /requirements.txt
RUN python -m pip install -U pip
RUN pip install --no-cache-dir -r /requirements.txt

# Add code and volumes
ADD . /code/

# Add any custom, static environment variables needed by Django or your settings file here:
ENV 'BOT_TOKEN'='oauth:CHANGEME'
ENV 'BOT_NICK'='CHANGEME'
ENV 'OWNER_ID'='22812120'
ENV 'INITIAL_CHANNELS'='CHANGEME'
ENV 'STREAMLABS_TOKEN'='CHANGEME'
ENV 'MYSQL_HOST'='CHANGEME'
ENV 'MYSQL_PORT'='CHANGEME'
ENV 'MYSQL_DATABASE'='CHANGEME'
ENV 'MYSQL_USER'='CHANGEME'
ENV 'MYSQL_PASSWORD'='CHANGEME'
ENV 'MYSQL_RANDOM_ROOT_PASSWORD'='CHANGEME'

# Start Bot
CMD ["python", "/code/bot.py"]
