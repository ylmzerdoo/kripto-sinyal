import ccxt
import pandas as pd
import ta

def fetch_ohlcv(symbol="HOT/USDT", interval="1h", limit=100):
    exchange = ccxt.binance()
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=interval, limit=limit)
    df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df

def analyze_coin(symbol):
    df = fetch_ohlcv(symbol)

    # MACD hesapla
    macd = ta.trend.macd_diff(df["close"])
    df["macd"] = macd

    # ATR hesapla (14 periyotluk)
    atr = ta.volatility.AverageTrueRange(high=df["high"], low=df["low"], close=df["close"], window=14).average_true_range()
    df["atr"] = atr

    # TP ve SL hesapla (örnek: son fiyat ± 2 * ATR)
    last_price = df["close"].iloc[-1]
    last_atr = df["atr"].iloc[-1]
    tp = round(last_price + 2 * last_atr, 6)
    sl = round(last_price - 2 * last_atr, 6)

    # MACD sinyali
    macd_signal = "AL" if df["macd"].iloc[-1] > 0 else "SAT"

    return {
        "price": round(last_price, 6),
        "tp": tp,
        "sl": sl,
        "macd": round(df["macd"].iloc[-1], 6),
        "macd_signal": macd_signal
    }
