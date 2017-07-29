#-*- coding: utf-8 -*-
import sys
import mysql.connector

from flask import Flask
from flask import request
from flask import jsonify
from flask import Response
from flask import render_template

import logging
import json
import config

app = Flask(__name__, static_url_path='/static')

config = {
  'user': config.MYSQL_USER,
  'password': config.MYSQL_PASS,
  'host': config.MYSQL_HOST,
  'database': config.MYSQL_DB,
  'raise_on_warnings': True,
}

@app.route('/orders/')
def readpage():
    return render_template('order.html')

@app.route("/order/lists/<order_number>")
def order_list_order_number(order_number):
    reload(sys)
    sys.setdefaultencoding('utf-8')

    try:
        logging.warning ('order_number: ' + order_number)

        cnx = mysql.connector.connect(user=config['user'],
                                      password=config['password'],
                                      host=config['host'],
                                      database=config['database'])

        cursor = cnx.cursor()

        query = ("SELECT order_number, order_items, total_price_rmb, total_price_ntd, all_price_rmb, all_price_ntd, created_time, remark, freight_rmb, freight_ntd from orders WHERE order_number = " + order_number)
        #logging.warning(query)

        cursor.execute(query)

        orders = []

        for (order_number, order_items, total_price_rmb, total_price_ntd, all_price_rmb, all_price_ntd, created_time, remark, freight_rmb, freight_ntd) in cursor:
            #logging.warning("data: {}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(order_number, order_items, total_price_rmb, total_price_ntd, all_price_rmb, all_price_ntd, created_time, remark, freight_rmb, freight_ntd))
            resp_order = {
                u'訂單編號': '',
                u'訂單內容': '',
                u'建立時間': '',
                u'備註': '',
                u'合計(¥)': '',
                u'合計(NT$)': '',
                u'運費(¥)': '',
                u'運費(NT$)': '',
                u'總金額(¥)': '',
                u'總金額(NT$)': ''
            }

            resp_order[u'訂單編號'] = order_number
            resp_order[u'訂單內容'] = order_items
            resp_order[u'建立時間'] = created_time
            resp_order[u'備註'] = remark
            resp_order[u'合計(¥)'] = total_price_rmb
            resp_order[u'合計(NT$)'] = total_price_ntd
            resp_order[u'運費(¥)'] = freight_rmb
            resp_order[u'運費(NT$)'] = freight_ntd
            resp_order[u'總金額(¥)'] = all_price_rmb
            resp_order[u'總金額(NT$)'] = all_price_ntd
            
            orders.append(resp_order)

        cursor.close()
        cnx.close()

        return render_template('order_list.html', orders=orders)

    except Exception, ex:
        logging.error(str(ex))
    
    return render_template('order.html')

@app.route("/order_lists", methods=['POST'])
def order_list():
    reload(sys)
    sys.setdefaultencoding('utf-8')

    try:
        result = request.form
        order_number = result['order_number']
        logging.warning ('order_number: ' + order_number)

        cnx = mysql.connector.connect(user=config['user'],
                                      password=config['password'],
                                      host=config['host'],
                                      database=config['database'])

        cursor = cnx.cursor()

        query = ("SELECT order_number, order_items, total_price_rmb, total_price_ntd, all_price_rmb, all_price_ntd, created_time, remark, freight_rmb, freight_ntd from orders WHERE order_number = " + order_number)
        #logging.warning(query)

        cursor.execute(query)

        orders = []

        for (order_number, order_items, total_price_rmb, total_price_ntd, all_price_rmb, all_price_ntd, created_time, remark, freight_rmb, freight_ntd) in cursor:
            #logging.warning("data: {}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(order_number, order_items, total_price_rmb, total_price_ntd, all_price_rmb, all_price_ntd, created_time, remark, freight_rmb, freight_ntd))
            resp_order = {
                u'訂單編號': '',
                u'訂單內容': '',
                u'建立時間': '',
                u'備註': '',
                u'合計(¥)': '',
                u'合計(NT$)': '',
                u'運費(¥)': '',
                u'運費(NT$)': '',
                u'總金額(¥)': '',
                u'總金額(NT$)': ''
            }

            resp_order[u'訂單編號'] = order_number
            resp_order[u'訂單內容'] = order_items
            resp_order[u'建立時間'] = created_time
            resp_order[u'備註'] = remark
            resp_order[u'合計(¥)'] = total_price_rmb
            resp_order[u'合計(NT$)'] = total_price_ntd
            resp_order[u'運費(¥)'] = freight_rmb
            resp_order[u'運費(NT$)'] = freight_ntd
            resp_order[u'總金額(¥)'] = all_price_rmb
            resp_order[u'總金額(NT$)'] = all_price_ntd
            
            orders.append(resp_order)

        cursor.close()
        cnx.close()

        return render_template('order_list.html', orders=orders)

    except Exception, ex:
        logging.error(str(ex))
    
    return render_template('order.html')

@app.route("/order/items/<order_number>")
def order_items_list_order_number(order_number):
    reload(sys)
    sys.setdefaultencoding('utf-8')

    try:
        logging.warning ('order_number: ' + order_number)

        cnx = mysql.connector.connect(user=config['user'],
                                      password=config['password'],
                                      host=config['host'],
                                      database=config['database'])

        cursor = cnx.cursor()

        if order_number == '0':
            query = ("SELECT name, qty, exchange_rate, price_rmb, price_ntd, fee, total_price_rmb, total_price_ntd, order_number from order_items")
        else :
            query = ("SELECT name, qty, exchange_rate, price_rmb, price_ntd, fee, total_price_rmb, total_price_ntd, order_number from order_items WHERE order_number = " + order_number)
        #logging.warning(query)

        cursor.execute(query)

        order_items = []

        for (name, qty, exchange_rate, price_rmb, price_ntd, fee, total_price_rmb, total_price_ntd, order_number) in cursor:
            resp_order_item = {
                u'品名': '',
                u'數量': '',
                u'匯率': '',
                u'價格(¥)': '',
                u'價格(NT$)': '',
                u'手續費': '',
                u'合計(¥)': '',
                u'合計(NT$)': '',
                u'訂單編號': ''
            }

            resp_order_item[u'品名'] = name
            resp_order_item[u'數量'] = qty
            resp_order_item[u'匯率'] = exchange_rate
            resp_order_item[u'價格(¥)'] = price_rmb
            resp_order_item[u'價格(NT$)'] = price_ntd
            resp_order_item[u'手續費'] = fee
            resp_order_item[u'合計(¥)'] = total_price_rmb
            resp_order_item[u'合計(NT$)'] = total_price_ntd
            resp_order_item[u'訂單編號'] = order_number
            
            order_items.append(resp_order_item)

        cursor.close()
        cnx.close()

        return render_template('order_items.html', order_items=order_items)

    except Exception, ex:
        logging.error(str(ex))

    return render_template('order_items.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)