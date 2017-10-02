#!/usr/bin/python
import sqlite3
try:
	db = sqlite3.connect('sqlite.db')
	cursor = db.cursor()

	sql_statement = '''create table cryptocoins (
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
		last_updated integer
	);
	'''
	cursor.execute(sql_statement)
	db.commit()
except Exception as e:
	print('Exception Occured')
	raise e
	db.rollback() 
finally:	
	db.close()