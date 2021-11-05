import serial
import pprint
import requests
import json
import pprint as pp
from pymongo import MongoClient
from platform import python_version
import time

def getHeader():
    data = {'email': 'thorwulf@hotmail.com', 'password': 'd5pljrtr!'}
    r = requests.post('https://api.cityflow.live/users/login', data=json.dumps(data), verify=False)
    retVal = json.loads(r.text)
    f.write(retVal['token']+'\n')
    f.flush()
    token=retVal['token']
    headers = {'Content-Type':'application/json','Authorization': 'Bearer {}'.format(token)}
    return headers


def doImp(header):
    # GET /measurements/latest HTTP/1.1
    # Authorization: Bearer {BEARER_TOKEN}
    # Host: api.cityflow.live
    rmes2 = requests.get('https://api.cityflow.live/measurements/latest', headers=header, verify=False)
    data2 = json.loads(rmes2.text)
    #pp.pprint(data2)

    #type(data2['150'])
    # type(data2.items())
    #for line in data2['150']:
    #    pp.pprint(line)

    client = MongoClient("mongodb://3.145.0.163:27017/cityflow")
    dbn = client.get_database('cityflow')
    #db = client.test
    #print(dbn.list_collection_names())
    #col = dbn.observations
    #obs = dbn.observations.find()
    #for item in obs:
    #    pp.pprint(item)
    #print(dbn)

    for line in data2['150']:
        result = dbn.observations.insert_one(line)
        f.write(str(line)+'\n')
        f.flush()
        print(result.inserted_id)

if __name__ == "__main__":
    f=open("logfile.txt","a")
    now = "{:0f}".format(time.time())
    diff=10
    header=getHeader()
    while True:
        doImp(header)
        time.sleep(10)
