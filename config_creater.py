import requests
import json

DEFAULT_URL = 'https://api.binance.com/api/v3/exchangeInfo'

try:
    response = json.loads(requests.get(DEFAULT_URL).text)
except Exception as e:
    print(f'Error - {e}')
else:
    result_dict = {}
    for item in response['symbols']:
        if item['symbol'] not in result_dict:
            result_dict[item['symbol']] = {
                'master': '',
                'slave': '',
            }
        result_dict[item['symbol']]['master'] = item['quoteAsset']
        result_dict[item['symbol']]['slave'] = item['baseAsset']

    with open('parameters/symbols.json', 'w') as file:
        file.write(json.dumps(result_dict))

