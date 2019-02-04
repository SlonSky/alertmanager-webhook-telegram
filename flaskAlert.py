import telegram
import logging

import os
from flask import Flask
from flask import request
from datetime import datetime

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv('secret_key')

CHAT_ID = os.getenv('chatID')
TOKEN = os.getenv('botToken')

logger.info('Connecting to chat: ' + str(CHAT_ID))
logger.info('Token is: ' + str(TOKEN))

bot = telegram.Bot(token=TOKEN)

@app.route('/alert', methods = ['POST'])
def postAlertmanager():

    logger.info('Got request')
    
    content = request.get_json()
    if not content:
        abort(400)

    alert_name = content['alerts'][0]['labels']['alertname']
    # just strip microseconds part
    d = content['alerts'][0]['startsAt'].split('.')[0]
    alert_time = str(datetime.strptime(d, '%Y-%m-%dT%H:%M:%S'))
    alert_high = content['alerts'][0]['labels']['severity'].upper()
    alert_inst = content['alerts'][0]['labels']['instance']
    # assume desciption may be empty

    message = '[{}] {} at {}\non {}\n'.format(
            alert_high, alert_name, alert_time, alert_inst)

    for annotation in content['alerts'][0]['annotations']:
        message += '{}: {}\n'.format(annotation, content['alerts'][0]['annotations'][annotation])
    bot.sendMessage(chat_id=CHAT_ID, text=message)
    
    logger.info('Send message: ' + message)

    return ''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9119)
