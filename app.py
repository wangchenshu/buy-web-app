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

        query = ("SELECT order_number, order_items, total_price_rmb, total_price_ntd, all_price_rmb, all_price_ntd, created_time, remark, weight, freight_rmb, freight_ntd, ccat_delivery_number from orders WHERE order_number = " + order_number)
        #logging.warning(query)

        cursor.execute(query)

        orders = []

        for (order_number, order_items, total_price_rmb, total_price_ntd, all_price_rmb, all_price_ntd, created_time, remark, weight, freight_rmb, freight_ntd, ccat_delivery_number) in cursor:

            resp_order = {
                u'訂單編號': '',
                u'訂單內容': '',
                u'建立時間': '',
                u'備註': '',
                u'合計(¥)': '',
                u'合計(NT$)': '',
                u'重量(kg)': '',
                u'運費(¥)': '',
                u'運費(NT$)': '',
                u'總金額(¥)': '',
                u'總金額(NT$)': '',
                u'黑貓單號': ''
            }

            resp_order[u'訂單編號'] = order_number
            resp_order[u'訂單內容'] = order_items
            resp_order[u'建立時間'] = created_time
            resp_order[u'備註'] = remark
            resp_order[u'合計(¥)'] = total_price_rmb
            resp_order[u'合計(NT$)'] = total_price_ntd
            resp_order[u'重量(kg)'] = weight
            resp_order[u'運費(¥)'] = freight_rmb
            resp_order[u'運費(NT$)'] = freight_ntd
            resp_order[u'總金額(¥)'] = all_price_rmb
            resp_order[u'總金額(NT$)'] = all_price_ntd
            resp_order[u'黑貓單號'] = ccat_delivery_number
            
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

        query = ("SELECT order_number, order_items, total_price_rmb, total_price_ntd, all_price_rmb, all_price_ntd, created_time, remark, weight, freight_rmb, freight_ntd, ccat_delivery_number from orders WHERE order_number = " + order_number)
        #logging.warning(query)

        cursor.execute(query)

        orders = []

        for (order_number, order_items, total_price_rmb, total_price_ntd, all_price_rmb, all_price_ntd, created_time, remark, weight, freight_rmb, freight_ntd, ccat_delivery_number) in cursor:

            resp_order = {
                u'訂單編號': '',
                u'訂單內容': '',
                u'建立時間': '',
                u'備註': '',
                u'合計(¥)': '',
                u'合計(NT$)': '',
                u'重量(kg)': '',
                u'運費(¥)': '',
                u'運費(NT$)': '',
                u'總金額(¥)': '',
                u'總金額(NT$)': '',
                u'黑貓單號': ''
            }

            resp_order[u'訂單編號'] = order_number
            resp_order[u'訂單內容'] = order_items
            resp_order[u'建立時間'] = created_time
            resp_order[u'備註'] = remark
            resp_order[u'合計(¥)'] = total_price_rmb
            resp_order[u'合計(NT$)'] = total_price_ntd
            resp_order[u'重量(kg)'] = weight
            resp_order[u'運費(¥)'] = freight_rmb
            resp_order[u'運費(NT$)'] = freight_ntd
            resp_order[u'總金額(¥)'] = all_price_rmb
            resp_order[u'總金額(NT$)'] = all_price_ntd
            resp_order[u'黑貓單號'] = ccat_delivery_number
            
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
            query = ("SELECT name, qty, exchange_rate, price_rmb, price_ntd, fee, total_price_rmb, total_price_ntd, order_number, order_number_taobao, taobao_delivery_number, weight from order_items")
        else :
            query = ("SELECT name, qty, exchange_rate, price_rmb, price_ntd, fee, total_price_rmb, total_price_ntd, order_number, order_number_taobao, taobao_delivery_number, weight from order_items WHERE order_number = " + order_number)
        #logging.warning(query)

        cursor.execute(query)

        order_items = []

        for (name, qty, exchange_rate, price_rmb, price_ntd, fee, total_price_rmb, total_price_ntd, order_number, order_number_taobao, taobao_delivery_number, weight) in cursor:
            resp_order_item = {
                u'品名': '',
                u'數量': '',
                u'匯率': '',
                u'單價(¥)': '',
                u'單價(NT$)': '',
                u'手續費': '',
                u'合計(¥)': '',
                u'合計(NT$)': '',
                u'訂單編號': '',
                u'淘寶訂單編號': '',
                u'淘寶貨運單號': '',
                u'重量(kg)': ''
            }

            resp_order_item[u'品名'] = name
            resp_order_item[u'數量'] = qty
            resp_order_item[u'匯率'] = exchange_rate
            resp_order_item[u'單價(¥)'] = price_rmb
            resp_order_item[u'單價(NT$)'] = price_ntd
            resp_order_item[u'手續費'] = fee
            resp_order_item[u'合計(¥)'] = total_price_rmb
            resp_order_item[u'合計(NT$)'] = total_price_ntd
            resp_order_item[u'訂單編號'] = order_number
            resp_order_item[u'淘寶訂單編號'] = order_number_taobao
            resp_order_item[u'淘寶貨運單號'] = taobao_delivery_number
            resp_order_item[u'重量(kg)'] = weight
            
            order_items.append(resp_order_item)

        cursor.close()
        cnx.close()

        return render_template('order_items.html', order_items=order_items)

    except Exception, ex:
        logging.error(str(ex))

    return render_template('order_items.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
