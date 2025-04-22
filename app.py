from flask import Flask, render_template, request
from analyzer import analyze_coin

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    coin = ""
    result = None

    if request.method == "POST":
        coin = request.form.get("coin", "").upper()
        if coin:
            try:
                result = analyze_coin(coin + "/USDT")
            except Exception as e:
                result = {"error": str(e)}

    return render_template("index.html", coin=coin, result=result)
