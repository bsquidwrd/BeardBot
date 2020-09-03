from twitchio.ext import commands
from twitchio import dataclasses
from cogs.utils import checks
import json


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

    @commands.command(name='ping')
    @commands.check(checks.is_mod)
    async def ping_command(self, ctx):
        await ctx.send(f"Pong {ctx.author.name}")

    @commands.command(name='pong')
    @commands.check(checks.is_mod)
    async def pong_command(self, ctx):
        await ctx.send(f"Ping {ctx.author.name}")

def prepare(bot):
    # Module is being loaded
    # Prepare anything you need
    # then add the cog
    bot.add_cog(Basic(bot))


def breakdown(bot):
    # Incase you wanna do something
    # when the Module is getting unloaded?
    pass
