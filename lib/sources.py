#!/usr/bin/python

import requests
import json


class Coinmarketcap:
    def __init__(self):
        self.cmc_api_ticker = "https://api.coinmarketcap.com/v1/ticker/"
        self.cmc_api_global = "https://api.coinmarketcap.com/v1/global/"


    def get_api_data(self, localcurrency=None):
        payload = {}
        if localcurrency is not None:
            c = localcurrency.upper()
            if c in ['AUD','BRL','CAD','CHF','CLP','CNY','CZK','DKK','EUR','GBP','HKD','HUF','IDR','ILS','INR','JPY','KRW','MXN','MYR','NOK','NZD','PHP','PKR','PLN','RUB','SEK','SGD','THB','TRY','TWD','ZAR']:
                payload = {'convert': c}
        
        data = None

        try:            
            res = requests.get(self.cmc_api_ticker, params=payload, timeout=10)
            data = res.json()
        except requests.exceptions.ConnectionError as ex1:
            print "[*] connection failure"
            raise ex1        
        except Exception, e:
            print str(e)
            raise e
        finally:
            return data