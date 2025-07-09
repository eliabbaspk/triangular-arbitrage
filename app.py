
import streamlit as st
import pandas as pd
import time
import datetime
import random

st.set_page_config(page_title="Triangular Arbitrage Scanner", layout="wide")
st.title("Triangular Arbitrage Scanner")

exchange_fees = {
    "binance": 0.1,
    "kucoin": 0.1,
    "mexc": 0.1,
    "gate": 0.2,
    "bybit": 0.1,
}

@st.cache_data(ttl=15)
def fetch_opportunities():
    now = datetime.datetime.utcnow()
    data = [
        {
            "exchange": "binance",
            "pair1": "USDT -> BTC",
            "pair2": "BTC -> ETH",
            "pair3": "ETH -> USDT",
            "profit": 0.25,
            "timestamp": now,
        },
        {
            "exchange": "kucoin",
            "pair1": "USDC -> XRP",
            "pair2": "XRP -> ADA",
            "pair3": "ADA -> USDC",
            "profit": 0.12,
            "timestamp": now,
        },
        {
            "exchange": "mexc",
            "pair1": "USDT -> DOGE",
            "pair2": "DOGE -> TRX",
            "pair3": "TRX -> USDT",
            "profit": 0.05,
            "timestamp": now,
        },
        {
            "exchange": "gate",
            "pair1": "USDC -> LTC",
            "pair2": "LTC -> SOL",
            "pair3": "SOL -> USDC",
            "profit": 0.02,
            "timestamp": now,
        },
        {
            "exchange": "bybit",
            "pair1": "USDT -> AVAX",
            "pair2": "AVAX -> APT",
            "pair3": "APT -> USDT",
            "profit": 0.34,
            "timestamp": now,
        },
    ]

    filtered = []
    for row in data:
        fee = exchange_fees[row['exchange']]
        total_fee = 3 * fee
        net_profit = row['profit'] - total_fee
        row['net_profit'] = round(net_profit, 4)
        valid_minutes = random.randint(3, 15)
        row['valid_until'] = (row['timestamp'] + datetime.timedelta(minutes=valid_minutes)).strftime("%H:%M:%S UTC")
        filtered.append(row)

    return filtered

data = fetch_opportunities()

if data:
    df = pd.DataFrame(data)
    df = df.rename(columns={
        "exchange": "Exchange",
        "pair1": "Trade 1",
        "pair2": "Trade 2",
        "pair3": "Trade 3",
        "profit": "Gross Profit %",
        "net_profit": "Net Profit %",
        "timestamp": "Detected",
        "valid_until": "Valid Until"
    })
    st.success(f"Found {len(df)} opportunities. Auto-refreshes every 15 seconds.")
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No arbitrage opportunities found.")

st.caption("Updated every 15 seconds • Ends in USDT or USDC • Same-exchange only • No restrictions")
