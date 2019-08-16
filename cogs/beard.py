from twitchio.ext import commands
import web.wsgi
from bearddb.models import BeardLog
from django.db.models import Sum, Q
from cogs.utils.team import get_team


class Beard(commands.AutoCog):
    def __init__(self, bot):
        self.bot = bot

    def _prepare(self, bot):
        pass


    def get_save_count(self):
        count = BeardLog.objects.filter(event_team="#save", event_test=False).aggregate(Sum("event_points"))['event_points__sum']
        if count is None:
            count = 0
        return count


    def get_shave_count(self):
        count = BeardLog.objects.filter(event_team="#shave", event_test=False).aggregate(Sum("event_points"))['event_points__sum']
        if count is None:
            count = 0
        return count


    @commands.command(name='beard')
    async def beard_command(self, ctx):
        save_count = self.get_save_count()
        shave_count = self.get_shave_count()
        await ctx.send(f"Team #save: {save_count} | Team #shave: {shave_count}")


    @commands.command(name='beardinfo')
    async def beard_info_command(self, ctx):
        message_to_send = "Every $1 from Donations, Bits, Subs, Resubs, and Gifted Subs will count as one point for your preferred team (with an added 5 point bonus for T3 subs). Gifted subs are at choice of gifter. Please clarify with #save or #shave to have your vote count or if you forget to clarify the point will go to the losing team automatically."
        await ctx.send(message_to_send)


    @commands.command(name='save')
    async def save_command(self, ctx):
        save_count = self.get_save_count()
        await ctx.send(f"The Current Save Count is: {save_count}")


    @commands.command(name='shave')
    async def shave_command(self, ctx):
        shave_count = self.get_shave_count()
        await ctx.send(f"The Current Shave Count is: {shave_count}")


    @commands.command(name='claim') # Maybe do spend instead?
    async def claim_command(self, ctx, *, raw_team: str = None):
        events = BeardLog.objects.filter(event_user=ctx.author.name, event_test=False).filter(Q(event_team__isnull=True)|Q(event_team__exact=''))
        points = events.aggregate(Sum("event_points"))['event_points__sum']
        if events.count() == 0:
            await ctx.send(f"{ctx.author.name} It doesn't look like you have any pending points to claim")
        else:
            team = get_team(raw_team)
            if team:
                events.update(event_team=team)
                self.bot.log.info(f"{ctx.author.name} claimed {points} to team {team}")
                await ctx.send(f"{ctx.author.name} I have allocated {points} points to team {team}")
            else:
                await ctx.send(f"{ctx.author.name} I didn't quite understand the team you typed. Please try again and make sure to type either #save or #shave")


def prepare(bot):
    bot.add_cog(Beard(bot))


def breakdown(bot):
    pass
