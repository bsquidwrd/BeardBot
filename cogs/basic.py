from twitchio.ext import commands
from twitchio import dataclasses
from cogs.utils import checks


class Basic(commands.AutoCog):
    def __init__(self, bot):
        self.bot = bot

    # def _basic__unload(self):
    #     pass

    def _prepare(self, bot):
        # I don't know why this is here
        # but it's required to have a cog
        # so keep it as a pass
        pass

    @commands.command(name='test')
    async def test_command(self, ctx):
        if ctx.channel.name == self.bot.nick or checks.is_owner(ctx) or checks.is_mod(ctx):
            self.bot.log.info(ctx.message.author.tags)


def prepare(bot):
    # Module is being loaded
    # Prepare anything you need
    # then add the cog
    bot.add_cog(Basic(bot))


def breakdown(bot):
    # Incase you wanna do something
    # when the Module is getting unloaded?
    pass
