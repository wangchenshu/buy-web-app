# -*- coding: utf-8 -*-

import mysql.connector
import requests
import config

config = {
  'user': config.MYSQL_USER,
  'password': config.MYSQL_PASS,
  'host': config.MYSQL_HOST,
  'database': config.MYSQL_DB,
  'raise_on_warnings': True,
}

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor(buffered=True)

query = ("SELECT name, qty, exchange_rate, price_rmb, price_ntd, fee, total_price_rmb, total_price_ntd from my_orders")
cursor.execute(query)

for (name, qty, exchange_rate, price_rmb, price_ntd, fee, total_price_rmb, total_price_ntd) in cursor:
    #print name, qty, exchange_rate, price_rmb, price_ntd, fee, total_price_rmb, total_price_ntd
    print u'%s, 數量: %d, 匯率: %.2f, ¥ %.2f, NT$ %.2f, 手續費: %.2f, 合計: ¥ %.2lf, 合計: NT$ %.2lf' % (name, qty, exchange_rate, price_rmb, price_ntd, fee, total_price_rmb, total_price_ntd)

cursor.close()
cnx.close()