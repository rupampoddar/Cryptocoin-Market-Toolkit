#!/usr/bin/python

import time
from .sources import Coinmarketcap

class Updater:
    def __init__(self, db, meta, config):
        self.db_con = db[0]
        self.db_cur = db[1]
        self.meta = meta
        self.config = config


    def __update_cmc_ticker_table(self, data):
        ''' updates coinmarketcap_ticker table '''
        lc = self.config[1].lower()
        if lc == 'usd':
            query = '''
                replace into coinmarketcap_ticker 
                (id, name, symbol, rank, price_usd, price_btc, volume_usd_24h,
                market_cap_usd, available_supply, total_supply, percent_change_1h,
                percent_change_24h, percent_change_7d, last_updated) 
                values 
                (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                '''
        else:
            query = '''
                replace into coinmarketcap_ticker 
                (id, name, symbol, rank, price_usd, price_btc, volume_usd_24h,
                market_cap_usd, available_supply, total_supply, percent_change_1h,
                percent_change_24h, percent_change_7d, last_updated, price_{}, 
                vol_{}_24h, market_cap_{}) 
                values 
                (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                '''.format(lc,lc,lc)

        try:
            self.db_cur.executemany(query,data)
            self.db_cur.execute(
                "replace into meta_table (source,last_updated) values (?,?)",('coinmarketcap',int(time.time()))
            )
            self.db_con.commit()
            print "[*] Autoupdated: CoinMarketCap"
        except Exception, e:
            print str(e)    


    def __need_update(self, ts):
        ''' update every 5 mins '''
        now = int(time.time())
        if (now-ts) > 300:
            return True
        return False    


    def __update_cmc(self):
        # localcurrency
        lc = self.config[1].upper()
        lc = lc if lc != 'USD' else None

        cmc = Coinmarketcap()
        cmc_data = cmc.get_api_data(lc)
        if cmc_data is not None:            
            # loop through json and build a list
            l = []
            for x in cmc_data:
                t = (
                    x['id'], 
                    x['name'], 
                    x['symbol'], 
                    x['rank'], 
                    x['price_usd'],
                    x['price_btc'], 
                    x['24h_volume_usd'], 
                    x['market_cap_usd'],
                    x['available_supply'],
                    x['total_supply'],
                    x['percent_change_1h'],
                    x['percent_change_24h'],
                    x['percent_change_7d'],
                    x['last_updated']
                )
                # add localcurrency fields
                if lc is not None:
                    t = t + (x['price_inr'], x['24h_volume_inr'], x['market_cap_inr'])
                l.append(t)
            # update cmc ticker table
            self.__update_cmc_ticker_table(l)


    def auto_update(self):
        ''' Fetches API data from different sources & updates local db '''                
        if not self.meta:
            # initial update
            self.__update_cmc()
        else:
            # subsequent updates    
            for x in self.meta:
                if x[0] == 'coinmarketcap' and self.__need_update(x[1]):
                    self.__update_cmc()

