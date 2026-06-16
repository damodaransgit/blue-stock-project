import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import os

# --- Page Configuration ---
st.set_page_config(page_title="Bluestock MF Analytics", page_icon="📈", layout="wide")
st.title("📈 Bluestock Mutual Fund Analytics Dashboard")
st.markdown("*End-to-End Capstone Project Dashboard*")

# --- Data Loading ---
@st.cache_data
def load_data():
    db_path = '../data/db/bluestock_mf.db'
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        # Load tables (using try-except in case tables are missing)
        try:
            df_nav = pd.read_sql("SELECT * FROM fact_nav LIMIT 1000", conn)
        except:
            df_nav = pd.DataFrame()
        conn.close()
        return df_nav
    else:
        # Fallback to processed CSVs or raw CSVs
        sip_path = '../data/raw/04_monthly_sip_inflows.csv'
        aum_path = '../data/raw/03_aum_by_fund_house.csv'
        
        df_sip = pd.read_csv(sip_path) if os.path.exists(sip_path) else pd.DataFrame()
        df_aum = pd.read_csv(aum_path) if os.path.exists(aum_path) else pd.DataFrame()
        return df_sip, df_aum

data_loaded = load_data()
df_sip = data_loaded[0] if isinstance(data_loaded, tuple) else pd.DataFrame()
df_aum = data_loaded[1] if isinstance(data_loaded, tuple) else pd.DataFrame()

# --- Sidebar Filters ---
st.sidebar.header("Filters")
selected_year = st.sidebar.selectbox("Select Year", options=["All", "2022", "2023", "2024", "2025"])

# --- KPI Cards ---
st.header("Industry Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Industry AUM", "₹81 Lakh Cr", "+2.5%")
col2.metric("Monthly SIP Inflow", "₹31,002 Cr", "All-Time High")
col3.metric("Total Folios", "26.12 Cr", "+15%")
col4.metric("Total Schemes", "1,908", "0")

st.divider()

# --- Visualizations ---
colA, colB = st.columns(2)

with colA:
    st.subheader("SIP Inflow Trend")
    if not df_sip.empty:
        fig1 = px.line(df_sip, x='month_year', y='sip_amount_cr', title='Monthly SIP Growth (Rs. Crore)')
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("SIP Data not found. Ensure ETL is completed.")

with colB:
    st.subheader("AUM by Top Fund Houses")
    if not df_aum.empty:
        # Filter for latest year if needed, or aggregate
        df_aum_agg = df_aum.groupby('fund_house')['aum_cr'].max().reset_index().sort_values('aum_cr', ascending=False).head(10)
        fig2 = px.bar(df_aum_agg, x='fund_house', y='aum_cr', title='Top 10 AMCs by AUM')
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("AUM Data not found. Ensure ETL is completed.")

st.divider()

st.header("Advanced Metrics (Demo)")
st.markdown("Run the **Day 6 Advanced Analytics** notebook to populate the Risk-Adjusted Return metrics (Sharpe, VaR) and view them here!")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit. Bluestock Fintech Capstone Project.")
