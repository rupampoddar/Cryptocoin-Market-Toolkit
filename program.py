#!/usr/bin/python

import argparse
import requests
import sqlite3
import json
import time
import sys

db = None
cursor = None

coinmarketcap_api_url = "https://api.coinmarketcap.com/v1/ticker/"
coinmarketcap_payload = {}


'''
read config data from config.json file
'''
def read_config():
	config = []
	with open('config.json','r') as configfile:
		config = json.load(configfile)
	return config	


'''
connect to local sqlite database
database schema should already exist
'''
def connect_database():
	global db
	global cursor
	try:
		db = sqlite3.connect('sqlite.db')
		cursor = db.cursor()
	except Exception as e:
		print "[*] error connecting to database"
		raise e


'''
close the database connection
'''
def close_database():
	global db
	global cursor
	db.close()


'''
local database auto-updater (not in use)
'''
def updater_check():
	with open('meta.json','r') as metafile:
		data = json.load(metafile)
	db_last_update = data['database_last_update_timestamp']
	current_timestamp = int(time.time())
	if (current_timestamp - db_last_update) > 300:
		print "[*] auto-updating"
		update_database()
	else:
		print "[*] local database up-to-date"	


'''
returns when local database was updated
'''
def get_last_update_time():
	x = ''
	with open('meta.json','r') as metafile:
		data = json.load(metafile)
		diff = int(time.time()) - int(data['database_last_update_timestamp'])
		if diff >= (24*2600):
			x = '1 d ago'
		elif diff >= 3600:
			tmp = (diff/3600)
			x = '{0} hr ago'.format(tmp)	
		else:
			tmp = (diff/60)
			x = '{0} min ago'.format(tmp)
	return x
		

'''
updates the local database
'''
def update_database():
	global db
	global cursor
	try:
		print "[*] downloading content (CoinMarketCap)"
		api_response = requests.get(coinmarketcap_api_url, params=coinmarketcap_payload, timeout=10)
		json_data = api_response.json()
		# loop through json and build a list
		data_list = []
		for x in json_data:
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
			data_list.append(t)

		# update local database
		print "[*] updating local database"
		cursor.executemany(
			'''
			replace into cryptocoins 
			(id, name, symbol, rank, price_usd, price_btc, volume_usd_24h,
			market_cap_usd, available_supply, total_supply, percent_change_1h,
			percent_change_24h, percent_change_7d, last_updated) 
			values 
			(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
			''',
			data_list
		)
		db.commit()

		# udpate meta file
		data = None
		with open('meta.json','r') as metafile:
			data = json.load(metafile)
			data['database_last_update_timestamp'] = int(time.time())
		with open('meta.json','w') as metafile:
			json.dump(data, metafile)
		print "[*] done"

	except requests.exceptions.ConnectionError as ex1:
		print "[*] connection failure"
		
	except Exception as ex:
		print str(ex)
		db.rollback()


'''
show list if top coins
can be sorted by different fields
'''
def top_coins(limit, sort=None):
	global db
	global cursor
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

	try:
		cursor.execute(
			'''select id,name,symbol,rank,price_usd,market_cap_usd 
			from cryptocoins order by {0} limit ?'''.format(orderby),
			(limit,)
		)
		res = cursor.fetchall()

		# print
		print "[#] Top: {0} coins\n[#] Sort Order: {1}\n".format(limit,orderby)
		print '{0: <5} {1: <25} {2: <10} {3: >15} {4: >20}'.format('Rank','Name','Symbol','Price (USD)','Market Cap (USD)')
		print '----- ------------------------- ---------- --------------- --------------------'
		for i in res:
			rank=i[3]
			name=i[1][:25]
			symbol=i[2]
			price_usd='None' if i[4] is None else float(i[4])
			market_cap_usd='None' if i[5] is None else float(i[5])
			print '{0: <5} {1: <25} {2: <10} {3: >15} {4: >20}'.format(rank, name, symbol, price_usd, market_cap_usd)
	
	except Exception as e:
		raise e	


'''
Search the local database
'''
def search(q, sort=None):
	global db
	global cursor
	query = '%'+q.lower()+'%'
	
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

	try:
		cursor.execute(
			'''select id,name,symbol,rank,price_usd,market_cap_usd 
			from cryptocoins 
			where name like ? 
			collate nocase
			order by {0}'''.format(orderby,),
			(query,)
		)
		res = cursor.fetchall()

		# print
		print "[#] Search Query: {0}\n[#] Sort Order: {1}\n".format(q,orderby)
		print '{0: <5} {1: <25} {2: <10} {3: >15} {4: >20}'.format('Rank','Name','Symbol','Price (USD)','Market Cap (USD)')
		print '----- ------------------------- ---------- --------------- --------------------'
		for i in res:
			rank=i[3]
			name=i[1][:25]
			symbol=i[2]
			price_usd='None' if i[4] is None else float(i[4])
			market_cap_usd='None' if i[5] is None else float(i[5])
			print '{0: <5} {1: <25} {2: <10} {3: >15} {4: >20}'.format(rank, name, symbol, price_usd, market_cap_usd)
	
	except Exception as e:
		raise e		


'''
the main
'''
def main():
	print "[$-------------------------------$]"
	print "[$   CryptoCoin Market Toolkit   $]"
	print "[$-------------------------------$]\n"
	print "[#] v 1.0 | Source - CoinMarketCap"
	print "[#] local database last updated : {0}".format(get_last_update_time())
	print ""
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"-u", 
		"--update", 
		help="update local database", 
		action="store_true"
	)
	parser.add_argument(
		"-t",
		"--top",
		action="store",
		help='''show top coins, e.g. --top 50 --sortorder marketcap_desc''',
		default=None
		
	) 
	parser.add_argument(
		"-s", 
		"--search", 
		help="search local database. e.g. --search bitcoin",
		action="store"
	)
	parser.add_argument(
		"-so", 
		"--sortorder", 
		help='''use with --search|--top, available values [rank|rank_asc|
				rank_desc|marketcap|marketcap_asc|
				marketcap_desc|price|price_asc|price_desc]
				e.g. --search bitcoin --sortorder price_desc''', 
		default=None,
		action="store"
	)
	args = parser.parse_args()
	if (len(sys.argv) <= 1):
		parser.print_help()
	
	# connect to local database
	connect_database()

	# update
	if args.update:
		update_database()
	
	# top coins
	if args.top and args.sortorder:
		top_coins(args.top, args.sortorder)
	elif args.top:
		top_coins(args.top)

	# search
	if args.search and args.sortorder:
		search(args.search, args.sortorder)	
	elif args.search:
		search(args.search)

	# finally close the database connection
	close_database()


if __name__ == '__main__':
	main()
