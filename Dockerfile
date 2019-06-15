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
ENV 'BOT_TOKEN'='oauth:placeholder'
ENV 'BOT_NICK'='placeholder'
ENV 'OWNER_ID'='22812120'
ENV 'INITIAL_CHANNELS'='placeholder'
ENV 'STREAMLABS_TOKEN'='placeholder'
ENV 'DATABASE_NAME'='placeholder'
ENV 'DATABASE_USER'='placeholder'
ENV 'DATABASE_PASSWORD'='placeholder'
ENV 'DATABASE_HOST'='placeholder'
ENV 'DATABASE_PORT'='placeholder'
ENV 'LOG_DIR'='/var/log/'

# Start Bot
CMD ["python", "/code/bot.py"]
