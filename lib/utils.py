#!/usr/bin/python

from tabulate import tabulate

class Utils:
    def __init__(self, db, meta, config):
        self.db_con = db[0]
        self.db_cur = db[1]
        self.meta = meta
        self.config = config
        self.percent_change = '24h'

    def __sort(self, sort = None):
        ''' Calculates order by field used in SQL query '''
        if sort is None:
            orderby = 'rank asc'
        else:
            if '_' in sort:
                sort = sort.split('_')
                sort_by = sort[0] if sort[0] in ['price','marketcap','pc1','pc24','pc7','supply'] else 'rank'
                sort_order = sort[1] if sort[1] in ['asc','desc'] else 'asc'
            else:
                sort_by = sort if sort in ['price','marketcap','pc1','pc24','pc7','supply'] else 'rank'
                sort_order = 'asc'
            
            if sort_by == 'price':
                sort_by = 'price_usd'
            elif sort_by == 'marketcap':
                sort_by = 'market_cap_usd'
            
            # Expand short forms
            if sort_by in ['pc1','pc24','pc7','supply']:
                if sort_by == 'pc1':
                    sort_by = 'percent_change_1h'
                    self.percent_change = '1h'
                elif sort_by == 'pc24':
                    sort_by = 'percent_change_24h'
                    self.percent_change = '24h'
                elif sort_by == 'pc7':
                    sort_by = 'percent_change_7d'
                    self.percent_change = '7d'
                elif sort_by == 'supply':
                    sort_by = 'available_supply'            
            orderby = sort_by + " " + sort_order
        return orderby


    def __print_table(self, data):
        ''' Prints data as a table '''
        c = self.config[1].lower()
        if c == 'usd':
            headers = ['Rank','Name','Symbol','Price (USD)','Market Cap (USD)','Available Supply','% Change {}'.format(self.percent_change)]
        else:
            tmp = c.upper()
            headers = ['Rank','Name','Symbol','Price ({})'.format(tmp),'Market Cap ({})'.format(tmp),'Price (USD)','Market Cap (USD)','Available Supply','% Change {}'.format(self.percent_change)]
        
        # build table data
        table_data = []
        for i in data:
            rank=i[3]
            name=i[1][:25]
            symbol=i[2]
            price_usd='-' if i[4] is None else "{0:,.4f}".format(float(i[4]))
            market_cap_usd='-' if i[5] is None else "{0:,.2f}".format(float(i[5]))
            available_supply='-' if i[6] is None else "{0:,.0f}".format(float(i[6]))
            percent_change = '-' if i[7] is None else float(i[7])
            if percent_change != '-':
                if percent_change < 0:
                    percent_change = '{} %'.format(percent_change)
                else:
                    percent_change = '+{} %'.format(percent_change)    
            if c == 'usd':
                l = [rank,name,symbol,price_usd,market_cap_usd,percent_change]
            else:
                price_local = i[8]
                market_cap_local = '-' if i[9] is None else float(i[9])
                l = [rank,name,symbol,price_local,market_cap_local,price_usd,market_cap_usd,available_supply,percent_change]    
            table_data.append(l)
        
        # print table
        print tabulate(table_data, headers=headers, tablefmt="plsql", floatfmt=('','','','.4f','.0f','.6f','.0f','.2f'), numalign="right",stralign="right")


    def top_coins(self, limit, sort = None):
        ''' List top coins '''
        orderby = self.__sort(sort)
        c = self.config[1].lower()
        if c == 'usd':
            query = \
            '''select id,name,symbol,rank,price_usd,market_cap_usd,available_supply,percent_change_{} 
            from coinmarketcap_ticker order by {} limit ?'''.format(self.percent_change,orderby)            
        else:
            query = \
            '''select id,name,symbol,rank,price_usd,market_cap_usd,available_supply,percent_change_{},price_{},market_cap_{} 
            from coinmarketcap_ticker order by {} limit ?'''.format(self.percent_change,c,c,orderby)
            
        try:
            self.db_cur.execute(query,(limit,))
            res = self.db_cur.fetchall()
            
            # print table
            print "[#] Top: {0} coins\n[#] Sort Order: {1}\n".format(limit,orderby)
            self.__print_table(res)
        except Exception as e:
            raise e 


    def search_coins(self,q, sort=None):
        ''' Search coins '''
        search_query = '%'+q.lower()+'%'
        
        orderby = self.__sort(sort)
        orderby = self.__sort(sort)
        c = self.config[1].lower()
        if c == 'usd':
            sql = \
            '''select id,name,symbol,rank,price_usd,market_cap_usd,available_supply,percent_change_{} 
            from coinmarketcap_ticker 
            where name like ? 
            collate nocase
            order by {0}'''.format(self.percent_change,orderby)
        else:
            sql = \
            '''select id,name,symbol,rank,price_usd,market_cap_usd,available_supply,percent_change_{},price_{},market_cap_{}
            from coinmarketcap_ticker
            where name like ? 
            collate nocase
            order by {}'''.format(self.percent_change,c,c,orderby)

        try:
            self.db_cur.execute(sql,(search_query,))
            res = self.db_cur.fetchall()
            # print table
            print "[#] Search Query: {0}\n[#] Sort Order: {1}\n".format(q,orderby)
            self.__print_table(res)

        except Exception as e:
            raise e     


    def watch_coin(self, coin_symbol):
        ''' '''
        pass