#!/usr/bin/python

import sys
import argparse
from argparse import RawTextHelpFormatter
from lib.database import Database
from lib.setup import *
from lib.sources import Coinmarketcap
from lib.updater import Updater
from lib.utils import Utils

def main():
    print '''
   11
  ====,
   1   )   Cryptocoin-Market-Toolkit
   1===    v 1.1
   1   )   
  ====^
   11 
    '''
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)

    parser.add_argument(
        "--setup",
        help="Initial setup\n"
        "$ ./cmt.py --setup --localcurrency INR\n"
        "Available currencies:\n"
        "AUD, BRL, CAD, CHF, CLP, CNY, CZK, DKK, EUR, GBP\n"
        "HKD, HUF, IDR, ILS, INR, JPY, KRW, MXN, MYR, NOK\n"
        "NZD, PHP, PKR, PLN, RUB, SEK, SGD, THB, TRY, TWD, ZAR",
        action="store_true"
    )
    parser.add_argument(
        "--localcurrency",
        help="See --setup",
        action="store",
        metavar=""
    )
    '''
    parser.add_argument(
        "-u", 
        "--update", 
        help="Update local database", 
        action="store_true"
    )
    '''
    parser.add_argument(
        "-t",
        "--top",        
        help="Show top coins\n"
        "$ ./cmt.py --top 20\n"
        "$ ./cmt.py --top 50 --sortorder marketcap_desc",
        action="store",
        metavar=""
    )
    parser.add_argument(
        "-s", 
        "--search", 
        help="Search coins\n"
        "$ ./cmt.py --search bitcoin\n"
        "$ ./cmt.py --search bitcoin --sortorder price_desc",
        action="store",
        metavar=""
    )
    parser.add_argument(
        "-so", 
        "--sortorder", 
        help="Use with --search or --top\n"
        "Available options\n"
        "[rank | rank_asc | rank_desc | marketcap | marketcap_asc |\n"
        "marketcap_desc | price | price_asc | price_desc ]", 
        default=None,
        action="store",
        metavar=""
    )
    args = parser.parse_args()
    if (len(sys.argv) <= 1):
        parser.print_help()
    

    # connect to database
    db = Database()
    db_resource = db.connect()


    # initial setup    
    if args.setup and args.localcurrency:
        setup_init(db_resource[0], db_resource[1], args.localcurrency)
    elif args.setup:
        setup_init(db_resource[0], db_resource[1])

    # config & metadata
    db_resource[1].execute("select * from meta_table")
    meta = db_resource[1].fetchall()
    db_resource[1].execute("select * from config_table")
    config = db_resource[1].fetchone()
    
    # auto update
    updater = Updater(db_resource, meta, config)
    updater.auto_update()
    
    utils = Utils(db_resource, meta, config)
    # top coins
    if args.top and args.sortorder:
        utils.top_coins(args.top, args.sortorder)
    elif args.top:
        utils.top_coins(args.top)

    # search
    if args.search and args.sortorder:
        utils.search_coins(args.search, args.sortorder) 
    elif args.search:
        utils.search_coins(args.search)
    
    # finally close the database connection
    db.close()


if __name__ == '__main__':
    main()
