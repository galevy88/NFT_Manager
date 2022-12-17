# NFT Classes

import Utills as Utl 
import Globals as G


class NFT:
    def __init__(self, name, token_id, contract_address, image, Hidden):
        self.name = name
        self.token_id = token_id
        self.contract_address = contract_address
        self.image = image
        self.url = ""
        self.floor_price = 0
        self.USD_price = 0
        self.ILS_price = 0
        self.Hidden = Hidden
        self.manage_Hidden(Hidden)
        self.manage_Methane()
        print(self.name)
    
    def manage_Hidden(self, Hidden):
        if not Hidden and self.name != "Methane":
            self.url = Utl.get_url_by_name(self.name)
            self.floor_price = Utl.get_floor_price(self.url)
            self.USD_price = self.floor_price * G.ETH_Price
            self.ILS_price = self.USD_price * G.USD_rate

    def manage_Methane(self):
        if self.name == "Methane":
            self.floor_price = G.Methane_Floor_Price * G.Methane_Amount / G.Division_Factor
            self.USD_price = self.floor_price * G.ETH_Price
            self.ILS_price = self.USD_price * G.USD_rate

    def print_details(self):
        print(f"name     : {self.name}")
        print(f"url:     : {self.url}")
        print(f"ID       : {self.token_id}")
        print(f"contract : {self.contract_address}")
        print(f"Image    : {self.image}")
        print(f"Hidden   : {self.Hidden}")


    def get_ETH_value(self):
        return self.floor_price

    def get_USD_value(self):
        return self.USD_price

    def get_ILS_value(self):
        return self.ILS_price

    def get_NFT_details(self):
        details = [self.name, self.token_id, self.contract_address, self.image, self.url, self.floor_price, self.Hidden, self.USD_price, self.ILS_price]
        return details
    

class NFT_Handler:

    def __init__(self):
        self.JSON_NFTs = Utl.get_NFTs()
        self.Verbose = Utl.get_Verbose()
        self.NFTs_instances = self.generate_NFTs()

    def fetch_nft(self, nft):
        Hidden = True
        metadata = nft["metadata"]
        contract_address = nft["contract_address"]
        token_id = nft["token_id"]
        image = metadata["image"]
        name = Utl.get_name_by_contract_address(contract_address)
        if contract_address in self.Verbose: Hidden = False
        return Hidden, contract_address, token_id, image, name

    def generate_NFTs(self):
        NFT_instances = []
        for nft in self.JSON_NFTs:
            Hidden, contract_address, token_id, image, name = self.fetch_nft(nft)
            NFT_instances.append(NFT(name=name, token_id=token_id, contract_address=contract_address, image=image, Hidden=Hidden))
        NFT_instances.append(NFT(name="Methane", token_id="", contract_address="", image="", Hidden=False))
        return NFT_instances
    
    def get_NFTs(self):
        return self.NFTs_instances
    
    def get_all_NFTs_details(self):
        details = []
        for nft in self.NFTs_instances:
            if not nft.Hidden:
                details.append(nft.get_NFT_details())
        return details
        

    def get_headers(self):
        headers = ["Name", "Token Id", "Contract Address", "Image", "End Of URL", "ETH Floor Price", "Hidden", "USD Price", "ILS Price"]
        return headers

    def calculate_total_value(self):
        sum_USD = 0
        sum_ILS = 0
        for nft in self.NFTs_instances:
            sum_USD += nft.get_USD_value()
            sum_ILS += nft.get_ILS_value()
        return sum_USD, sum_ILS

    def calculate_total_ETH(self):
        sum_ETH = 0
        for nft in self.NFTs_instances:
            sum_ETH += nft.get_ETH_value()
        return sum_ETH