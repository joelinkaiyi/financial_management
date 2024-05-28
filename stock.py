from flask import Blueprint, render_template, request, redirect
from db_process import getDB

stock_bp = Blueprint('stock', __name__)


@stock_bp.route("/stock", methods=['POST'])
def submitStock():
    processing_fee = 0
    tax = 0
    stock_id = request.values['stock-id']
    stock_num = request.values['stock-num']
    stock_price = request.values['stock-price']
    if request.values['processing-fee'] != "":
        processing_fee = request.values['processing-fee']
    if request.values['tax'] != "":
        tax = request.values['tax']
    date = request.values['date']
    # update database
    conn = getDB()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO stock (stock_id,stock_num,stock_price,processing_fee,tax,date_info) VALUES(?,?,?,?,?,?)""",
                   (stock_id, stock_num, stock_price, processing_fee, tax, date))
    conn.commit()
    return redirect("/")

  
@stock_bp.route('/stock', methods=['GET', 'POST'])
def stock():
    if request.method == 'POST':
        return submitStock()
    return render_template("stock.html")
