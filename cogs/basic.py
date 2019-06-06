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

    # @commands.command(name='test')
    # async def test_command(self, ctx):
    #     if ctx.channel.name == self.bot.nick or checks.is_owner(ctx) or checks.is_mod(ctx):
    #         self.bot.log.info(ctx.message.author.tags)

    # async def event_usernotice_subscription(self, notice):
    #     self.bot.log.info(f'channel: {notice.channel}')
    #     self.bot.log.info(f'user: {notice.user}')
    #     self.bot.log.info(f'cumulative_months: {notice.cumulative_months}')
    #     self.bot.log.info(f'share_streak: {notice.share_streak}')
    #     self.bot.log.info(f'streak_months: {notice.streak_months}')
    #     self.bot.log.info(f'sub_plan: {notice.sub_plan}')
    #     self.bot.log.info(f'sub_plan_name: {notice.sub_plan_name}')
    #     self.bot.log.info(json.dumps(notice.tags, indent=4, sort_keys=True))


def prepare(bot):
    # Module is being loaded
    # Prepare anything you need
    # then add the cog
    bot.add_cog(Basic(bot))


def breakdown(bot):
    # Incase you wanna do something
    # when the Module is getting unloaded?
    pass
