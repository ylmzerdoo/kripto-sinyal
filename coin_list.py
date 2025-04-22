import ccxt

def get_binance_usdt_symbols():
    exchange = ccxt.binance()
    markets = exchange.load_markets()
    symbols = [symbol.split("/")[0] for symbol in markets if symbol.endswith("/USDT")]
    symbols.sort()
    return symbols
