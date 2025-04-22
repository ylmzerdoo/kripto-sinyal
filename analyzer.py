import ccxt
import pandas as pd

def fetch_ohlcv(symbol, timeframe):
    exchange = ccxt.binance()
    bars = exchange.fetch_ohlcv(f"{symbol}/USDT", timeframe, limit=100)
    df = pd.DataFrame(bars, columns=["timestamp", "open", "high", "low", "close", "volume"])
    return df

def calculate_indicators(df):
    df["ema20"] = df["close"].ewm(span=20).mean()
    df["ema50"] = df["close"].ewm(span=50).mean()

    delta = df["close"].diff()
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
    rs = gain / loss
    df["rsi"] = 100 - (100 / (1 + rs))

    median = (df["high"] + df["low"]) / 2
    df["ao"] = median.rolling(window=5).mean() - median.rolling(window=34).mean()

    rsi = df["rsi"]
    df["stochrsi"] = ((rsi - rsi.rolling(14).min()) / (rsi.rolling(14).max() - rsi.rolling(14).min())).fillna(0)

    return df

def generate_signal(row):
    if row["stochrsi"] > 0.8 and row["ao"] < 0:
        return "SAT"
    elif row["stochrsi"] < 0.2 and row["ao"] > 0:
        return "AL"
    else:
        return "BEKLE"

def analyze_coin(symbol):
    timeframes = ["15m", "1h", "4h"]
    results = {}
    try:
        price = ccxt.binance().fetch_ticker(f"{symbol}/USDT")["last"]
    except:
        return {"symbol": symbol, "price": "Fiyat alınamadı", "results": {}}

    for tf in timeframes:
        try:
            df = fetch_ohlcv(symbol, tf)
            df = calculate_indicators(df)
            last = df.iloc[-1]
            signal = generate_signal(last)

            results[tf] = {
                "rsi": round(last["rsi"], 2),
                "ao": round(last["ao"], 4),
                "stochrsi": round(last["stochrsi"], 4),
                "ema20": round(last["ema20"], 4),
                "ema50": round(last["ema50"], 4),
                "signal": signal
            }
        except:
            results[tf] = {
                "rsi": "HATA", "ao": "HATA", "stochrsi": "HATA",
                "ema20": "HATA", "ema50": "HATA", "signal": "YOK"
            }

    return {"symbol": symbol, "price": price, "results": results}