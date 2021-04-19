import requests
import json
import datetime
import sys

TICKER_URL = "https://www.binance.com/api/v3/ticker/bookTicker"
START_COIN = sys.argv[1]    # Стартовая валюта
START_SCORE = 4000
MAX_PART_OF_CHAIN = 3       # Колличество сделок
PROFIT_COEF = 1.01          # Минимальный подходящий коэфициент

with open('parameters/symbols.json') as file:
    SYMBOLS_DICT = json.loads(file.read())
    START_CHAIN_LIST = [symbol for symbol, coins in SYMBOLS_DICT.items() if coins['quoteAsset'] == START_COIN]


def get_next_coin(symbol, previous_coin):
    return SYMBOLS_DICT[symbol]['baseAsset'] if previous_coin == SYMBOLS_DICT[symbol]['quoteAsset'] else SYMBOLS_DICT[symbol]['quoteAsset']


def get_available_symbols(list_used_symbols, coin):
    return [symbol for symbol, coins in SYMBOLS_DICT.items()
            if (coin in [coins['quoteAsset'], coins['baseAsset']]) and
            (symbol not in list_used_symbols)]


def get_next_score(symbol, previous_score, coin):
    for item in all_prices:
        if item['symbol'] == symbol:
            ask_price = float(item['askPrice'])
            bid_price = float(item['bidPrice'])
            if ask_price == 0 or bid_price == 0:
                return None
            else:
                if SYMBOLS_DICT[symbol]['quoteAsset'] == coin:
                    return previous_score / ask_price
                else:
                    return previous_score * bid_price



def chain_finder(list_used_symbols, coin, current_score):

    if len(list_used_symbols) > MAX_PART_OF_CHAIN:
        return None

    next_coin = get_next_coin(list_used_symbols[-1], coin)
    next_score = get_next_score(list_used_symbols[-1], current_score, coin)

    if next_score is None:
        return None

    if next_coin == START_COIN:
        coef = next_score / START_SCORE
        if coef >= PROFIT_COEF:
            result_chain = '->'.join(list_used_symbols)
            with open('logs/result.txt', 'a') as file:
                file.write(f'{datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}   {result_chain}  Coef - {coef}\n')
            if result_chain not in top_deals_by_symbol:
                top_deals_by_symbol[result_chain] = coef
            elif result_chain in top_deals_by_symbol:
                if float(top_deals_by_symbol[result_chain]) < coef:
                    top_deals_by_symbol[result_chain] = coef
        return None


    if len(list_used_symbols) >= MAX_PART_OF_CHAIN:
        return None
    else:
        for next_symbol in get_available_symbols(list_used_symbols, next_coin):
            list_used_symbols.append(next_symbol)
            if chain_finder(list_used_symbols, next_coin, next_score) is None:
                list_used_symbols.pop()


top_deals_by_symbol = dict()
while(True):
    start_time = datetime.datetime.now()
    try:
        all_prices = json.loads(requests.get(TICKER_URL).text)
    except Exception as e:
        print(e)

    for item in all_prices:
        if item['symbol'] in START_CHAIN_LIST:
            chain_finder([item['symbol']], START_COIN, START_SCORE)

    with open('logs/top_deals_by_symbol.txt', 'w') as file:
        for chain, coef in top_deals_by_symbol.items():
            file.write(f"{chain} - {coef}\n")
    end_time = datetime.datetime.now()
    print(f"Transaction time = {end_time - start_time}s")
