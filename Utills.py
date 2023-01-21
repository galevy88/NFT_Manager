# Utills functions

import numpy as np
import pandas as pd
import Globals as G
import requests
from opensea import OpenseaAPI
import ccxt
from forex_python.converter import CurrencyRates

api = OpenseaAPI()


def get_NFTs():
    url = G.URL
    headers = G.Headers

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        parsed_JSON = response.json()
        NFTs = parsed_JSON["nfts"]
    return NFTs

def get_name_by_contract_address(contract_address):
    return G.contract_name_dictonary[contract_address]

def get_url_by_name(name):
    return G.name_url_dictonary[name]

def get_Verbose():
    return G.Verbose

def get_floor_price(url):
    result = api.collection_stats(collection_slug=url)
    stats = result["stats"]
    floor_price = stats["floor_price"]
    return floor_price

def get_ETH_price():
    print("Getting ETH Current Price ...")
    exchange = ccxt.binance()
    ticker = exchange.fetch_ticker('ETH/USDT')
    ETH_price = ticker['last']
    return ETH_price

def USD_rate():
    print("Getting USD Current Rate ...")
    cr = CurrencyRates()
    ILS_rates = cr.get_rates('ILS')
    ILS_USD_rate = ILS_rates['USD']
    rate = 1 / ILS_USD_rate
    return rate

def calculate_profit_df(NFT_handler,Binance_handler, USD_invested, ILS_invested):
    USD_value_NFT, ILS_value_NFT = NFT_handler.calculate_total_value()
    USD_value_Binance, ILS_value_Binance = Binance_handler.calculate_total_value()

    USD_value = USD_value_NFT + USD_value_Binance
    ILS_value = ILS_value_NFT + ILS_value_Binance

    USD_row = [USD_invested, USD_value, USD_value - USD_invested]
    ILS_row = [ILS_invested, ILS_value, ILS_value - ILS_invested]
    columns = ["Invested", "Total", "Profit"]
    index = ["USD", "ILS"]
    df = pd.DataFrame([USD_row, ILS_row], columns=columns, index=index)
    return df


def combine_total_df(NFTs_DF, Binance_DF):
    df_nft = NFTs_DF[["Name", "ETH Floor Price", "USD Price"]]
    df_binance = Binance_DF[["coins", "total_eth", "total_usd"]]
    combine_df = pd.concat([df_nft, df_binance])
    return combine_df


    