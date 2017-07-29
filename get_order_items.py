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
    query_str = "SELECT name, qty, exchange_rate, price_rmb, price_ntd, fee, total_price_rmb, total_price_ntd, order_number from order_items WHERE order_number = " + order_number
    query = (query_str)
    cursor.execute(query)

    all_rmb = 0.0
    all_ntd = 0.0
    all_items = '' 

    for (name, qty, exchange_rate, price_rmb, price_ntd, fee, total_price_rmb, total_price_ntd, order_number) in cursor:
        print u'商品: %s' % (name)
        print u'數量: %d' % (qty)
        print u'匯率: %.2f' % (exchange_rate)
        print '¥ %.2f' % (price_rmb)
        print 'NT$ %.2f' % (price_ntd)
        print u'手續費: %.2f' % (fee)
        print u'合計: ¥ %.2lf' % (total_price_rmb)
        print u'合計: NT$ %.2lf' % (total_price_ntd)
        print u'訂單編號: %s' % (order_number)
        print '--------'
        all_items += name + ', '
        all_rmb += total_price_rmb
        all_ntd += total_price_ntd

    cursor.close()
    cnx.close()

    print 'items: ' + all_items
    print 'All RMB: ' + str(all_rmb)
    print 'All NT$: ' + str(all_ntd)