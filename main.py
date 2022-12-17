# main

from MoudleNFT import NFT_Handler
import Utills as Utl
import pandas as pd
import Globals as G


G.ETH_Price = Utl.get_ETH_price()
G.USD_rate = Utl.USD_rate()
handler = NFT_Handler()
NFTs = handler.get_all_NFTs_details()
headers = handler.get_headers()
NFTs_DF = pd.DataFrame(NFTs, columns=headers)
Profit_DF = Utl.calculate_profit_df(handler, G.USD_invested, G.ILS_invested)
NFTs_DF.to_csv('NFTS.csv')
Profit_DF.to_csv('Profits.csv')
print(NFTs_DF)
print(Profit_DF)
print(f"Total ETH: {handler.calculate_total_ETH()}  ETH Price: {G.ETH_Price}  USD Rate: {G.USD_rate}")


