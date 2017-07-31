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

if len(sys.argv) <= 1:
    print 'Usage: python %s <order_number>' % (sys.argv[0])
else:
    order_number = sys.argv[1]

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(buffered=True)
    query_str = "SELECT order_number, order_items, total_price_rmb, total_price_ntd, all_price_rmb, all_price_ntd, created_time, remark, freight_rmb, freight_ntd, ccat_delivery_number from orders WHERE order_number=" + order_number
    query = (query_str)
    cursor.execute(query)

    for (order_number, order_items, total_price_rmb, total_price_ntd, all_price_rmb, all_price_ntd, created_time, remark, freight_rmb, freight_ntd, ccat_delivery_number) in cursor:
        print u'訂單編號: %s' % (order_number)
        print u'訂單內容: %s' % (order_items)
        print u'合計(¥): %s' % (total_price_rmb)
        print u'合計(NT$): %s' % (total_price_ntd)
        print u'運費: ¥ %.2f' % (freight_rmb)
        print u'運費: NT$ %.2f' % (freight_ntd)
        print u'總金額(¥): %s' % (all_price_rmb)
        print u'總金額(NT$): %s' % (all_price_ntd)
        print u'備註: %s' % (remark)
        print u'建立時間: %s' % (created_time)
        print u'黑貓單號: %s' % (ccat_delivery_number)

    cursor.close()
    cnx.close()