import requests
import time
import json
from datetime import datetime
URL = 'https://backend-arbitrum.gains.trade/trading-variables'
FILE_NAME = 'interests.json'

desired_pairs = ['BTCUSD', 'ETHUSD', 'NVDAUSD']
previous_interests = {}

while True:
    try:
        t = time.time()
        response = requests.get(URL)
        data = response.json()

        current_interests = {}
        for pair, interest in zip(data['pairs'], data['openInterests']):
            pair_name = pair['from'] + pair['to']
            if pair_name in desired_pairs:
                current_interests[pair_name] = interest['short']

        for pair, interest in current_interests.items():
            if pair in previous_interests:
                if previous_interests[pair] != interest:
                    print(f'[{datetime.now()}] Interest for {pair} has changed. New interest: {interest}')
                else:
                    print(f'[{datetime.now()}] Interest for {pair} has not changed. Current interest: {interest}')
                
        previous_interests = current_interests

        with open(FILE_NAME, 'w') as file:
            json.dump(current_interests, file)

        print(time.time() - t)
        time.sleep(60)
    except Exception as e:
        print(f'An error occurred: {e}')
        break
