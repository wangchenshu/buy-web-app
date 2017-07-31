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

exchange_rate = 4.6
fee = 0.03

if len(sys.argv) <= 7:
    print 'Usage: python %s <name> <qty> <price_rmb> <url> <order_number> <order_number_taobao> <taobao_delivery_number>' % (sys.argv[0])
else:
    name = sys.argv[1]
    qty = int(sys.argv[2])
    price_rmb = float(sys.argv[3])
    price_ntd = price_rmb * exchange_rate

    total_price_rmb = qty * float(price_rmb) * (1 + fee)
    total_price_ntd = total_price_rmb * exchange_rate
    url = sys.argv[4]
    order_number = sys.argv[5]
    order_number_taobao = sys.argv[6]
    taobao_delivery_number = sys.argv[7]

    cnx = mysql.connector.connect(**config)

    add_order = ("INSERT INTO order_items "
                "(name, qty, exchange_rate, price_rmb, price_ntd, fee, total_price_rmb, total_price_ntd, url, order_number, order_number_taobao, taobao_delivery_number) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    order_service = (name, qty, exchange_rate, price_rmb, price_ntd, fee, total_price_rmb, total_price_ntd, url, order_number, order_number_taobao, taobao_delivery_number)

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