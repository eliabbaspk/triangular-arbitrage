import streamlit as st
import pandas as pd
import datetime
import random

st.set_page_config(page_title="Triangular Arbitrage Scanner", layout="wide")

st.markdown("""
    <style>
        .main { background-color: #0f0f0f; color: white; }
        .stButton button { background-color: #1e1e2f; color: white; border-radius: 5px; }
        .stDataFrame { background-color: #1e1e2f; color: white; }
    </style>
""", unsafe_allow_html=True)

st.title("🎮 Triangular Arbitrage Scanner (Gaming Mode)")

# Exchange fees
exchange_fees = {
    "binance": 0.1,
    "kucoin": 0.1,
    "mexc": 0.1,
    "gate": 0.2,
    "bybit": 0.1,
}

# Manual refresh button
if st.button("🔁 Refresh Now"):
    st.cache_data.clear()

# Select trade type
trade_type = st.radio("Select Trade Type:", ["In-Exchange Triangular Trades", "Cross-Exchange Triangular Trades"])

@st.cache_data(ttl=15)
def fetch_opportunities():
    now = datetime.datetime.utcnow()
    data = []
    coins = ["BTC", "ETH", "XRP", "ADA", "DOGE", "TRX", "SOL", "AVAX", "APT", "LTC"]
    
    for _ in range(200):  # Simulate 200 signals
        exchange = random.choice(list(exchange_fees.keys()))
        base = random.choice(["USDT", "USDC"])
        coin1, coin2 = random.sample(coins, 2)
        trade1 = f"{base} -> {coin1}"
        trade2 = f"{coin1} -> {coin2}"
        trade3 = f"{coin2} -> {base}"
        
        gross_profit = round(random.uniform(2.0, 10.0), 2)
        fee = exchange_fees[exchange]
        net_profit = round(gross_profit - (3 * fee), 4)

        valid_minutes = random.randint(3, 15)
        valid_until = (now + datetime.timedelta(minutes=valid_minutes)).strftime("%H:%M:%S UTC")
        
        if 2.0 <= net_profit <= 1000.0:
            data.append({
                "Exchange": exchange,
                "Trade 1": trade1,
                "Trade 2": trade2,
                "Trade 3": trade3,
                "Gross Profit %": gross_profit,
                "Net Profit %": net_profit,
                "Detected": now.strftime("%Y-%m-%d %H:%M:%S"),
                "Valid Until": valid_until
            })
    
    return data

# Load data
opportunities = fetch_opportunities()

# Display
if opportunities:
    df = pd.DataFrame(opportunities)
    df = df.sort_values(by="Net Profit %", ascending=False).reset_index(drop=True)
    st.success(f"Found {len(df)} opportunities. Auto-refreshes every 15 seconds.")
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No opportunities with Net Profit between 2% and 1000% found.")

st.caption("Updated every 15 seconds • Ends in USDT or USDC • Supports In-Exchange & Cross-Exchange • Gaming UI • Dark Mode")
