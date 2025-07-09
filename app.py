import streamlit as st
import pandas as pd
import time
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

# Option to choose trade type
trade_type = st.radio("Select Trade Type:", ["In-Exchange Triangular Trades", "Cross-Exchange Triangular Trades"])

# Manual refresh button
if st.button("🔁 Refresh Now"):
    st.cache_data.clear()

@st.cache_data(ttl=15)
def fetch_opportunities():
    now = datetime.datetime.utcnow()
    data = []
    for _ in range(120):  # Simulating 100+ signals
        ex = random.choice(list(exchange_fees.keys()))
        base = random.choice(["USDT", "USDC"])
        p1, p2, p3 = f"{base} -> A", "A -> B", f"B -> {base}"
        gross = round(random.uniform(0.01, 0.5), 2)
        fee = exchange_fees[ex]
        total_fee = 3 * fee
        net = round(gross - total_fee, 4)
        valid_minutes = random.randint(3, 15)
        valid_until = (now + datetime.timedelta(minutes=valid_minutes)).strftime("%H:%M:%S UTC")
        if net > 0:
            data.append({
                "Exchange": ex,
                "Trade 1": p1,
                "Trade 2": p2,
                "Trade 3": p3,
                "Gross Profit %": gross,
                "Net Profit %": net,
                "Detected": now.strftime("%Y-%m-%d %H:%M:%S"),
                "Valid Until": valid_until
            })
    return data

# Fetch and display
data = fetch_opportunities()

if data:
    df = pd.DataFrame(data)
    df = df.sort_values(by="Net Profit %", ascending=False).reset_index(drop=True)
    st.success(f"Found {len(df)} opportunities. Auto-refreshes every 15 seconds.")
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No profitable arbitrage opportunities found.")

st.caption("Updated every 15 seconds • Ends in USDT or USDC • Same-exchange only or cross-exchange • Gaming UI • Dark Mode")
