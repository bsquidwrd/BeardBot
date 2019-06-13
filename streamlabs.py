import os
import datetime
import logging
import traceback
import re
import socketio
import web.wsgi
from bearddb.models import BeardLog


sio = socketio.Client()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(module)s %(name)s.%(funcName)s +%(lineno)s: %(levelname)-8s [%(process)d] %(message)s',
                    )


def get_team(message):
    regex = r"#(save|shave)"
    matches = re.finditer(regex, message, re.MULTILINE | re.IGNORECASE)

    for matchNum, match in enumerate(matches, start=1):
        return match.group()


def log_event(event_id, event_user, event_type, event_points, event_team, event_message, event_test=False):
    logging.info(f'{event_user} put {event_points} points towards {event_team} with a {event_type}')
    try:
        BeardLog.objects.create(event_id=event_id, event_user=event_user, event_type=event_type, event_points=event_points, event_team=event_team, event_message=event_message)
    except:
        pass


@sio.event
def connect():
    logging.info('Connected to Server Socket')


@sio.on('event')
def event_handler(raw_data):
    event_type = raw_data['type']
    if event_type not in ['donation', 'subscription', 'resub', 'bits']:
        return

    try:
        event_id = raw_data['event_id']
        event_for = raw_data['for']
        data = raw_data['message'][0]
        message = data['message']
        event_test = data['isTest']
        # raw_team = get_team(message)
        import random
        raw_team = random.choice(['#save','#shave'])

        # if not event_test:
        #     return

        if raw_team:
            name = ''
            points = 0
            team = raw_team.lower()

            if event_for == 'streamlabs' and event_type == 'donation':
                name = data['from']
                amount = data['amount']
                points = int(amount)
                log_event(event_id, name, event_type, points, team, message)

            elif event_for == 'twitch_account':
                name = data['name']
                
                if event_type == 'subscription' or event_type == 'resub':
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
                    pass

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
