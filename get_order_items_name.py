# -*- coding: utf-8 -*-

import sys
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

order_number = 0

if len(sys.argv) <= 1:
    print 'Usage: python %s <order_number>' % (sys.argv[0])
else:
    order_number = sys.argv[1]

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(buffered=True)
    query_str = "SELECT name, qty, exchange_rate, price_rmb, price_ntd, fee, total_price_rmb, total_price_ntd, order_number, order_number_taobao, taobao_delivery_number, weight from order_items WHERE order_number = " + order_number
    query = (query_str)
    cursor.execute(query)

    all_rmb = 0.0
    all_ntd = 0.0
    all_weight = 0.0
    all_items = '' 

    #print '商品,數量,匯率,單價(¥),單價(NT$),手續費,合計(¥),合計(NT$),訂單編號,淘寶訂單編號,淘寶貨運單號'
    for (name, qty, exchange_rate, price_rmb, price_ntd, fee, total_price_rmb, total_price_ntd, order_number, order_number_taobao, taobao_delivery_number, weight) in cursor:
        #print '%s,%d,%.2f,%.2f,%.2f,%.2f,%.2lf,%.2lf,%s,%s,%s' % (name, qty, exchange_rate, price_rmb, price_ntd, fee, total_price_rmb, total_price_ntd, order_number, order_number_taobao, taobao_delivery_number)
        print u'商品: %s, 淘寶貨運單號: %s' % (name, taobao_delivery_number)

    cursor.close()
    cnx.close()