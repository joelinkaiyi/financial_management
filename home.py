from flask import Blueprint, render_template
import requests
import math
import os
from db_process import getDB
from chart import stock_chart, cash_and_stock_chart
home_bp = Blueprint('home', __name__)


@home_bp.route("/")
def home():
    # 獲取database數據
    conn = getDB()
    cursor = conn.cursor()
    result = cursor.execute("SELECT * FROM cash")
    cash_result = result.fetchall()
    print(cash_result)

    # 計算總額
    taiwan_dollars = 0
    us_dollars = 0

    for data in cash_result:
        taiwan_dollars += data[1]
        us_dollars += data[2]

    # 獲取匯率資訊
    r = requests.get('https://tw.rter.info/capi.php')
    currency = r.json()['USDTWD']['Exrate']
    print(currency)

 # 取得所有股票資訊
    result2 = cursor.execute("select * from stock")
    stock_result = result2.fetchall()
    unique_stock_list = []
    for data in stock_result:
        if data[1] not in unique_stock_list:
            unique_stock_list.append(data[1])
    # 計算股票總市值
    total_stock_value = 0

    # 計算單一股票資訊
    stock_info = []
    for stock in unique_stock_list:
        result = cursor.execute(
            "select * from stock where stock_id =?", (stock, ))
        result = result.fetchall()
        stock_cost = 0  # 單一股票總花費
        shares = 0  # 單一股票股數
        for d in result:
            shares += d[2]
            stock_cost += d[2] * d[3] + d[4] + d[5]
        # 取得目前股價
        url = f"https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&stockNo={stock}"
        response = requests.get(url)
        data = response.json()
        if 'data' in data:
            price_array = data['data']
            current_price = float(price_array[-1][6])
        else:
            print(
                f"No 'data' key found in the API response for stock_id {stock}.")
            current_price = 0
        # 單一股票總市值
        total_value = round(current_price * shares)
        total_stock_value += total_value
        # 單一股票平均成本
        average_cost = round(stock_cost / shares, 2)
        # 單一股票報酬率
        rate_of_return = round((total_value - stock_cost)
                               * 100 / stock_cost, 2)
        stock_info.append({'stock_id': stock, 'stock_cost': stock_cost,
                           'total_value': total_value, 'average_cost': average_cost,
                           'shares': shares, 'current_price': current_price, 'rate_of_return': rate_of_return})

    for stock in stock_info:
        stock['value_percentage'] = round(
            stock['total_value'] * 100 / total_stock_value, 2)

    # stock chart
    stock_chart(unique_stock_list=unique_stock_list, stock_info=stock_info)
    # cash and stock chart
    cash_and_stock_chart(usd=us_dollars, currency=currency,
                         td=taiwan_dollars, total_stock_value=total_stock_value)
    total = math.floor((taiwan_dollars + us_dollars * currency))
    data = {'show_stock_picture': os.path.exists('static/stockchart.jpg'), 'show_cash_stock_picture': os.path.exists('static/cashstockchart.jpg'),
            'total': total, 'currency': currency, 'us': us_dollars,
            'twd': taiwan_dollars, 'cashResult': cash_result, 'stock_info': stock_info}
    return render_template("index.html", data=data)
