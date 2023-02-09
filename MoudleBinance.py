# NFT Classes


import numpy as np
import pandas as pd
import Globals as G
from binance.client import Client

binance = Client(G.Binance_API_Key, G.Binance_API_Secret)

class Binance_Handler:
    def __init__(self):
        self.df = None
        self.eth_value = None
        self.usd_value = None
        
    def get_price(self, given_symbol, prices_list):
        price = next(filter(lambda x: x['symbol'] == given_symbol, prices_list), None)
        if price:
            return price['price']
        else:
            return None


    def create_binance_df(self, coins, coins_amount, coin_prices, final_amount_eth, final_amount_usd):
        data = {'coins': coins, 'amount': coins_amount, 'rate_usd': coin_prices, 'total_eth': final_amount_eth, 'total_usd': final_amount_usd}
        df = pd.DataFrame(data)
        df.loc['sum'] = df.sum()
        df.loc['sum', 'coins'] = "TOTAL"
        df.loc['sum', df.columns[1:3]] = "---"
        return df


    def get_binance_assets(self):
        print("Getting Binance Assets ...")
        account = binance.get_account()
        balances = account['balances']
        
        coins = [asset['asset'] for asset in balances if float(asset['free']) > 5]
        
        coins_amount = [float(asset['free']) for asset in balances if float(asset['free']) > 5]
        
        tickers = [coin + "USDT" for coin in coins]
        print(tickers)
        coin_prices = []
        all_tickers = binance.get_all_tickers()
        for ticker in tickers:
            price = self.get_price(ticker, all_tickers)
            coin_prices.append(float(price))

        final_amount_usd = np.round([amount * float(price) for amount, price in zip(coins_amount, coin_prices)], 3)
        final_amount_eth = np.round([amount/G.ETH_Price for amount in final_amount_usd], 3)
        df = self.create_binance_df(coins, coins_amount, coin_prices, final_amount_eth, final_amount_usd)

        self.df = df
        self.usd_value = df.at['sum', 'total_usd']
        self.eth_value = df.loc['sum', 'total_eth']
        return df
    
    def calculate_total_value(self):
        sum_USD = self.usd_value
        sum_ILS = self.usd_value * G.USD_rate
        return sum_USD, sum_ILS
    
    def get_df(self):
        return self.df

    def get_eth(self):
        return self.eth_value

    def get_usd(self):
        return self.usd_value
        




        
    