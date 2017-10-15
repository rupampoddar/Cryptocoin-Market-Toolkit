#!/usr/bin/python

import sqlite3
import os
from .sources import Coinmarketcap

class Database:

    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), "../data/sqlite.db")
        
    def connect(self):
        try:
            self.con = sqlite3.connect(self.db_path)
            self.cur = self.con.cursor()
            return [self.con, self.cur]
        except Exception, e:
            print "[*] error connecting to database"
            raise e

    def get_cursor(self):
        return self.cur

    def close(self):
        self.con.close()