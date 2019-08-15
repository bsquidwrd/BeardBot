import os
import datetime
import logging
import traceback
import web.wsgi
from twitchio.ext import commands
from twitchio.ext.commands.errors import CommandNotFound


initial_extensions = (
    'cogs.admin',
    'cogs.basic',
    'cogs.beard',
    'cogs.tasks',
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(module)s %(name)s.%(funcName)s +%(lineno)s: %(levelname)-8s [%(process)d] %(message)s',
)


class Bot(commands.Bot):
    def __init__(self, irc_token, nick, client_id='test', initial_channels=[], api_token='test'):
        self.params = {
            'irc_token': irc_token,
            'client_id': client_id,
            'nick': nick,
            'prefix': '!',
            'initial_channels': initial_channels,
            'api_token': api_token,
        }
        super().__init__(**self.params)
        self.log = logging

        self.log.info(f"Initial channels: {self.initial_channels}")

        for extension in initial_extensions:
            try:
                self.load_module(extension)
            except Exception as e:
                print(f'Failed to load extension {extension}.')
                traceback.print_exc()


    async def event_ready(self):
        ready_string = f'Ready: {self.nick}'
        self.log.info(ready_string)
        self.log.info('-'*len(ready_string))
        print(ready_string)
        print('-'*len(ready_string))


    async def event_command_error(self, ctx, error):
        #self.log.info(error)
        pass


    async def event_message(self, message):
        if message.author.name.lower() != self.nick.lower():
            await self.handle_commands(message)


if __name__ == '__main__':
    nick = os.environ['BOT_NICK']
    irc_token = os.environ['BOT_TOKEN']
    client_id = os.getenv('BOT_CLIENTID', None)
    api_token = os.getenv('BOT_APITOKEN', None)

    initial_channels = os.getenv('INITIAL_CHANNELS', '').split(',')
    if initial_channels[0] == '' or initial_channels is None or len(initial_channels) > 1:
        raise Exception("Please make sure you are only specifiying 1 channel in the INITIAL_CHANNELS environment key")

    bot = Bot(irc_token=irc_token, client_id=client_id, nick=nick, initial_channels=initial_channels, api_token=api_token)
    bot.run()
