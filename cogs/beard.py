from twitchio.ext import commands


class Beard(commands.AutoCog):
    def __init__(self, bot):
        self.bot = bot

    def _prepare(self, bot):
        pass


    async def event_message(self, message):
        if 'Cheer' in message.content:
            self.bot.log.info(message.content)

    
    async def event_usernotice_subscription(self, notice):
        sub_points = 0
        sub_type = None
        if '#shave' in notice.tags.get('system-msg'):
            sub_type = '#shave'
        elif '#save' in notice.tags.get('system-msg'):
            sub_type = '#save'
        else:
            self.bot.log.info(f'{notice.user.name} did not specify #save or #shave')
            return

        if notice.sub_plan == 'Prime' or notice.sub_plan == 1000:
            sub_points = 5
        elif notice.sub_plan == 2000:
            sub_points = 10
        elif notice.sub_plan == 3000:
            sub_points = 30
        self.bot.log.info(f'{notice.user.name} has contibuted to {sub_type} for {sub_points} points')


def prepare(bot):
    bot.add_cog(Beard(bot))


def breakdown(bot):
    pass
