#! python
# Cluster IP Address and Credentials

import time,datetime
import base64
import pprint
import asyncio
from aiohttp import ClientSession
import requests
import json
import sys
import random
import argparse
import os


pp = pprint.PrettyPrinter(indent=4)
d = (datetime.datetime.utcnow())
timestamp_from=(d.strftime('%a %b %d 00:00:00 UTC %Y'))
timestamp_to=(d.strftime('%a %b %d 24:00:00 UTC %Y'))


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

with open(os.path.join(__location__, '.creds')) as f:
    creds = json.load(f)


parser = argparse.ArgumentParser()
parser.add_argument('-c', '--cluster', choices=creds, required='True', help='Choose a cluster in .creds')
args = parser.parse_args()

creds=creds[args.cluster]

NODE_IP_LIST = creds['servers']
USERNAME = creds['username']
PASSWORD = creds['password']

# ignore certificate verification messages
requests.packages.urllib3.disable_warnings()

# Generic Rubrik API Functions
def basic_auth_header():
    """Takes a username and password and returns a value suitable for
    using as value of an Authorization header to do basic auth.
    """
    credentials = '{}:{}'.format(USERNAME, PASSWORD)
    # Encode the Username:Password as base64
    authorization = base64.b64encode(credentials.encode())
    # Convert to String for API Call
    authorization = authorization.decode()
    return authorization

def rubrik_get(api_version, api_endpoint):
    """ Connect to a Rubrik Cluster and perform a syncronous GET operation """
    AUTHORIZATION_HEADER = {'Content-Type': 'application/json',
                            'Accept': 'application/json',
                            'Authorization': 'Basic ' + basic_auth_header()
                            }
    request_url = "https://{}/api/{}{}".format(random.choice(NODE_IP_LIST), api_version, api_endpoint)
    try:
        api_request = requests.get(request_url, verify=False, headers=AUTHORIZATION_HEADER)
        # Raise an error if they request was not successful
        api_request.raise_for_status()
    except requests.exceptions.RequestException as error_message:
        print(error_message)
        sys.exit(1)
    response_body = api_request.json()
    return response_body

async def rubrik_get_async(url):
    """ Connect to a Rubrik Cluster and perform an async GET operation """
    series_id = url.split('/event_series/', 1)[-1]
    node_ip = url.strip('https://').split('/api', 1)[0]

    AUTHORIZATION_HEADER = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Basic ' + basic_auth_header()
    }

    async with ClientSession(headers=AUTHORIZATION_HEADER) as session:
        async with session.get(url,headers=AUTHORIZATION_HEADER,verify_ssl=False) as response:
            response_body = await response.read()
            try:
                response_body = json.loads(response_body)
                EVENT_DATA.append([{'series_id':series_id,'rubrik_node':node_ip,'series_data':response_body['data']}])
            except:
                print(response.message)
                return

start = time.time()
# Here we just run the initial call to get event IDs. We set the timeframe for today and query only for failures.
print("Running initial query for IDs")
EVENTS = rubrik_get("internal","/event?status=Failure&limit=9999&show_only_latest=true&before_date={}&after_date={}".format(timestamp_to,timestamp_from))
mid = time.time()
elapsed_mid = time.time()-start

counter_sync=1

# METHOD 1
# Here we run syncronous requests based on the event list returned above
print("Running {} sub requests syncronously".format(len(EVENTS['data'])))
for event in EVENTS['data']:
    counter_sync += 1
    event_series = rubrik_get("internal","/event_series/{}".format(event['eventSeriesId']))['data']

elapsed_sync = time.time()-start
tasks = []
EVENT_DATA = []

# METHOD 2
# Here we assemble our request loop to run async, randomizing the node we use.
loop = asyncio.get_event_loop()
print("Running {} sub requests asyncronously".format(len(EVENTS['data'])))
for event in EVENTS['data']:
    api_endpoint = "/event_series/{}".format(event['eventSeriesId'])
    node_ip = random.choice(NODE_IP_LIST)
    task = asyncio.ensure_future(rubrik_get_async("https://{}/api/{}{}".format(node_ip, 'internal', api_endpoint)))
    tasks.append(task)

# Here we run the async tasks 
loop.run_until_complete(asyncio.wait(tasks))
end = time.time()
elapsed_async = end-start-elapsed_sync+elapsed_mid

print("Data from : {} - {}".format(timestamp_from,timestamp_to))
print("Event series reported : {}".format(len(EVENT_DATA)))
print("Sync : {}\nAsync : {}".format(elapsed_sync,elapsed_async))