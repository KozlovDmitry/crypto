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
        if item['status'] != 'TRADING':
            continue
        if item['symbol'] not in result_dict:
            result_dict[item['symbol']] = {
                'quoteAsset': '',
                'baseAsset': '',
            }
        result_dict[item['symbol']]['quoteAsset'] = item['quoteAsset']
        result_dict[item['symbol']]['baseAsset'] = item['baseAsset']

    with open('parameters/symbols.json', 'w') as file:
        file.write(json.dumps(result_dict))

