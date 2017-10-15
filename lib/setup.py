#!/usr/bin/python

from .database import Database

def setup_init(db_con, db_cur, localcurrency='usd'):
	s1 = ''
	s2 = ''
	if localcurrency is not None:
		if localcurrency.upper() in ['AUD','BRL','CAD','CHF','CLP','CNY','CZK','DKK','EUR','GBP','HKD','HUF','IDR','ILS','INR','JPY','KRW','MXN','MYR','NOK','NZD','PHP','PKR','PLN','RUB','SEK','SGD','THB','TRY','TWD','ZAR']:
			c = localcurrency.lower()
			s1 = ', price_{} real, vol_{}_24h real, market_cap_{} real'.format(c,c,c)
			s2 = ', total_market_cap_{} real, total_24h_volume_{} real'.format(c,c)

	try:
		sql1 = '''create table coinmarketcap_ticker (
			id text unique,
			name text,
			symbol text,
			rank integer,
			price_usd real,
			price_btc real,
			volume_usd_24h real,
			market_cap_usd real,
			available_supply real,
			total_supply real,
			percent_change_1h real,
			percent_change_24h real,
			percent_change_7d real,
			last_updated integer{0}
		);'''.format(s1)

		sql2 = '''create table coinmarketcap_global (
			total_market_cap_usd real, 
    		total_24h_volume_usd real, 
    		bitcoin_percentage_of_market_cap real, 
    		active_currencies integer, 
    		active_assets integer, 
    		active_markets integer{0}
		);'''.format(s2)

		sql3 = '''create table meta_table (
			source text unique,
			last_updated integer
		)'''

		sql4 = '''create table config_table (
			id integer,
			local_currency text
		)
		'''
		sql5 = "insert into config_table (id, local_currency) values (?,?)"
		db_cur.execute(sql1)
		db_cur.execute(sql2)
		db_cur.execute(sql3)
		db_cur.execute(sql4)
		db_cur.execute(sql5, (1,localcurrency.upper()))
		db_con.commit()

		print "[*] Setup complete"
	except Exception as e:
		print "[*] Error: "+str(e)
		db_con.rollback()