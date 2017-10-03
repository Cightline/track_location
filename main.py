import json
import datetime

import dataset
from flask import Flask, request


app = Flask(__name__)

base_path = '/home/admin/.config/track_location'

with open('%s/config.json' % (base_path)) as cfg:
    config = json.load(cfg)

db    = dataset.connect(config['db_uri'])
table = db['locations']

@app.route('/store_location', methods=['POST', 'GET'])
def store_location():

    if not request.is_json:
        return json.dumps({}), 403


    j = request.json

    now = datetime.datetime.utcnow()

    table.insert(dict(_type=j['_type'], 
                      tid=j['tid'], 
                      acc=j['acc'], 
                      batt=j['batt'], 
                      conn=j['conn'],
                      lat=j['lat'],
                      lon=j['lon'],
                      date=now))



    #return json.dumps([{'type_':'cmd', 'action':'reportLocation'}]) , 200


    # {'_type': 'location', 'tid': 'ra', 'acc': 23, 'batt': 92, 'conn': 'm', 'lat': 33.0040529, 'lon': -96.9905623, 't': 'u', 'tst': 1507065015, '_cp': True}

    return json.dumps({}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
