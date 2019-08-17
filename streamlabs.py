import os
import datetime
import json
import logging
import traceback
import socketio
import sys

import web.wsgi
from bearddb.models import BeardLog
from cogs.utils.team import get_team


sio = socketio.Client()


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(module)s %(name)s.%(funcName)s +%(lineno)s: %(levelname)-8s [%(process)d] %(message)s',
)


def log_event(event_id, event_user, event_type, event_points, event_team, event_message, event_test=False):
    logging.info(f'{event_user} put {event_points} points towards {event_team} with a {event_type}')
    try:
        existing_logs = BeardLog.objects.filter(event_id=event_id)
        if existing_logs.count() >= 1:
            logging.info(f'{event_id} already logged for user {event_user}. Skipping')
            return
        else:
            BeardLog.objects.create(event_id=event_id, event_user=event_user, event_type=event_type, event_points=event_points, event_team=event_team, event_message=event_message, event_test=event_test)
    except:
        pass


@sio.event
def connect():
    logging.info('Connected to Server Socket')
    print("Connected to Server Socket.")


@sio.on('event')
def event_handler(raw_data):
    event_type = raw_data['type']
    if event_type not in ['donation', 'subscription', 'resub', 'bits']:
        return
    if event_type == 'subscription':
        logging.info(raw_data)

    try:
        event_for = raw_data.get('for', None)
        data = raw_data['message'][0]
        try:
            event_id = raw_data['event_id']
        except:
            event_id = data['event_id']
        event_test = data.get('isTest', False)
        message = data.get('message', '')
        team = get_team(message)
        name = ''
        points = 0

        try:
            team = team.lower()
        except:
            pass

        if event_type == 'donation':
            name = data['from']
            amount = data['amount']
            points = int(float(amount))

        elif event_for == 'twitch_account':
            name = data['name']

            if event_type == 'subscription' or event_type == 'resub':
                gifted = False
                sub_plan = ''

                try:
                    if data['sub_type'] == 'subgift':
                        gifted = True
                        name = data['gifter']
                        sub_plan = data['subPlan']
                        message = f"Gifted sub to {data['name']}"
                    else:
                        sub_plan = data['sub_plan']
                except:
                    sub_plan = data['sub_plan']

                if sub_plan == "Prime" or sub_plan == "1000":
                    points = 5
                elif sub_plan == '2000':
                    points = 10
                elif sub_plan == '3000':
                    points = 30

            elif event_type == 'bits':
                amount = int(data['amount'])
                points = int(amount / 100)

            else:
                return
        
        log_event(event_id, name, event_type, points, team, message, event_test)

    except Exception as e:
        traceback.print_exc()



def start_server(server_url):
    sio.connect(server_url)
    sio.wait()


if __name__ == '__main__':
    token = os.environ['STREAMLABS_TOKEN']
    server_url = f'https://sockets.streamlabs.com?token={token}'
    start_server(server_url)
