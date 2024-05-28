import matplotlib.pyplot as plt
import matplotlib
import os
from db_process import getDB
matplotlib.use('agg')


def stock_chart(unique_stock_list, stock_info):
    if len(unique_stock_list) != 0:
        labels = tuple(unique_stock_list)
        sizes = [d['total_value']for d in stock_info]
        fig, ax = plt.subplots(figsize=(6, 5))
        ax.pie(sizes, labels=labels, autopct=None, shadow=None)
        fig.subplots_adjust(top=1, bottom=0, right=1,
                            left=0, hspace=0, wspace=0)
        plt.savefig("static/stockchart.jpg", dpi=200)
    else:
        try:
            os.remove('static/stockchart.jpg')
        except:
            pass    


def cash_and_stock_chart(usd, currency, td, total_stock_value):
    if usd != 0 or td != 0 or total_stock_value != 0:
        labels = ("USD", "TWD", "Stock")
        sizes = (usd*currency, td, total_stock_value)
        fig, ax = plt.subplots(figsize=(6, 5))
        ax.pie(sizes, labels=labels, autopct=None, shadow=None)
        fig.subplots_adjust(top=1, bottom=0, right=1,
                            left=0, hspace=0, wspace=0)
        plt.savefig("static/cashstockchart.jpg", dpi=200)
    else:
        try:
            os.remove('static/cashstockchart.jpg')
        except:
            pass   
