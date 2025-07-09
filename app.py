import streamlit as st
import pandas as pd
import datetime
import random

st.set_page_config(page_title="Triangular Arbitrage Scanner", layout="wide")

# Dark theme and gaming color UI
st.markdown("""
    <style>
        .main { background-color: #0f0f0f; color: white; }
        .stButton button { background-color: #1e1e2f; color: white; border-radius: 5px; }
        .stDataFrame { background-color: #1e1e2f; color: white; }
    </style>
""", unsafe_allow_html=True)

st.title("🎮 Triangular Arbitrage Scanner (Gaming Mode)")

# Exchange trading fees (simplified flat rate)
exchange_fees = {
    "binance": 0.1,
    "kucoin": 0.1,
    "mexc": 0.1,
    "gate": 0.2,
    "bybit": 0.1,
}

# Refresh Button
if st.button("🔁 Refresh Now"):
    st.cache_data.clear()

# Choose between in-exchange and cross-exchange
trade_type = st.radio("Select Trade Type:", ["In-Exchange Triangular Trades", "Cross-Exchange Triangular Trades"])

@st.cache_data(ttl=15)
def fetch_opportunities():
    now = datetime.datetime.utcnow()
    signals = []
    coins = ["BTC", "ETH", "XRP", "ADA", "DOGE", "TRX", "SOL", "AVAX", "APT", "LTC"]

    for _ in range(250):
        base = random.choice(["USDT", "USDC"])
        coin1, coin2 = random.sample(coins, 2)
        trade1 = f"{base} -> {coin1}"
        trade2 = f"{coin1} -> {coin2}"
        trade3 = f"{coin2} -> {base}"

        buy_order = f"Buy {coin1} with {base}"
        mid_order = f"Convert {coin1} to {coin2}"
        sell_order = f"Sell {coin2} for {base}"

        # Exchange logic
        if trade_type == "In-Exchange Triangular Trades":
            exchange = random.choice(list(exchange_fees.keys()))
        else:  # Cross-Exchange
            exchange = random.choice(list(exchange_fees.keys())) + " ⇄ " + random.choice(list(exchange_fees.keys()))

        gross_profit = round(random.uniform(5000.0, 20000.0), 2)
        fee = 0.3 if "⇄" in exchange else exchange_fees[exchange.split()[0]]
        slippage = random.uniform(1.0, 3.0)  # simulate 1% to 3% slippage
        net_profit = round(gross_profit - (3 * fee) - slippage, 2)

        slippage_risk = "✅ Low" if net_profit > 0 else "❌ High"

        valid_minutes = random.randint(3, 15)
        valid_until = (now + datetime.timedelta(minutes=valid_minutes)).strftime("%H:%M:%S UTC")

        if 5000.0 <= net_profit <= 10000000.0:
            signals.append({
                "Exchange": exchange,
                "Trade 1": trade1,
                "Trade 2": trade2,
                "Trade 3": trade3,
                "Gross Profit %": gross_profit,
                "Net Profit % (After Slippage)": net_profit,
                "Slippage Risk": slippage_risk,
                "Order 1": buy_order,
                "Order 2": mid_order,
                "Order 3": sell_order,
                "Detected": now.strftime("%Y-%m-%d %H:%M:%S"),
                "Valid Until": valid_until
            })

    return signals

# Load and display
results = fetch_opportunities()

if results:
    df = pd.DataFrame(results)
    df = df.sort_values(by="Net Profit % (After Slippage)", ascending=False).reset_index(drop=True)
    st.success(f"Found {len(df)} signals with Net Profit ≥ 5000%. Auto-refresh every 15s.")
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No arbitrage signals with Net Profit ≥ 5000% found.")

st.caption("Updates every 15 seconds • Ends in USDT/USDC • In-Exchange & Cross-Exchange • Gaming UI • Slippage Simulation • Dark Mode")
