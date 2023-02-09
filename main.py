# main

from MoudleNFT import NFT_Handler
from MoudleBinance import Binance_Handler
import Utills as Utl
import pandas as pd
import Globals as G
import os
import datetime

now = datetime.datetime.now()
directory_name = now.strftime('Data/%Y-%m-%d %H-%M-%S')
os.mkdir(directory_name)

G.ETH_Price = Utl.get_ETH_price()
G.USD_rate = Utl.USD_rate()

Binance_handler = Binance_Handler()
Binance_DF = Binance_handler.get_binance_assets()

NFT_handler = NFT_Handler()
NFTs = NFT_handler.get_all_NFTs_details()
headers = NFT_handler.get_headers()
NFTs_DF = pd.DataFrame(NFTs, columns=headers)

Profit_DF = Utl.calculate_profit_df(NFT_handler, Binance_handler, G.USD_invested, G.ILS_invested)
Total_DF = Utl.combine_total_df(NFTs_DF, Binance_DF)


NFTs_DF.to_csv(f'{directory_name}/NFTS.csv')
Binance_DF.to_csv(f'{directory_name}/Binance.csv')
Total_DF.to_csv(f'{directory_name}/Total_DF.csv')
Profit_DF.to_csv(f'{directory_name}/Profits.csv')


print(Profit_DF)
ETH_Amount = NFT_handler.calculate_total_ETH() + Binance_handler.get_eth()
print(f"Total ETH: {ETH_Amount}  ETH Price: {G.ETH_Price}  USD Rate: {G.USD_rate}")




