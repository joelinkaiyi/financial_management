from flask import Blueprint, render_template, request, redirect
from db_process import getDB

cash_bp = Blueprint('cash', __name__)


@cash_bp.route("/cash", methods=['POST'])
def submitCash():
    taiwanese_dollar = 0
    us_dollar = 0
    if request.values['taiwanese-dollars'] != "":
        taiwanese_dollar = request.values['taiwanese-dollars']
    if request.values['us-dollars'] != "":
        us_dollar = request.values['us-dollars']
    note = request.values['note']
    date = request.values['date']
    # Update database
    conn = getDB()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO cash (taiwanese_dollars, us_dollars, note, date_info) VALUES (?, ?, ?, ?)""",
                   (taiwanese_dollar, us_dollar, note, date))
    conn.commit()

    return redirect("/")

@cash_bp.route("/cash-delete",methods=['POST'])
def deleteCash():
    transaction_id=request.values['id']
    conn=getDB()
    cursor=conn.cursor()
    cursor.execute("""delete from cash where transaction_id=?""",(transaction_id))
    conn.commit()
    return redirect("/")


@cash_bp.route('/cash', methods=['GET', 'POST'])
def cash():
    if request.method == 'POST':
        return submitCash()
    return render_template("cash.html")
