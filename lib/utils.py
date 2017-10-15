#!/usr/bin/python

from tabulate import tabulate

class Utils:
    def __init__(self, db, meta, config):
        self.db_con = db[0]
        self.db_cur = db[1]
        self.meta = meta
        self.config = config


    def __sort(self, sort = None):
        ''' Calculates order by field used in SQL query '''
        if sort is None:
            orderby = 'rank asc'
        else:
            if '_' in sort:
                sort = sort.split('_')
                sort_by = sort[0] if sort[0] in ['price','marketcap'] else 'rank'
                sort_order = sort[1] if sort[1] in ['asc','desc'] else 'asc'
            else:
                sort_by = sort if sort in ['price','marketcap'] else 'rank'
                sort_order = 'asc'

            if sort_by == 'price':
                sort_by = 'price_usd'
            elif sort_by == 'marketcap':
                sort_by = 'market_cap_usd'
            orderby = sort_by + " " + sort_order
        return orderby


    def __print_table(self, data):
        ''' Prints data as a table '''
        c = self.config[1].lower()
        if c == 'usd':
            headers = ['Rank','Name','Symbol','Price (USD)','Market Cap (USD)']
        else:
            tmp = c.upper()
            headers = ['Rank','Name','Symbol','Price ({})'.format(tmp),'Market Cap ({})'.format(tmp),'Price (USD)','Market Cap (USD)']
        
        # build table data
        table_data = []
        for i in data:
            rank=i[3]
            name=i[1][:25]
            symbol=i[2]
            price_usd='None' if i[4] is None else float(i[4])
            market_cap_usd='None' if i[5] is None else float(i[5])
            if c == 'usd':
                l = [rank,name,symbol,price_usd,market_cap_usd]
            else:
                price_local = i[6]
                market_cap_local = i[7] 
                l = [rank,name,symbol,price_local,market_cap_local,price_usd,market_cap_usd]    
            table_data.append(l)
        
        # print table
        print tabulate(table_data, headers=headers, tablefmt="plsql", floatfmt=('','','','.2f','.0f','.6f','.0f'))


    def top_coins(self, limit, sort = None):
        ''' List top coins '''
        orderby = self.__sort(sort)
        c = self.config[1].lower()
        if c == 'usd':
            query = \
            '''select id,name,symbol,rank,price_usd,market_cap_usd 
            from coinmarketcap_ticker order by {} limit ?'''.format(orderby)            
        else:
            query = \
            '''select id,name,symbol,rank,price_usd,market_cap_usd, price_{},market_cap_{} 
            from coinmarketcap_ticker order by {} limit ?'''.format(c,c,orderby)
            
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
            '''select id,name,symbol,rank,price_usd,market_cap_usd 
            from coinmarketcap_ticker 
            where name like ? 
            collate nocase
            order by {0}'''.format(orderby,)
        else:
            sql = \
            '''select id,name,symbol,rank,price_usd,market_cap_usd,price_{},market_cap_{}
            from coinmarketcap_ticker
            where name like ? 
            collate nocase
            order by {}'''.format(c,c,orderby)

        try:
            self.db_cur.execute(sql,(search_query,))
            res = self.db_cur.fetchall()
            # print table
            print "[#] Search Query: {0}\n[#] Sort Order: {1}\n".format(q,orderby)
            self.__print_table(res)

        except Exception as e:
            raise e     
