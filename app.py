from flask import Flask, render_template, request
from analyzer import analyze_coin

app = Flask(__name__)

def calculate_profit_loss(entry_price, tp_price, sl_price, leverage, capital=100):
    position_size = capital * leverage
    tp_profit = (tp_price - entry_price) / entry_price * position_size
    sl_loss = (entry_price - sl_price) / entry_price * position_size
    return round(tp_profit, 2), round(sl_loss, 2)

@app.route("/", methods=["GET", "POST"])
def index():
    data = None
    price = None
    tp = None
    sl = None
    coin = None
    leverage = None
    overall_trend = None
    profit = None
    loss = None

    if request.method == "POST":
        coin = request.form["symbol"].upper()
        data = analyze_coin(coin)
        price = data["price"]

        signals = [result["signal"] for result in data["results"].values()]
        al_count = signals.count("AL")
        sat_count = signals.count("SAT")

        if al_count >= 2:
            overall_trend = "AL"
            leverage = 20 if al_count == 3 else 10
            tp = round(price * 1.015, 6)
            sl = round(price * 0.985, 6)
        elif sat_count >= 2:
            overall_trend = "SAT"
            leverage = 20 if sat_count == 3 else 10
            tp = round(price * 0.985, 6)
            sl = round(price * 1.015, 6)
        else:
            overall_trend = "BEKLE"
            leverage = 1

        if overall_trend in ["AL", "SAT"]:
            profit, loss = calculate_profit_loss(price, tp, sl, leverage)

    return render_template("index.html",
                           coin=coin,
                           signal_data=data,
                           price=price,
                           tp=tp,
                           sl=sl,
                           leverage=leverage,
                           overall_trend=overall_trend,
                           profit=profit,
                           loss=loss)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)