# -*- coding: utf-8 -*-

import sys
import mysql.connector
import requests
import config
from datetime import datetime

config = {
  'user': config.MYSQL_USER,
  'password': config.MYSQL_PASS,
  'host': config.MYSQL_HOST,
  'database': config.MYSQL_DB,
  'raise_on_warnings': True,
}

exchange_rate = 4.6
fee = 0.03

if len(sys.argv) <= 8:
    print 'Usage: python %s <order_number> <order_items> <remark> <freight_rmb> <weight> <total_price_rmb> <cargo_order_number> <user>' % (sys.argv[0])
else:
    order_number = sys.argv[1]
    order_items = sys.argv[2]
    remark = sys.argv[3]
    freight_rmb = float(sys.argv[4])
    freight_ntd = freight_rmb * exchange_rate
    weight = float(sys.argv[5])
    total_price_rmb = float(sys.argv[6])
    cargo_order_number = sys.argv[7]
    total_price_ntd = total_price_rmb * exchange_rate
    all_price_rmb = total_price_rmb + (freight_rmb * (1 + fee))
    all_price_ntd = all_price_rmb * exchange_rate
    user = sys.argv[8]

    cnx = mysql.connector.connect(**config)

    add_order = ("INSERT INTO orders "
                "(order_number, order_items, total_price_rmb, total_price_ntd, all_price_rmb, all_price_ntd, remark, weight, freight_rmb, freight_ntd, cargo_order_number, user) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    order_service = (order_number, order_items, total_price_rmb, total_price_ntd, all_price_rmb, all_price_ntd, remark, weight, freight_rmb, freight_ntd, cargo_order_number, user)

    try:
        cursor = cnx.cursor(buffered=True)
        cursor.execute(add_order, order_service)
        cnx.commit()
        print 'Insert success'

    except Exception, ex:
        print 'Insert fail!!!'
        print ex

    cursor.close()
    cnx.close()