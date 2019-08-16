import os
import asyncio
from twitchio.ext import commands
import web.wsgi
from bearddb.models import BeardLog
from django.db.models import Sum, Q


class Tasks(commands.AutoCog):
    def __init__(self, bot):
        self.bot = bot
        self._task = None


    def _prepare(self, bot):
        pass


    def _tasks__unload(self):
        self._task.cancel()

    
    async def event_ready(self):
        pass


    async def run_tasks(self):
        try:
            while True:
                await self.run_scheduled_tasks()
                await asyncio.sleep(60)
        except asyncio.CancelledError:
            pass

    
    async def run_scheduled_tasks(self):
        events = BeardLog.objects.filter(event_test=False, asks__lt=5).filter(Q(event_team__isnull=True)|Q(event_team__exact=''))
        events_data = events.values("event_user").annotate(n=Sum("event_points"))
        channel = self.bot.get_channel(os.environ['INITIAL_CHANNELS'])
        if channel is None:
            return
        if events_data.count() == 0:
            return

        message = 'Points awaiting claim: '
        user_messages = []
        for e in events_data:
            user_messages.append(f"{e['event_user']}: {e['n']}")
            for i in events.filter(event_user=e['event_user']):
                i.asks += 1
                i.save()
        message += ", ".join(user_messages)

        message += ". Please type !claim #save or !claim #shave"
        await channel.send(message)


def prepare(bot):
    cog = Tasks(bot)
    cog._task = bot.loop.create_task(cog.run_tasks())
    bot.add_cog(cog)


def breakdown(bot):
    pass
