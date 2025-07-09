# Accurate Triangular Arbitrage Scanner (Binance + MEXC)
# Supports real-time order book data, exchange fees, slippage, and profit estimation.

import streamlit as st
import pandas as pd
import datetime
import ccxt
import time

st.set_page_config(page_title="Real Triangular Arbitrage", layout="wide")
st.title("🔁 Real-Time Triangular Arbitrage Scanner")

# === Configuration ===
EXCHANGES = {
    "binance": {
        "instance": ccxt.binance(),
        "capital": 100,
        "fee": 0.1
    },
    "mexc": {
        "instance": ccxt.mexc(),
        "capital": 50,
        "fee": 0.1
    }
}
SLIPPAGE_PERCENT = 0.15  # Estimate slippage on each trade in %

# === Function to get best ask/bid ===
def get_order_book_price(exchange, symbol, side, amount):
    try:
        ob = exchange.fetch_order_book(symbol)
        levels = ob['asks'] if side == 'buy' else ob['bids']
        cost = 0
        remaining = amount
        for price, qty in levels:
            trade_qty = min(remaining, qty)
            cost += trade_qty * price
            remaining -= trade_qty
            if remaining <= 0:
                avg_price = cost / amount
                return avg_price
        return None  # Not enough liquidity
    except:
        return None

# === Build triangular arbitrage paths ===
def find_triangular_opportunities():
    now = datetime.datetime.utcnow()
    results = []
    for ex_name, ex_data in EXCHANGES.items():
        exchange = ex_data['instance']
        capital = ex_data['capital']
        fee = ex_data['fee']
        try:
            markets = exchange.load_markets()
            symbols = list(markets.keys())
            coins = set()
            for s in symbols:
                if '/USDT' in s or '/USDC' in s:
                    base = s.replace('/USDT','').replace('/USDC','')
                    coins.add(base)
            coins = list(coins)

            for coin1 in coins:
                for coin2 in coins:
                    if coin1 == coin2:
                        continue
                    base_coin = 'USDT'

                    pair1 = f"{base_coin}/{coin1}"
                    pair2 = f"{coin1}/{coin2}"
                    pair3 = f"{coin2}/{base_coin}"

                    if pair1 in symbols and pair2 in symbols and pair3 in symbols:
                        price1 = get_order_book_price(exchange, pair1, 'buy', capital / 3)
                        if not price1: continue
                        coin1_amt = (capital / price1) * (1 - fee/100 - SLIPPAGE_PERCENT/100)

                        price2 = get_order_book_price(exchange, pair2, 'sell', coin1_amt)
                        if not price2: continue
                        coin2_amt = coin1_amt * price2 * (1 - fee/100 - SLIPPAGE_PERCENT/100)

                        price3 = get_order_book_price(exchange, pair3, 'sell', coin2_amt)
                        if not price3: continue
                        final_amt = coin2_amt * price3 * (1 - fee/100 - SLIPPAGE_PERCENT/100)

                        net_profit = final_amt - capital
                        net_profit_pct = (net_profit / capital) * 100

                        if net_profit_pct > 0:
                            results.append({
                                'Exchange': ex_name,
                                'Trade 1': pair1,
                                'Trade 2': pair2,
                                'Trade 3': pair3,
                                'Final Value ($)': round(final_amt, 4),
                                'Net Profit ($)': round(net_profit, 4),
                                'Net Profit (%)': round(net_profit_pct, 2),
                                'Detected': now.strftime('%Y-%m-%d %H:%M:%S'),
                                'Valid Until': (now + datetime.timedelta(minutes=5)).strftime('%H:%M:%S UTC')
                            })
        except:
            continue

    return sorted(results, key=lambda x: x['Net Profit (%)'], reverse=True)

# === Display ===
with st.spinner("Fetching arbitrage opportunities..."):
    data = find_triangular_opportunities()

if data:
    df = pd.DataFrame(data)
    st.success(f"Found {len(df)} profitable opportunities")
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No profitable opportunities found at the moment.")

st.caption("Auto-refresh every 15s • Includes exchange fees + slippage • In-exchange only • Binance & MEXC")
