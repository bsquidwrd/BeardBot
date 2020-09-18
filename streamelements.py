import os
from datetime import datetime
import json
import logging
import traceback
import socketio
import sys

import web.wsgi
from bearddb.models import BeardLog
from cogs.utils.team import get_team
from django.db.models import Sum

sio = socketio.Client()


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(module)s %(name)s.%(funcName)s +%(lineno)s: %(levelname)-8s [%(process)d] %(message)s',
)

def get_save_count():
    count = BeardLog.objects.filter(event_team="#save", event_test=False).aggregate(Sum("event_points"))['event_points__sum']
    if count is None:
        count = 0
    return count


def get_shave_count():
    count = BeardLog.objects.filter(event_team="#shave", event_test=False).aggregate(Sum("event_points"))['event_points__sum']
    if count is None:
        count = 0
    return count


def log_event(event_id, event_user, event_type, event_points, event_team, event_message, event_test=False):
    try:
        existing_logs = BeardLog.objects.filter(event_id=event_id)
        if existing_logs.count() >= 1:
            logging.info(f'{event_id} already logged for user {event_user}. Skipping')
            return
        else:
            BeardLog.objects.create(event_id=event_id, event_user=event_user, event_type=event_type, event_points=event_points, event_team=event_team, event_message=event_message, event_test=event_test)
            save_count = get_save_count()
            shave_count = get_shave_count()
            logging.info(f'{event_user} put {event_points} points towards {event_team} with a {event_type} . TOTALS: #shave {shave_count} | #save {save_count}')
    except:
        pass


@sio.on('connect')
def event_connect():
    token = os.environ['STREAMELEMENTS_TOKEN']
    sio.emit('authenticate', { 'method': 'jwt', 'token': token })
    logging.info('Connected to Server Socket')
    print("Connected to Server Socket.")


# @sio.on('message')
# def message_hander(msg):
#     logging.info(msg)


@sio.on('event')
def event_handler(raw_data):
    if 'type' not in raw_data:
        logging.info('Type not found')
        return
    listener_type = raw_data['type'].lower()

    if listener_type not in ['subscriber', 'tip', 'cheer']:
        logging.info('Type not subscriber, tip or cheer')
        return
    
    try:
        data = raw_data['data']
        event_type = listener_type
        event_id = raw_data['_id']
        event_test = raw_data.get('event', {}).get('isTest', False)
        message = data.get('message', '')
        team = get_team(message)
        name = data['username']
        points = 0

        try:
            team = team.lower()
        except:
            pass

        if event_type == "subscriber":
            sub_multiplier = 0
            amount = 0

            if data.get('gifted', False) == True:
                name = data['sender']
            elif data.get('bulkGifted', False) == True:
                amount = int(data.get('amount', '1'))
            elif data.get('subExtension', False) == True:
                amount = 1
            else:
                amount = 1

            if data['tier'] == "1000" or data['tier'] == 'prime':
                sub_multiplier = 5
            elif data['tier'] == "2000":
                sub_multiplier = 10
            elif data['tier'] == "3000":
                sub_multiplier = 30

            points = sub_multiplier * amount

        if event_type == "cheer":
            amount = int(data.get('amount', '1'))
            points = int(amount / 100)

        if event_type == "tip":
            amount = int(data.get('amount', '1'))
            points = amount

        log_event(event_id, name, event_type, points, team, message, event_test)

    except Exception as e:
        logging.info(json.dumps(raw_data))
        logging.error(traceback.print_exc())



def start_server(server_url):
    sio.connect(server_url, transports=['websocket'])
    sio.wait()


if __name__ == '__main__':
    server_url = f'https://realtime.streamelements.com'
    start_server(server_url)
