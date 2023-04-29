import os 
import json
import random
import aiohttp
import asyncio
import requests
import itertools

from datetime import datetime 
from nanoid import generate
from typing import List, Dict


class ServiceTesting():

    def __init__(self):
        self.url = 'http://localhost:8080/v3/hodl'
        self.tickers_list = os.environ['TICKERS'].split(' ')
        self.ls = ['.True', '.False']
        self.input_currency_list = ['gbp', 'eurs', 'chf', 'eur', 'eurs', 'brl']
                
    def main(self):
        x = self.feed()
        result = asyncio.run(self.fetch_all(params_dict=x))
        return result        
                
    def feed(self):
        crossection = list(itertools.product(self.tickers_list, self.input_currency_list, self.ls))
        random.shuffle(crossection)
        
        params_dict = []
        for value in crossection[0:3]:

            data = {
            "date": datetime.utcnow().isoformat() + 'Z',
            "initial": 0,
            "inputAmount": f"{1000}",
            "inputTicker": f"{value[1]}",
            "tariffId": f"{value[0].replace('-','')}{value[2]}",
            "requestId": f"{generate()}",
            "leverage": f"{random.randint(4, 25)}"}
            
            params_dict.append(data)
            
        return params_dict
    
    async def fetch_all(self, params_dict:List) -> List:
        tasks = []
        for i in range(1,len(params_dict),1):
            task = asyncio.create_task(self.fetch(data = params_dict[i])) 
            tasks.append(task)
        result = await asyncio.gather(*tasks)
        return result
    
    async def fetch(self, data:Dict) -> List:
        async with aiohttp.ClientSession() as session:
            async with session.post(url=self.url, data=data) as response:
                data = await response.json()
                return(data)
        
   
